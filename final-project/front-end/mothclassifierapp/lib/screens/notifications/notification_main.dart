import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import '../../shared/shared.dart';
import '../screens.dart';

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const NotificationsScreen(),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
      ),
      body: Center(
        child: Column(
          children: [
            RaisedButton(
              onPressed: () {
                context.signOut();
                Navigator.of(context).push(AuthScreen.route);
              },
              child: const Text('Sign out'),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.keyboard_backspace_rounded),
        backgroundColor: PainterPalette.lBlue,
        onPressed: () {
          Navigator.of(context).pushReplacement(HomeScreen.route);
        },
      ),
    );
  }
}
