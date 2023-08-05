# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_forecasting',
 'pytorch_forecasting.models',
 'pytorch_forecasting.models.nbeats',
 'pytorch_forecasting.models.temporal_fusion_transformer']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib',
 'optuna>=1.5.0,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pytorch_lightning>=0.8,<0.9',
 'pytorch_ranger',
 'scikit-learn>=0.23,<0.24',
 'scipy',
 'torch>=1.5,<2.0']

setup_kwargs = {
    'name': 'pytorch-forecasting',
    'version': '0.1.2',
    'description': 'Temporal fusion transformer for timeseries forecasting',
    'long_description': '# Timeseries forecasting with Pytorch\n\nInstall with\n\n`pip install pytorch-forecasting`\n\n## Available models\n\n- [Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting](https://arxiv.org/pdf/1912.09363.pdf)\n-\n\n## Usage\n\n```python\nimport pytorch_lightning as pl\nfrom pytorch_lightning.callbacks import EarlyStopping\n\nfrom pytorch_forecasting import TimeSeriesDataSet, TemporalFusionTransformer\n\n# load data\ndata = ...\n\n# define dataset\nmax_encode_length = 36\nmax_prediction_length = 6\ntraining_cutoff = "YYYY-MM-DD"  # day for cutoff\n\ntraining = TimeSeriesDataSet(\n    data[lambda x: x.date < training_cutoff],\n    time_idx= ...,\n    target= ...,\n    # weight="weight",\n    group_ids=[ ... ],\n    max_encode_length=max_encode_length,\n    max_prediction_length=max_prediction_length,\n    static_categoricals=[ ... ],\n    static_reals=[ ... ],\n    time_varying_known_categoricals=[ ... ],\n    time_varying_known_reals=[ ... ],\n    time_varying_unknown_categoricals=[ ... ],\n    time_varying_unknown_reals=[ ... ],\n)\n\n\nvalidation = TimeSeriesDataSet.from_dataset(training, data, min_prediction_idx=training.index.time.max() + 1)\nbatch_size = 128\ntrain_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=2)\nval_dataloader = validation.to_dataloader(train=False, batch_size=batch_size, num_workers=2)\n\n\nearly_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=1, verbose=False, mode="min")\ntrainer = pl.Trainer(\n    max_epochs=10,\n    gpus=0,\n    gradient_clip_val=0.1,\n    early_stop_callback=early_stop_callback,\n)\n\n\ntft = TemporalFusionTransformer.from_dataset(training)\nprint(f"Number of parameters in network: {tft.size()/1e3:.1f}k")\n\ntrainer.fit(\n    tft, train_dataloader=train_dataloader, val_dataloaders=val_dataloader,\n)\n```\n',
    'author': 'Jan Beitner',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jdb78/pytorch_forecasting',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
