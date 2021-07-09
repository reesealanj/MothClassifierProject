# Moth Classifier Project Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

# Releases

[100% Demo, v0.6.0](#100-demo)

[90% Demo, v0.5.0](#90-demo)

[70% Demo, v0.4.0](#70-demo)

[40% Demo, v0.3.0](#40-demo)

[30% Demo, v0.2.0](#30-demo)

[Bootcamp Demo, v0.1.0](#bootcamp-demo)

---

## 100% Demo

## [v0.6.0] - 2021-04-07

### <ins>Front End</ins>

### Added

-   Added Pagination to Reclassify and Submissions
-   Added in depth error handling for pages with data submissions
-   Added caching for reclassification page

### Changed

-   Changed styling across application
-   Changed buttons across application to be consistent and more obvious

### <ins>API</ins>

### Added

-   Added and configured nginx and gunicorn for production
-   Configured and added settings to distinguish between production and development
-   Added more detailed logging messages for production
-   Added an endpoint to allow users to request researcher access

### Security

-   Configured HTTPS for production

### <ins>Machine Learning</ins>

### Changed
- Trained and improved machine learning model to classify the five most common species of moths in the database. 

---

## 90% Demo

## [v0.5.0] - 2021-03-03

### <ins>Front End</ins>

### Added

-   Added more assets
-   Added assets in smaller sizes to reduce bundle size for deployment
-   Added some error checking to the API service to reduce fatal crashes

### Changed

-   Changed folder structure of screens to make link tree less complex
-   Changed folder structure of services to reduce bundle size
-   Changed a number of icons for better readability
-   Changed UI in response to HCI demo critiques

### Removed

-   Removed unused files to reduce bundle size
-   Removed some unused functions to decrease tree shake time during production builds

### <ins>API</ins>

### Added

-   Added a periodic celery task to generate a zip file for the training dataset every 24 hours if needed
-   Wrote SLURM script for High Performance Web Scraping

### Changed

-   Changed the download_images service to use a pre-built training dataset to prevent a large training dataset zip file from being generated on every request
-   Changed run.sh to run the celery and ml_subscribe services to run in the background and to redirect the output of each service to log files.
-   Changed how duplicate images are handled. Duplicate images are now allowed in the system if they belong to different users. A single user cannot upload duplicate images.

### Security

-   Added a secrets.py file to hold important passwords and private information
-   Enabled throttling for anonymous users to avoid a large amount of requests from unknown users

### <ins>Machine Learning</ins>

### Added

-   Added ability to filter by total number of images
-   Added ability to clean up working directory for working on Cluster

### Changed

-   Changed parameters for increased model performance
-   Changed layers and filters per layer

---

## 70% Demo

## [v0.4.0] - 2021-01-27

### <ins>Front End</ins>

### Added

-   Added custom Exceptions for more descriptive error handling with Login, Registration, API, and Authentication Token errors
-   Added new pre-compile podfile dependency to optimize build times for iOS builds (from ~600 seconds avg to ~75 seconds avg buildtime) [Link to Article Explanation](https://github.com/FirebaseExtended/flutterfire/issues/2751).
-   Added LitFirebaseAuth for authentication state
-   Added dashboard page with links to other sections of the application instead of bottom bar navigation
-   Added retry and sign out buttons for dashboard when a user with cached sign in information doesn't have an internet connection.
-   Added ability to save and print debug information and refresh authentication tokens manually (option is only present in devices running the application in debug mode through flutter)
-   Added ability to change profile name from within the application profile screen.
-   Added more in depth documentation to the ApiService
-   Added Device model for tracking notification handler state.
-   Added Submissions tab to view a user's previously submitted images
-   Added Details screen to both User submissions and Reclassifications

### Changed

-   Upgraded Versions for the following plugins:
    -   firebase_core: 0.5.3
    -   firebase_analytics: 6.3.0
    -   firebase_auth: 0.18.4
    -   cloud_firestore: 0.14.4
    -   firebase_messaging: 5.1.4
    -   google_sign_in: 4.5.6
-   Changed login data flow to now make request for user information from API <i>outside</i> of the AuthService
-   Changed SignIn and Registration pages to be more modern, now include animations
-   Changed Authentication state sharing solution, now use LitAuth
-   Changed Page Routing solution from Named routes to Component parameter based routes
-   Third party authentication no longer errors out when cancelled, and will display a notification to indicate it was cancelled by the User.
-   Changed how ApiService gathers User information, now all of a User's information is stored in a Global variable (referenceable anywhere by calling Global.currUserData and Global.currApiData)
-   Changed submission screen so that the image submission is now compatible with MothClassifierApi setup (multipart/form-data)
-   Changed how notification tokens are handled. Now on login check to see if token is registered. If not, register it. If yes, patch to mark as active. On Logout, mark notification token as inactive.
-   Changed how global notification state is handled, now initialization and widget generation for notifications is done once globally and shared across app tree.
-   Changed notification handler to display alert dialog on notification reciept
-   Changed organization of application structure, now all screens are nested within their own folders and each folder contains all relevant screens for a specific task.

### Removed

-   No longer grabbing user collection reference from Firestore Collection at login
-   Removed old authentication service.
-   Removed old Login and Resgistration pages
-   Removed all old screen refrences which are no longer actively used.

### Security

-   Registration now requires a nontrivial password (as determined by firebase) and will throw an exception if firebase determines password is "too weak"

### <ins>API</ins>

### Added

-   Added functionality to register and update the information of mobile devices to the API
-   Added functionality to send notifications to devices following job completion or failure

### <ins>Machine Learning</ins>

### Added

-   Added service handler for communication over Pub/Sub channels with API Job Service
-   Added functionality to communicate between Machine Learning model output and API with proper response formatting

---

## 40% Demo

## [v0.3.0] - 2020-12-09

### <ins>Front End</ins>

### Added

-   Google Cloud Function project
-   Implemented cloud function to listen to database writes to a "notification" collection
-   Added BottomBar builder to make modifying bottom bar behavior take less code

### Changed

-   Changed behavior of Bottom Navigation bar
-   Changed behavior of routed navigation stack, now replaces old stack contents on new screen generation

### Removed

-   Removed old API service which was no longer being utilized
-   Removed usage of previous bottomNavigationBar and associated references

### <ins>API</ins>

### Added

-   Added the pub/sub communication model with the Machine Learning service
-   Added a `status_message` field to the Job model and a `file_name` field to MLModel model.

### <ins>Machine Learning</ins>

### Added

-   Added test methods which extracts a zip file of unclassified data, returns prediction and confidence on each image
-   Added visualization for output, shows prediction, input, and reference of prediction

### Changed

-   Changed functionality of temporary files for classification jobs (now folders generated will be removed and replaced with every run)
-   Changed functionality load and test flow so that old files from previous jobs will not prevent the program from being run more than once

---

## 30% Demo

## [v0.2.0] - 2020-11-24

### <ins>Front End</ins>

#### Added

-   Data Models for: Classification, Notification, Photo, and ReviewGridItem
-   Review Grid that can be built using API
-   API Service to handle fetching of async data
-   Added ability to submit images from Camera
-   Added Mock JSON API (and associated configuration) for improved local testing
-   Added basic implementation of Notification Handler (only shows Snackbar of notification title for now)
-   Added changelog file

#### Changed

-   Bottom AppBar changes based on type of user's account
-   Login authentication flow for Email Login
-   Modified look of Submission Screen
-   Output of a User image submission changed from Hex encoded string to multipart/form-data
-   Adjusted Data Model for User

#### Removed

-   Populating user data state from Firebase Firestore, will be replaced with API calls in the future
-   UserModel from Firebase, replaced with Custom UserData model

### <ins>API</ins>

#### Added

-   Added an endpoint to download a collection of images
-   Refined the image endpoint by detecting duplicate images
-   Wrote [API usage guide](http://167.172.31.118:8000/api/v1/docs/)
-   Added permissions to each API endpoint
-   Added tests for each API endpoint. Tests cover views, serializers, and services
-   Added changelog file

#### Changed

-   Endpoints relating to users now use uid instead of id
-   Modified web scraper to utilize new authentication scheme

#### Removed

-   Removed POST requests for the users endpoint as creating users is handled by Firebase Authentication

#### Security

-   Implemented API authentication with Firebase Authentication

### <ins>Machine Learning</ins>

#### Added

-   Added utility to get dataset from the Moth Classifier API
-   Added functionality train a model based on moth image data
-   Added utility to use a specified number of classes from dataset

#### Changed

-   Modified zip file extraction to be compatible with dataset from Moth Classifier API

---

## Bootcamp Demo

## [v0.1.0] - 2020-10-28

### <ins>Front End</ins>

#### Added

-   Implemented basic functionality of Navigator between pages
-   Implemented basic Email Registration and Sign In
-   Implemented Google Sign In
-   Implemented Apple Sign In
-   Modeled Firestore Collection to maintain user information for Login and Authentication

#### Security

-   Implemented authentication with Firebase Authentication

### <ins>API</ins>

#### Added

-   Implemented basic functionality of API by adding the users, images, jobs, classifications, and models endpoints
-   Wrote shell script to automate starting up the API server
-   Wrote a web scraper that utilizes multi-processing to extract moth images from Discover Life

### <ins>Machine Learning</ins>

#### Added

-   Configured Tensorflow
-   Added a flower model in accordance with the Tensorflow tutorial
-   Created a class that handles the Machine Learning service architecture
