"""
Timeseries models share a number of common characteristics. This module implements these in a common base class.
"""
from copy import deepcopy
import inspect
import cloudpickle
from torch import unsqueeze
from torch.functional import Tensor

from torch.utils.data import DataLoader
from tqdm.notebook import tqdm

from pytorch_forecasting.metrics import SMAPE
from typing import Any, Dict, List, Tuple, Union
from pytorch_lightning import LightningModule
from pytorch_lightning.metrics.metric import TensorMetric
from pytorch_ranger import Ranger
import torch
import numpy as np
import pandas as pd
from torch.optim.lr_scheduler import ReduceLROnPlateau, LambdaLR, OneCycleLR

import matplotlib.pyplot as plt
from pytorch_forecasting.data import TimeSeriesDataSet
from pytorch_forecasting.utils import groupby_apply

from pytorch_lightning.utilities.parsing import AttributeDict, collect_init_args, get_init_args


class BaseModel(LightningModule):
    """
    BaseModel from which new timeseries models should inherit from.
    The ``hparams`` of the created object will default to the parameters indicated in :py:meth:`~__init__`.

    The ``forward()`` method should return a dictionary with at least the entry ``prediction`` that contains the network's output

    Example:

        .. code-block:: python

            class Network(BaseModel):

                def __init__(self, my_first_parameter: int=2, loss=SMAPE()):
                    self.save_hyperparameters()
                    super().__init__()
                    self.loss = loss

                def forward(self, x):
                    encoding_target = x["encoder_target"]
                    return dict(prediction=...)

                # implement lightning steps
                def training_step(self, batch, batch_idx):
                    x, y = batch
                    return {"loss": self.loss.to_prediction(self(x), y)}

                # implement further steps

    """

    def __init__(
        self,
        log_interval=-1,
        log_val_interval: int = None,
        learning_rate: Union[float, List[float]] = 1e-3,
        log_gradient_flow: bool = False,
        loss: TensorMetric = SMAPE(),
        logging_metrics: List[TensorMetric] = [],
        reduce_on_plateau_patience: int = 1000,
        weight_decay: float = 0.0,
        monotone_constaints: Dict[str, int] = {},
        log_space: bool = False,
    ):
        """
        BaseModel for timeseries forecasting from which to inherit from

        Args:
            log_interval (int, optional): batches after which predictions are logged. Defaults to -1.
            log_val_interval (int, optional): batches after which predictions for validation are logged. Defaults to 
                None/log_interval.
            learning_rate (float, optional): Learning rate. Defaults to 1e-3.
            log_gradient_flow (bool): If to log gradient flow, this takes time and should be only done to diagnose 
                training failures. Defaults to False.
            loss (TensorMetric, optional): metric to optimize. Defaults to SMAPE().
            logging_metrics: (List[TensorMetric], optional): list of metrics to log.
            reduce_on_plateau_patience (int): patience after which learning rate is reduced by a factor of 10. Defaults 
                to 1000
            weight_decay (float): weight decay. Defaults to 0.0.
            monotone_constaints (Dict[str, int]): dictionary of monotonicity constraints for continuous decoder 
                variables mapping
                position (e.g. ``"0"`` for first position) to constraint (``-1`` for negative and ``+1`` for positive, 
                larger numbers add more weight to the constraint vs. the loss but are usually not necessary). 
                This constraint significantly slows down training. Defaults to {}.
        """
        super().__init__()
        # update hparams
        frame = inspect.currentframe()
        init_args = get_init_args(frame)
        self.save_hyperparameters({name: val for name, val in init_args.items() if name not in self.hparams})

        # update log interval if not defined
        if self.hparams.log_val_interval is None:
            self.hparams.log_val_interval = self.hparams.log_interval

        if not hasattr(self, "loss"):
            self.loss = loss
        if not hasattr(self, "logging_metrics"):
            self.logging_metrics = logging_metrics

    def size(self) -> int:
        """
        get number of parameters in model
        """
        return sum(p.numel() for p in self.parameters())

    def training_step(self, batch, batch_idx):
        x, y = batch
        log, _ = self.step(x, y, batch_idx, label="train")
        return log

    def training_epoch_end(self, outputs):
        log, _ = self.epoch_end(outputs, label="train")
        return log

    def validation_step(self, batch, batch_idx):
        x, y = batch
        log, _ = self.step(x, y, batch_idx, label="val")
        return log

    def validation_epoch_end(self, outputs):
        log, _ = self.epoch_end(outputs, label="val")
        return log

    def step(self, x: Dict[str, torch.Tensor], y: torch.Tensor, batch_idx: int, label="train"):
        """
        Run for each train/val step.
        """
        if label == "train" and len(self.hparams.monotone_constaints) > 0:
            # calculate gradient with respect to continous decoder features
            x["decoder_cont"].requires_grad_(True)
            out = self(x)
            y_hat = out["prediction"]
            gradient = torch.autograd.grad(
                outputs=y_hat,
                inputs=x["decoder_cont"],
                grad_outputs=torch.ones_like(y_hat),  # t
                create_graph=True,  # allows usage in graph
                allow_unused=True,
            )[0]

            # select relevant features
            indices = torch.tensor([int(i) for i in self.hparams.monotone_constaints.keys()])
            monotonicity = torch.tensor(
                [self.hparams.monotone_constaints[str(i.item())] for i in indices], dtype=gradient.dtype
            )
            # add additionl loss if gradient points in wrong direction
            gradient = gradient[..., indices] * monotonicity[None, None]
            monotinicity_loss = gradient.clamp_max(0).mean()
            # multiply monotinicity loss by large number to ensure relevance and take to the power of 2
            # for smoothness of loss function
            monotinicity_loss = 10 * torch.pow(monotinicity_loss, 2)

            loss = self.loss(y_hat, y) * (1 + monotinicity_loss)
        else:
            out = self(x)
            y_hat = out["prediction"]
            # calculate loss
            loss = self.loss(y_hat, y)

        # log loss
        tensorboard_logs = {f"{label}_loss": loss}
        # logging losses
        y_hat_detached = self.loss.to_prediction(y_hat.detach())
        for metric in self.logging_metrics:
            tensorboard_logs[f"{label}_{metric.name}"] = metric(y_hat_detached, y)
        log = {f"{label}_loss": loss, "log": tensorboard_logs, "n_samples": x["decoder_lengths"].size(0)}
        if label == "train":
            log["loss"] = loss
        if self.log_interval(label == "train") > 0:
            self._log_prediction(x, y_hat, batch_idx, label=label)
        return log, out

    def epoch_end(self, outputs, label="train"):
        """
        Run at epoch end for training or validation.
        """
        if "callback_metrics" in outputs[0]:  # workaround for pytorch-lightning bug
            outputs = [out["callback_metrics"] for out in outputs]
        # log average loss and metrics
        n_samples = sum([x["n_samples"] for x in outputs])
        avg_loss = torch.stack([x[f"{label}_loss"] * x["n_samples"] / n_samples for x in outputs]).sum()
        log_keys = outputs[0]["log"].keys()
        tensorboard_logs = {
            f"avg_{key}": torch.stack([x["log"][key] * x["n_samples"] / n_samples for x in outputs]).sum()
            for key in log_keys
        }

        return {f"{label}_loss": avg_loss, "log": tensorboard_logs}, outputs

    def log_interval(self, train: bool):
        """
        Log interval depending if training or validating
        """
        if train:
            return self.hparams.log_interval
        else:
            return self.hparams.log_val_interval

    def _log_prediction(self, x, y_hat, batch_idx, label="train"):
        # log single prediction figure
        if batch_idx % self.log_interval(label == "train") == 0 and self.log_interval(label == "train") > 0:
            y_all = torch.cat(
                [x["encoder_target"][0], x["decoder_target"][0]]
            )  # all true values for y of the first sample in batch
            if y_all.ndim == 2:  # timesteps, (target, weight), i.e. weight is included
                y_all = y_all[:, 0]
            max_encoder_length = x["encoder_lengths"].max()
            fig = self.plot_prediction(
                torch.cat(
                    (
                        y_all[: x["encoder_lengths"][0]],
                        y_all[max_encoder_length : (max_encoder_length + x["decoder_lengths"][0])],
                    ),
                ),
                y_hat[0, : x["decoder_lengths"][0]].detach(),
            )  # first in batch
            tag = f"{label.capitalize()} prediction"
            if label == "train":
                tag += f" of item 0 in global batch {self.global_step}"
            else:
                tag += f" of item 0 in batch {batch_idx}"
            self.logger.experiment.add_figure(
                tag, fig, global_step=self.global_step,
            )

    def plot_prediction(self, y: torch.Tensor, y_hat: torch.Tensor) -> plt.Figure:
        """
        Plot prediction of prediction vs actuals

        Args:
            y: all actual values
            y_hat: predictions

        Returns:
            matplotlib figure
        """
        # move to cpu
        y = y.detach().cpu()
        y_hat = y_hat.cpu()
        # create figure
        fig, ax = plt.subplots()
        n_pred = y_hat.shape[0]
        x_obs = np.arange(y.shape[0] - n_pred)
        x_pred = np.arange(y.shape[0] - n_pred, y.shape[0])
        prop_cycle = iter(plt.rcParams["axes.prop_cycle"])
        obs_color = next(prop_cycle)["color"]
        pred_color = next(prop_cycle)["color"]
        # plot observed history
        if len(x_obs) > 0:
            if len(x_obs) > 1:
                plotter = ax.plot
            else:
                plotter = ax.scatter
            plotter(x_obs, y[:-n_pred], label="observed", c=obs_color)
        if len(x_pred) > 1:
            plotter = ax.plot
        else:
            plotter = ax.scatter
        # plot observed prediction
        plotter(x_pred, y[-n_pred:], label=None, c=obs_color)

        # plot prediction
        plotter(x_pred, self.loss.to_prediction(y_hat), label="predicted", c=pred_color)

        # plot predicted quantiles
        y_quantiles = self.loss.to_quantiles(y_hat)
        plotter(x_pred, y_quantiles[:, y_quantiles.shape[1] // 2], c=pred_color, alpha=0.15)
        for i in range(y_quantiles.shape[1] // 2):
            if len(x_pred) > 1:
                ax.fill_between(x_pred, y_quantiles[:, i], y_quantiles[:, -i - 1], alpha=0.15, fc=pred_color)
            else:
                ax.errorbar(
                    x_pred, torch.tensor([[y_quantiles[0, i]], [y_quantiles[0, -i - 1]]]), c=pred_color, capsize=1.0,
                )
        loss = self.loss(y_hat[None], y[-n_pred:][None])
        ax.set_title(f"Loss {loss:.3g}")
        ax.set_xlabel("Time index")
        fig.legend()
        return fig

    def _log_gradient_flow(self, named_parameters: Dict[str, Tensor]) -> None:
        """
        log distribution of gradients to identify exploding / vanishing gradients
        """
        ave_grads = []
        layers = []
        for name, p in named_parameters:
            if p.grad is not None and p.requires_grad and "bias" not in name:
                layers.append(name)
                ave_grads.append(p.grad.abs().mean())
                self.logger.experiment.add_histogram(tag=name, values=p.grad, global_step=self.global_step)
        fig, ax = plt.subplots()
        ax.plot(ave_grads)
        ax.set_xlabel("Layers")
        ax.set_ylabel("Average gradient")
        ax.set_yscale("log")
        ax.set_title("Gradient flow")
        self.logger.experiment.add_figure("Gradient flow", fig, global_step=self.global_step)

    def on_after_backward(self):
        """
        Log gradient flow for debugging.
        """
        if (
            self.global_step % self.hparams.log_interval == 0
            and self.hparams.log_interval > 0
            and self.hparams.log_gradient_flow
        ):
            self._log_gradient_flow(self.named_parameters())

    def configure_optimizers(self):
        """
        Configure optimizers.

        Uses single Ranger optimizer. Depending if learning rate is a list or a single float, implement dynamic 
        learning rate scheduler or deterministic version

        Returns:
            Tuple[List]: first entry is list of optimizers and second is list of schedulers
        """
        # either set a schedule of lrs or find it dynamically
        if isinstance(self.hparams.learning_rate, (list, tuple)):  # set schedule
            lrs = self.hparams.learning_rate
            optimizer = Ranger(self.parameters(), lr=lrs[0])
            # normalize lrs
            lrs = np.array(lrs) / lrs[0]
            schedulers = [
                {
                    "scheduler": LambdaLR(optimizer, lambda epoch: lrs[min(epoch, len(lrs) - 1)]),
                    "interval": "epoch",
                    "reduce_on_plateau": False,
                    "frequency": 1,
                }
            ]
        else:  # find schedule based on validation loss
            optimizer = Ranger(self.parameters(), lr=self.hparams.learning_rate, weight_decay=self.hparams.weight_decay)
            schedulers = [
                {
                    "scheduler": ReduceLROnPlateau(
                        optimizer,
                        mode="min",
                        factor=0.1,
                        patience=self.hparams.reduce_on_plateau_patience,
                        cooldown=self.hparams.reduce_on_plateau_patience,
                    ),
                    "monitor": "val_loss",  # Default: val_loss
                    "interval": "epoch",
                    "reduce_on_plateau": True,
                    "frequency": 1,
                }
            ]

        return [optimizer], schedulers

    def _get_mask(self, size, lengths, inverse=False):
        if inverse:  # return where values are
            return torch.arange(size, device=self.device).unsqueeze(0) < lengths.unsqueeze(-1)
        else:  # return where no values are
            return torch.arange(size, device=self.device).unsqueeze(0) >= lengths.unsqueeze(-1)

    @classmethod
    def from_dataset(cls, dataset: TimeSeriesDataSet, **kwargs) -> LightningModule:
        """
        Create model from dataset, i.e. save dataset parameters in model

        This function should be called as ``super().from_dataset()`` in a derived models that implement it

        Args:
            dataset (TimeSeriesDataSet): timeseries dataset

        Returns:
            BaseModel: Model that can be trained
        """
        net = cls(**kwargs)
        net.dataset_parameters = dataset.get_parameters()
        return net

    def on_save_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        checkpoint["dataset_parameters"] = getattr(
            self, "dataset_parameters", None
        )  # add dataset parameters for making fast predictions
        checkpoint["loss"] = cloudpickle.dumps(self.loss)  # restore loss
        checkpoint[
            "hparams_name"
        ] = "kwargs"  # hyper parameters are passed as arguments directly and not as single dictionary

    def on_load_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        self.dataset_parameters = checkpoint.get("dataset_parameters", None)
        self.loss = cloudpickle.loads(checkpoint["loss"])

    def predict(
        self,
        data: Union[DataLoader, pd.DataFrame, TimeSeriesDataSet],
        mode: Union[str, Tuple[str, str]] = "prediction",
        return_index: bool = False,
        return_decoder_lengths: bool = False,
        batch_size: int = 64,
        num_workers: int = 0,
        fast_dev_run: bool = False,
        show_progress_bar: bool = False,
    ):
        """
        predict dataloader

        Args:
            dataloader: dataloader, dataframe or dataset
            mode: one of "prediction", "quantiles" or "raw", or tuple ``("raw", output_name)`` where output_name is
                a name in the dictionary returned by ``forward()``
            return_index: if to return the prediction index
            return_decoder_lengths: if to return decoder_lengths
            batch_size: batch size for dataloader - only used if data is not a dataloader is passed
            num_workers: number of workers for dataloader - only used if data is not a dataloader is passed
            fast_dev_run: if to only return results of first batch
            show_progress_bar: if to show progress bar. Defaults to True

        Returns:
            output, index, decoder_lengths: some elements might not be present depending on what is configured 
                to be returned
        """
        # convert to dataloader
        if isinstance(data, pd.DataFrame):
            data = TimeSeriesDataSet.from_parameters(self.dataset_parameters, data, predict=True)
        if isinstance(data, TimeSeriesDataSet):
            dataloader = data.to_dataloader(batch_size=batch_size, train=False, num_workers=num_workers)
        else:
            dataloader = data

        # ensure passed dataloader is correct
        assert isinstance(dataloader.dataset, TimeSeriesDataSet), "dataset behind dataloader mut be TimeSeriesDataSet"

        # prepare model
        self.eval()  # no dropout, etc. no gradients

        # run predictions
        output = []
        decode_lenghts = []
        progress_bar = tqdm(desc="Predict", unit=" batches", total=len(dataloader), disable=not show_progress_bar)
        with torch.no_grad():
            for x, _ in dataloader:
                out = self(x)  # raw output is dictionary
                lengths = x["decoder_lengths"]
                if return_decoder_lengths:
                    decode_lenghts.append(lengths)
                nan_mask = self._get_mask(out["prediction"].size(1), lengths)
                if isinstance(mode, (tuple, list)):
                    if mode[0] == "raw":
                        out = out[mode[1]]
                    else:
                        raise ValueError(
                            f"If a tuple is specified, the first element must be 'raw' - got {mode[0]} instead"
                        )
                elif mode == "prediction":
                    out = self.loss.to_prediction(out["prediction"])
                    # mask non-predictions
                    out = out.masked_fill(nan_mask, torch.tensor(float("nan")))
                elif mode == "quantiles":
                    out = self.loss.to_quantiles(out["prediction"])
                    # mask non-predictions
                    out = out.masked_fill(nan_mask.unsqueeze(-1), torch.tensor(float("nan")))
                elif mode == "raw":
                    pass
                else:
                    raise ValueError(f"Unknown mode {mode} - see docs for valid arguments")

                output.append(out)
                progress_bar.update()
                if fast_dev_run:
                    break

        # concatenate
        if isinstance(mode, (tuple, list)) or mode != "raw":
            output = torch.cat(output, dim=0)
        elif mode == "raw":
            output = {name: torch.cat(values, dim=0) for name, values in output.items()}

        if return_decoder_lengths:
            decoder_lengths = torch.cat(decode_lenghts, dim=0)

        # get index
        if return_index:
            index = dataloader.dataset.get_index()

        if return_index and return_decoder_lengths:
            return output, index, decoder_lengths
        elif return_index:
            return output, index
        elif return_decoder_lengths:
            return output, decoder_lengths
        else:
            return output

    def calculate_prediction_actual_by_variable(
        self,
        x: Dict[str, torch.Tensor],
        y_pred: torch.Tensor,
        normalize: bool = True,
        bins: int = 95,
        std: float = 2.0,
    ) -> Dict[str, Dict[str, torch.Tensor]]:
        """
        Calculate predictions and actuals by variable averaged by ``bins`` bins spanning from ``-std`` to ``+std``

        Args:
            x: input as ``forward()``
            y_pred: predictions obtained by ``self.loss.to_prediction(self(x))``
            normalize: if to return normalized averages, i.e. mean or sum of ``y``
            bins: number of bins to calculate
            std: number of standard deviations for standard scaled continuous variables

        Returns:
            dictionary that can be used to plot averages with ``plot_prediction_actual_by_variable()``
        """
        support = {}  # histogram
        # averages
        averages_actual = {}
        averages_prediction = {}

        # mask values and transform to log space
        max_encoder_length = x["decoder_lengths"].max()
        mask = self._get_mask(max_encoder_length, x["decoder_lengths"], inverse=True)
        # select valid y values
        y_flat = x["decoder_target"][mask]
        y_pred_flat = y_pred[mask]
        if self.loss.log_space:
            y_flat = torch.log(y_flat + 1e-8)
            y_pred_flat = torch.log(y_pred_flat + 1e-8)

        # real bins
        positive_bins = (bins - 1) // 2

        # if to normalize
        if normalize:
            reduction = "mean"
        else:
            reduction = "sum"
        # continuous variables
        reals = x["decoder_cont"]
        for idx, name in self.hparams.real_labels.items():
            averages_actual[name], support[name] = groupby_apply(
                (reals[..., int(idx)][mask] * positive_bins / std).round().clamp(-positive_bins, positive_bins).long()
                + positive_bins,
                y_flat,
                bins=bins,
                reduction=reduction,
                return_histogram=True,
            )
            averages_prediction[name], _ = groupby_apply(
                (reals[..., int(idx)][mask] * positive_bins / std).round().clamp(-positive_bins, positive_bins).long()
                + positive_bins,
                y_pred_flat,
                bins=bins,
                reduction=reduction,
                return_histogram=True,
            )

        # categorical_variables
        cats = x["decoder_cat"]
        for idx, name in self.hparams.categorical_labels.items():
            averages_actual[name], support[name] = groupby_apply(
                cats[..., int(idx)][mask],
                y_flat,
                bins=self.hparams.embedding_sizes[idx][0],
                reduction=reduction,
                return_histogram=True,
            )
            averages_prediction[name], _ = groupby_apply(
                cats[..., int(idx)][mask],
                y_pred_flat,
                bins=self.hparams.embedding_sizes[idx][0],
                reduction=reduction,
                return_histogram=True,
            )
        return {
            "support": support,
            "average": {"actual": averages_actual, "prediction": averages_prediction},
            "std": std,
        }

    def plot_prediction_actual_by_variable(
        self, data: Dict[str, Dict[str, torch.Tensor]], name: str = None
    ) -> Union[Dict[str, plt.Figure], plt.Figure]:
        """
        Plot predicions and actual averages by variables
        
        Args:
            data (Dict[str, Dict[str, torch.Tensor]]): data obtained from 
                :py:ref:`~calculate_prediction_actual_by_variable`
            name (str, optional): name of variable for which to plot actuals vs predictions. Defaults to None which means returning a 
                dictionary of plots for all variables.

        Raises:
            ValueError: if the variable name is unkown

        Returns:
            Union[Dict[str, plt.Figure], plt.Figure]: matplotlib figure
        """
        if name is None:  # run recursion for figures
            figs = {name: self.plot_prediction_actual_by_variable(data, name) for name in data["support"].keys()}
            return figs
        else:
            # create figure
            kwargs = {}
            # adjust figure size for figures with many labels
            if name in self.hparams.categorical_labels.values():
                for idx, label_name in self.hparams.categorical_labels.items():
                    if label_name == name:
                        break
                if self.hparams.embedding_sizes[str(idx)][0] > 10:
                    kwargs = dict(figsize=(10, 5))
            fig, ax = plt.subplots(**kwargs)
            ax.set_title(f"{name} averages")
            ax.set_xlabel(name)
            if self.loss.log_space:
                ax.set_ylabel("Log prediction")
            else:
                ax.set_ylabel("Prediction")
            ax2 = ax.twinx()  # second axis for histogram
            ax2.set_ylabel("Frequency")

            # get values for average plot and histogram
            values_actual = data["average"]["actual"][name].cpu().numpy()
            values_prediction = data["average"]["prediction"][name].cpu().numpy()
            bins = values_actual.size
            support = data["average"][name].cpu().numpy()

            # only display values where samples were observed
            support_non_zero = support > 0
            support = support[support_non_zero]
            values_actual = values_actual[support_non_zero]
            values_prediction = values_prediction[support_non_zero]

            # plot averages
            if name in self.hparams.real_labels.values():
                for idx, label_name in self.hparams.real_labels.items():
                    if label_name == name:
                        break
                mean, scale = self.hparams.real_scales[idx]
                x = np.linspace(-data["std"], data["std"], bins) * scale + mean
                if len(x) > 0:
                    x_step = x[1] - x[0]
                else:
                    x_step = 1
                x = x[support_non_zero]
                ax.plot(x, values_actual, label="Actual")
                ax.plot(x, values_prediction, label="Prediction")

            elif name in self.hparams.categorical_labels.values():
                for idx, label_name in self.hparams.categorical_labels.items():
                    if label_name == name:
                        break
                # sort values from lowest to highest
                sorting = values_actual.argsort()
                labels = np.asarray(self.hparams.embedding_labels[str(idx)])[support_non_zero][sorting]
                values_actual = values_actual[sorting]
                values_prediction = values_prediction[sorting]
                support = support[sorting]
                # cut entries if there are too many categories to fit nicely on the plot
                maxsize = 50
                if values_actual.size > maxsize:
                    values_actual = np.concatenate([values_actual[: maxsize // 2], values_actual[-maxsize // 2 :]])
                    values_prediction = np.concatenate(
                        [values_prediction[: maxsize // 2], values_prediction[-maxsize // 2 :]]
                    )
                    labels = np.concatenate([labels[: maxsize // 2], labels[-maxsize // 2 :]])
                    support = np.concatenate([support[: maxsize // 2], support[-maxsize // 2 :]])
                # plot for each category
                x = np.arange(values_actual.size)
                x_step = 1
                ax.scatter(x, values_actual, label="Actual")
                ax.scatter(x, values_prediction, label="Prediction")
                # set labels at x axis
                ax.set_xticks(x)
                ax.set_xticklabels(labels, rotation=90)
            else:
                raise ValueError(f"Unknown name {name}")
            # plot support histogram
            ax2.bar(x, support, width=x_step, linewidth=0, alpha=0.2, color="k")
            # adjust layout and legend
            fig.tight_layout()
            fig.legend()
            return fig
