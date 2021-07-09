# Setting Up the Front End Module

### Prerequisites

-   Install Android Studio (and install an Anroid Virtual Device with support for Android APK 20 or higher and is Google-Play enabled)
-   Install the Flutter SDK (follow the official install guide [here](https://flutter.dev/docs/get-started/install))
-   Clone the GitHub Repository
-   Create a firebase project for the application (for your own development) and setup configuration files in accordance with the Firebase documentation [here](https://firebase.flutter.dev/docs/overview). If the Firebase documentation is too complicated this [YouTube Video](https://www.youtube.com/watch?v=Mx24wiPilHg&t=3s) is also helpful!

### Installing Libraries

-   Within your local copy of the GitHub repository, navigate to /front-end/mothclassifierapp
-   Run `flutter pub get`. This will install all libraries included in the `pubspec.yaml` file
-   Once all the libraries are installed, you can run `flutter doctor` which will verify flutter and a compatible emulator have been installed and that you will be able to run apps
-   The only way to properly verify libraries were installed for the project is to attempt to start the app with `flutter run`, which will build and compile the app and attempt to install it on your active emulator. If libraries were not properly installed the application will not start and will exit with an error that reads `Package {package name} was not found.` In that case you can run `flutter pub get` a second time and then `flutter run`.
