# Friendly MLOps: Making Deployment Flexible and Easy

The repo is to accompany the Friendly MLOps workshop at ODSC East given by Rajiv Shah and Tim Whittaker.  

Rajiv and Tim provide an easy explanation of critical issues around MLOps and get you started deploying a model.

This workshop relies on [DRUM](https://github.com/datarobot/datarobot-user-models), an open source deployment framework, that provides automated testing and flexibility around deployment pipelines. DRUM provides built-in support for a variety of modeling frameworks including Keras, scikit learn, R, H2O, DataRobot, and more. So join us to see how we can making MLOps friendlier.

* Using DRUM for performance testing of models
* Using DRUM for validation of models
* Using DRUM to get a REST API endpoint
* Show ease of swapping models out (different framewokrs - H2O GLM, DataRobot LGMB, Python Catboost, Python XGBoost
* Instrument humility rules

## Usage

The notebooks included in this repo are best run on Google Colab. Either use the link within the notebook or upload it to github.  

## Repository Contents

This repo contains
* Colab - Friendly MLOps
* data - folder containing data used in the Friendly MLOPs notebook]
* models - folder containing various models trained on [10k diabetes dataset](./data/readmissions_train.csv)

## Setup/Installation

While this was meant to run in colab, you can use [colab_requirements.txt](colab_requirements.txt) to set up the python environment locally.  

## Development and Contributing

If you'd like to report an issue or bug, suggest improvements, or contribute code to this project, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).


# Code of Conduct

This project has adopted the Contributor Covenant for its Code of Conduct. 
See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) to read it in full.

# License

Licensed under the Apache License 2.0. 
See [LICENSE](LICENSE) to read it in full.


