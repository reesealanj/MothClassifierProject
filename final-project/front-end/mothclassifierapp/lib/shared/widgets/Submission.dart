import 'package:flutter/material.dart';
import '../../services/services.dart';
import '../../screens/screens.dart';

class Submission extends StatelessWidget {
  final SubmissionModel submission;

  const Submission({
    Key key,
    @required this.submission,
  })  : assert(submission != null),
        super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Image.network(
        submission.fileUrl,
        width: 80.0,
        height: 80.0,
      ),
      title: Text('Submitted on: ${submission.dateTaken}'),
      onTap: () async {
        PhotoData photo =
            await Global.apiService.photoFromUrl(submission.imageUrl);
        Classification classification =
            await Global.apiService.classificationFromUrl(submission.classUrl);
        Navigator.of(context).pushAndRemoveUntil(
            MaterialPageRoute(
              builder: (context) => SubmissionDetailScreen(
                data: photo,
                classification: classification,
              ),
            ),
            (Route<dynamic> route) => false);
      },
    );
  }
}
