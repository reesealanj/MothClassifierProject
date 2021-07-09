# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.6.0] - 2021-04-07

### Added

-   Added Pagination to Reclassify and Submissions
-   Added in depth error handling for pages with data submissions
-   Added caching for reclassification page

### Changed

-   Changed styling across application
-   Changed buttons across application to be consistent and more obvious

## [v0.5.0] - 2021-03-03

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

## [v0.4.0] - 2021-01-27

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

## [v0.3.0] - 2020-12-09

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

## [v0.2.0] - 2020-11-24

### Added

-   Data Models for: Classification, Notification, Photo, and ReviewGridItem
-   Review Grid that can be built using API
-   API Service to handle fetching of async data
-   Added ability to submit images from Camera
-   Added Mock JSON API (and associated configuration) for improved local testing
-   Added basic implementation of Notification Handler (only shows Snackbar of notification title for now)
-   Added changelog file

### Changed

-   Bottom AppBar changes based on type of user's account
-   Login authentication flow for Email Login
-   Modified look of Submission Screen
-   Output of a User image submission changed from Hex encoded string to multipart/form-data
-   Adjusted Data Model for User

### Removed

-   Populating user data state from Firebase Firestore, will be replaced with API calls in the future
-   UserModel from Firebase, replaced with Custom UserData model

## [v0.1.0] - 2020-10-28

### Added

-   Implemented basic functionality of Navigator between pages
-   Implemented basic Email Registration and Sign In
-   Implemented Google Sign In
-   Implemented Apple Sign In
-   Modeled Firestore Collection to maintain user information for Login and Authentication

### Security

-   Implemented authentication with Firebase Authentication
