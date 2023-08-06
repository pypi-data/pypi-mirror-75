# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['metriculous', 'metriculous.evaluators']

package_data = \
{'': ['*']}

install_requires = \
['assertpy>=0.14.0',
 'bokeh>=2.1.1,<3.0.0',
 'jupyter>=1.0,<2.0',
 'numpy>=1.16',
 'pandas>=0.24.0',
 'scikit-learn>=0.21.2']

setup_kwargs = {
    'name': 'metriculous',
    'version': '0.2.0',
    'description': 'Very unstable library containing utilities to measure and visualize statistical properties of machine learning models.',
    'long_description': '<p align="center">\n    <a href="https://mybinder.org/v2/gh/metriculous-ml/metriculous/master?filepath=notebooks">\n        <img alt="Launch Binder" src="https://mybinder.org/badge_logo.svg">\n    </a>\n    <a href="https://github.com/ambv/black">\n        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n    </a>\n</p>\n\n# __`metriculous`__\nUnstable python library with utilities to measure, visualize and compare statistical properties of machine learning models. Breaking improvements to be expected.\n\n\n# Installation\n```console\n$ pip install metriculous\n```\n\nOr, for the latest unreleased version:\n```console\n$ pip install git+https://github.com/metriculous-ml/metriculous.git\n```\n\nOr, to avoid getting surprised by breaking changes:\n```console\n$ pip install git+https://github.com/metriculous-ml/metriculous.git@YourFavoriteCommit\n```\n\n\n# Usage\n\n### Comparing Regression Models  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/metriculous-ml/metriculous/master?filepath=notebooks%2Fquickstart_regression.py)\n\n```python\nimport numpy as np\n\n# Mock the ground truth, a one-dimensional array of floats\nground_truth = np.random.random(300)\n\n# Mock the output of a few models\nperfect_model = ground_truth\nnoisy_model = ground_truth + 0.1 * np.random.randn(*ground_truth.shape)\nrandom_model = np.random.randn(*ground_truth.shape)\nzero_model = np.zeros_like(ground_truth)\n\nimport metriculous\n\nmetriculous.compare_regressors(\n    ground_truth=ground_truth,\n    model_predictions=[perfect_model, noisy_model, random_model, zero_model],\n    model_names=["Perfect Model", "Noisy Model", "Random Model", "Zero Model"],\n).save_html("comparison.html").display()\n```\n\nThis will save an HTML file with common regression metrics and charts, and if you are working in a [Jupyter notebook](https://github.com/jupyter/notebook) will display the output right in front of you:\n\n\n![Screenshot of Metriculous Regression Metrics](./imgs/metriculous_regression_screen_shot_table.png)\n![Screenshot of Metriculous Regression Figures](./imgs/metriculous_regression_screen_shot_figures.png)\n\n### Comparing Classification Models [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/metriculous-ml/metriculous/master?filepath=notebooks%2Fquickstart_classification.py)\nFor an example that evaluates and compares classifiers please refer to the [quickstart notebook for classification](notebooks/quickstart_classification.ipynb).\n\n\n# Development\n\n### Poetry\nThis project uses [poetry](https://poetry.eustace.io/) to manage\ndependencies. Please make sure it is installed for the required python version. Then install the dependencies with `poetry install`.\n\n### Makefile\nA Makefile is used to automate common development workflows. Type `make` or `make help` to see a list of available commands. Before commiting changes it is recommended to run `make format check test`.\n',
    'author': 'Marlon',
    'author_email': None,
    'maintainer': 'Marlon',
    'maintainer_email': None,
    'url': 'https://github.com/metriculous-ml/metriculous',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
