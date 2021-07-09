# Front End Module

### Main Dev: Reese Jones

## Frameworks and Tools:

    - Flutter
    - Firebase Authentication
    - Firebase Firestore
    - FlutterFire authentication wrappers

## Packages Used:

Package versions can be found in `pubspec.yaml` in the root directory.
Run `flutter pub get` to have flutter download packages at versions specified in pubspec file.

-   Firebase Core
-   Firebase Analytics
-   Cloud Firestore
-   Firebase Auth
-   Google_Sign_In
-   Apple_Sign_In
-   image_picker
-   rxdart
-   provider
-   font_awesome_flutter

## Important Commands

-   Creating a blank flutter project: `flutter create myapp`
-   Cleaning build files for clean build: `flutter clean`
-   Building app APK (android) or XCode Runner (ios): `flutter build (apk/ios)`
-   Build and Run application in Debug mode: `flutter run`

## Requirements to Run on your own Computer

-   Have the latest Flutter installed (whether through git or their stable releases)
    -   [Flutter Getting Started Guide](https://flutter.dev/docs/get-started/install)
-   Clone this repo and navigate to `/front-end/mothclassifierapp`
-   From anywhere in `mothclassifierapp` run `flutter pub get` to have flutter download and install all dependencies
-   Run `flutter run` to build and run app.
    -   There must be a virtual device on your computer for flutter to "connect" to.
    -   On Windows: Android Virtual Device through android studio OR connect your own device via USB
        -   On Windows, there is some extra legwork to do in order to be able to deploy flutter apps to a Physical device.
        -   [Flutter Docss Instructions for Physical Device install](https://flutter.dev/docs/get-started/install/windows#set-up-your-android-device)
    -   On MacOS: iOS Simulator or AVD through android studio OR connect your own device via USB

## Important Files for App

-   `/lib/main.dart`
    -   This is the root of the application. Below is a list of tasks accomplished in the main file.
        -   Instantiate root material app which encapsulates the widget tree
        -   Register all routes (pages) and name them
        -   Register global themes for children to use
        -   Register providers for sharing data across the widget tree
        -   Register navigator object used for navigating between screens
-   `/lib/screens/`
    -   This directory holds one file for every screen in the app
    -   Each screen is registered as its own named route
-   `/lib/services/`
    -   This directory holds services that are reused across the business logic of the application (i.e. uploading images, authenticating users, accessing/writing to the database)
-   `/lib/shared/`
    -   This directory holds shared widgets needed across the app (bottom navBar, loading indicator)
-   `/ios/ and /android/`
    -   These two directories hold the actual project files for the android and ios application implementations. Running `flutter run` builds the flutter app and creates the project files needed for each native platform.
