import 'package:flutter/material.dart';
import '../../screens/screens.dart';
import '../../shared/shared.dart';

class SubmissionsPageTwo extends StatelessWidget {
  const SubmissionsPageTwo({
    Key key,
  }) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const SubmissionsPageTwo(),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Submissions'),
      ),
      body: Submissions(),
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
