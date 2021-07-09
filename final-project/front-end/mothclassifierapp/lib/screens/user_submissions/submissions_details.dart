import 'package:flutter/material.dart';
import '../../services/services.dart';
import '../../shared/shared.dart';
import '../screens.dart';

class SubmissionDetailScreen extends StatefulWidget {
  final PhotoData data;
  final Classification classification;
  const SubmissionDetailScreen(
      {Key key, @required this.data, this.classification})
      : super(key: key);

  @override
  _SubmissionDetailScreenState createState() => _SubmissionDetailScreenState();
}

class _SubmissionDetailScreenState extends State<SubmissionDetailScreen> {
  Classification classification;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Submission No. ${widget.data.id}'),
      ),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.fromLTRB(10.0, 10.0, 10.0, 0),
            child: Image.network(
              widget.data.fileUrl,
              fit: BoxFit.contain,
              height: 300,
            ),
          ),
          Text(
            'Submitted On: ${widget.data.dateTaken}',
            style: TextStyle(
              fontStyle: FontStyle.italic,
              fontSize: 16.0,
            ),
          ),
          SizedBox(height: 20),
          Text(
            'Classification',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 28,
              fontStyle: FontStyle.normal,
            ),
          ),
          SizedBox(height: 15),
          Text(
            'Species: ${widget.classification.species}',
            textAlign: TextAlign.start,
            style: TextStyle(
              fontSize: 20,
            ),
          ),
          SizedBox(height: 10),
          Text(
            'Accuracy: ${widget.classification.accuracy} %',
            textAlign: TextAlign.start,
            style: TextStyle(
              fontSize: 20,
            ),
          ),
          SizedBox(height: 10),
          SizedBox(
            width: MediaQuery.of(context).size.width * 0.8,
            child: (widget.classification.needsReview)
                ? Text(
                    'The above classification was automatically assigned by our Machine Learning Model and will be reviewed for accuracy by a DiscoverLife moth researcher',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 14,
                      fontStyle: FontStyle.italic,
                    ),
                  )
                : (widget.classification.isAutomated)
                    ? Text(
                        'The above classification was automatically assigned by our Machine Learning Model with a high degree of accuracy and will not be reviewed by a Researcher',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 14,
                          fontStyle: FontStyle.italic,
                        ),
                      )
                    : Text(
                        'The above classification was manually assigned by a DiscoverLife moth researcher',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 14,
                          fontStyle: FontStyle.italic,
                        ),
                      ),
          ),
          Global.fcmShared,
        ],
      ),
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
