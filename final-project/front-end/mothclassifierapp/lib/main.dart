import 'package:flutter/material.dart';
import 'package:firebase_analytics/observer.dart';
import 'package:firebase_analytics/firebase_analytics.dart';

import 'package:firebase_core/firebase_core.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import 'package:mothclassifierapp/shared/painter_palette.dart';

import 'screens/screens.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LitAuthInit(
      authProviders: const AuthProviders(
        emailAndPassword: true,
        google: true,
        apple: true,
      ),
      child: MaterialApp(
        title: 'DiscoverLife Moth Classifier',
        // Initialization for Firebase Analytics
        navigatorObservers: [
          FirebaseAnalyticsObserver(analytics: FirebaseAnalytics()),
        ],
        debugShowCheckedModeBanner: false,
        home: const LitAuthState(
          authenticated: HomeScreen(),
          unauthenticated: SplashScreen(),
        ),
        // Global Themeing for Application
        theme: ThemeData(
          brightness: Brightness.light,
          fontFamily: 'Nunito',
          bottomAppBarTheme: BottomAppBarTheme(color: Colors.black87),
          visualDensity: VisualDensity.adaptivePlatformDensity,
          textTheme: GoogleFonts.muliTextTheme(),
          accentColor: PainterPalette.dOrange,
          appBarTheme: const AppBarTheme(
            brightness: Brightness.dark,
            color: PainterPalette.dBlue,
          ),
        ),
      ),
    );
  }
}
