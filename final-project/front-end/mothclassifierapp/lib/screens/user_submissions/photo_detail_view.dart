import 'package:flutter/material.dart';
import 'package:mothclassifierapp/screens/screens.dart';
import '../../services/services.dart';
import '../../shared/shared.dart';

class PhotoDetailView extends StatelessWidget {
  final SubmissionModel data;
  const PhotoDetailView({Key key, @required this.data}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Submissions'),
      ),
      body: Text(data.imageUrl),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.keyboard_backspace_rounded),
        backgroundColor: PainterPalette.lBlue,
        onPressed: () {
          Navigator.of(context).pushReplacement(SubmissionsPageTwo.route);
        },
      ),
    );
  }
}
