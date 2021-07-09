# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.6.0] - 2021-04-07
### Added
- Added and configured nginx and gunicorn for production
- Configured and added settings to distinguish between production and development
- Added more detailed logging messages for production
- Added an endpoint to allow users to request researcher access

### Security
- Configured HTTPS for production

## [v0.5.0] - 2021-03-02
### Added
- Added a periodic celery task to generate a zip file for the training dataset every 24 hours if needed
- Wrote SLURM script for High Performance Web Scraping

### Changed
- Changed the download_images service to use a pre-built training dataset to prevent a large training dataset zip file from being generated on every request
- Changed run.sh to run the celery and ml_subscribe services to run in the background and to redirect the output of each service to log files. 
- Changed how duplicate images are handled. Duplicate images are now allowed in the system if they belong to different users. A single user cannot upload duplicate images.

### Security
- Added a secrets.py file to hold important passwords and private information
- Enabled throttling for anonymous users to avoid a large amount of requests from unknown users

## [v0.4.0] - 2021-01-26
### Added
- Added functionality to register and update the information of mobile devices to the API
- Added functionality to send notifications to devices following job completion or failure

## [v0.3.0] - 2020-12-09
### Added
- Added the pub/sub communication model with the Machine Learning service
- Added a ```status_message``` field to the Job model and a ```file_name``` field to MLModel model.

## [v0.2.0] - 2020-11-24
### Added
- Added an endpoint to download a collection of images
- Refined the image endpoint by detecting duplicate images
- Wrote [API usage guide](http://167.172.31.118:8000/api/v1/docs/)
- Added permissions to each API endpoint
- Added tests for each API endpoint. Tests cover views, serializers, and services
- Added changelog file

### Changed
- Endpoints relating to users now use uid instead of id
- Modified web scraper to utilize new authentication scheme

### Removed
- Removed POST requests for the users endpoint as creating users is handled by Firebase Authentication

### Security
- Implemented API authentication with Firebase Authentication

## [v0.1.0] - 2020-10-28
### Added
- Implemented basic functionality of API by adding the users, images, jobs, classifications, and models endpoints
- Wrote shell script to automate starting up the API server
- Wrote a web scraper that utilizes multi-processing to extract moth images from Discover Life
