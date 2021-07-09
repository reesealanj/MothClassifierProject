import 'package:flutter/material.dart';
import '../../screens/screens.dart';
import '../../shared/shared.dart';

class ReclassificationsPageTwo extends StatelessWidget {
  const ReclassificationsPageTwo({
    Key key,
  }) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const ReclassificationsPageTwo(),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Reclassify'),
      ),
      body: Reclassifications(),
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
