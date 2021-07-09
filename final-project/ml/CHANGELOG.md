# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.6.0] - 2021-04-07
### Changed
- Trained and improved machine learning model to classify the five most common species of moths in the database. 

## [v0.5.0] - 2021-03-03

### Added
- Added ability to filter by total number of images
- Added ability to clean up working directory for working on Cluster
### Changed
- Changed parameters for increased model performance
- Changed layers and filters per layer

## [v0.4.0] - 2021-01-27

### Added
- Added service handler for communication over Pub/Sub channels with API Job Service
- Added functionality to communicate between Machine Learning model output and API with proper response formatting

## [v0.3.0] - 2020-12-09

### Added
- Added test methods which extracts a zip file of unclassified data, returns prediction and confidence on each image
- Added visualization for output, shows prediction, input, and reference of prediction

### Changed
- Changed functionality of temporary files for classification jobs (now folders generated will be removed and replaced with every run)
- Changed functionality load and test flow so that old files from previous jobs will not prevent the program from being run more than once

## [v0.2.0] - 2020-11-24
#### Added
- Added utility to get dataset from the Moth Classifier API
- Added functionality train a model based on moth image data
- Added utility to use a specified number of classes from dataset

#### Changed
- Modified zip file extraction to be compatible with dataset from Moth Classifier API

## [v0.1.0] - 2020-10-28
#### Added
- Configured Tensorflow
- Added a flower model in accordance with the Tensorflow tutorial
- Created a class that handles the Machine Learning service architecture
