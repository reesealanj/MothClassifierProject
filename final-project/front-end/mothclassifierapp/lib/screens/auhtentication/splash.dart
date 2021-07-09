import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import '../screens.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const SplashScreen(),
      );

  @override
  Widget build(BuildContext context) {
    final user = context.watchSignedInUser();
    user.map(
      (value) {
        _navigateToHomeScreen(context);
      },
      empty: (_) {
        _navigateToAuthScreen(context);
      },
      initializing: (_) {},
    );

    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }

  // Use widgetsBinding.instance.addPostFrameCallback
  // so that this will only be called once Build has run at LEAST once
  void _navigateToAuthScreen(BuildContext context) {
    print('Calling NavigateToAuthScreen');
    WidgetsBinding.instance.addPostFrameCallback(
      (_) => Navigator.of(context).pushAndRemoveUntil(
        AuthScreen.route,
        (Route<dynamic> route) => false,
      ),
    );
  }

  void _navigateToHomeScreen(BuildContext context) {
    print('Calling NavigateToHomeScreen');
    WidgetsBinding.instance.addPostFrameCallback(
      (_) => Navigator.of(context).pushAndRemoveUntil(
        HomeScreen.route,
        (Route<dynamic> route) => false,
      ),
    );
  }
}
