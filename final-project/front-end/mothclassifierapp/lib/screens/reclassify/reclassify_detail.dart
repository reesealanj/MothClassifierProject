import 'package:flutter/material.dart';
import 'package:mothclassifierapp/screens/reclassify/reclassify_redo.dart';
import '../../services/services.dart';
import '../../shared/shared.dart';

class ReclassifyDetailScreen extends StatefulWidget {
  final PhotoData imgData;
  final ReclassificationModel classData;

  const ReclassifyDetailScreen({
    Key key,
    @required this.imgData,
    @required this.classData,
  }) : super(key: key);

  @override
  _ReclassifyDetailScreenState createState() => _ReclassifyDetailScreenState();
}

class _ReclassifyDetailScreenState extends State<ReclassifyDetailScreen> {
  String dropdownValue = 'Select A Classification';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Submission no. ${widget.imgData.id}'),
      ),
      body: Center(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Padding(
              padding: EdgeInsets.fromLTRB(10, 10, 10, 0),
              child: Image.network(
                widget.imgData.fileUrl,
                fit: BoxFit.contain,
                height: 300,
              ),
            ),
            Text(
              'Submitted On: ${widget.imgData.dateTaken}',
              style: TextStyle(
                fontStyle: FontStyle.italic,
                fontSize: 14,
              ),
            ),
            SizedBox(height: 10),
            Text(
              'Machine Classification:',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 2),
            Text(
              '${widget.classData.species}',
              style: TextStyle(
                fontStyle: FontStyle.italic,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 10),
            Text(
              'Machine Accuracy:',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            SizedBox(height: 2),
            Text(
              '${widget.classData.accuracy}',
              style: TextStyle(
                fontSize: 18,
              ),
            ),
            SizedBox(height: 25),
            Container(
              width: MediaQuery.of(context).size.width * 0.75,
              child: Padding(
                padding: EdgeInsetsDirectional.only(start: 10.0),
                child: DropdownButton(
                  value: dropdownValue,
                  elevation: 16,
                  onChanged: (String newValue) {
                    setState(() {
                      dropdownValue = newValue;
                    });
                  },
                  isExpanded: true,
                  items: <String>[
                    'Select A Classification',
                    'Phigalia Denticulata',
                    'Hypoprepia Fucosa',
                    'Melanolophia Canadaria-Signataria',
                    'Microcrambus Elegans',
                    'Phigalia Strigataria',
                    'Miscellaneous'
                  ].map<DropdownMenuItem<String>>((String value) {
                    return DropdownMenuItem<String>(
                      value: value,
                      child: Text(value),
                    );
                  }).toList(),
                ),
              ),
            ),
            RaisedButton(
              onPressed: () async {
                if (dropdownValue != 'Select A Classification') {
                  showDialog(
                    context: context,
                    builder: (BuildContext context) {
                      return AlertDialog(
                        title: Text(
                          'Reclassify Image no. ${widget.imgData.id}',
                        ),
                        content: Text(
                          'Would you like to officially classify this image as $dropdownValue? Once confirmed, this classification is final and can NOT be changed.',
                        ),
                        actions: [
                          FlatButton(
                            child: Text("Yes!"),
                            onPressed: () async {
                              var res =
                                  await Global.apiService.updateClassification(
                                dropdownValue,
                                widget.imgData.id,
                              );
                              if (res) {
                                Navigator.of(context).pushAndRemoveUntil(
                                  ReclassificationsPageTwo.route,
                                  (Route<dynamic> route1) => false,
                                );
                              }
                            },
                            color: Colors.green,
                          ),
                          FlatButton(
                            child: Text(
                              "Cancel",
                            ),
                            onPressed: () {
                              Navigator.of(context).pop();
                            },
                            color: Colors.red,
                          ),
                        ],
                      );
                    },
                  );
                } else {
                  showDialog(
                    context: context,
                    builder: (BuildContext context) {
                      return AlertDialog(
                        title: Text(
                          'Reclassify Image no. ${widget.imgData.id}',
                        ),
                        content: Text(
                          'You must select a classification from the dropdown!',
                        ),
                        actions: [
                          FlatButton(
                            child: Text(
                              "Ok!",
                            ),
                            onPressed: () {
                              Navigator.of(context).pop();
                            },
                          ),
                        ],
                      );
                    },
                  );
                }
              },
              child: Text(
                'Submit Classification',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 18,
                ),
              ),
            ),
            Global.fcmShared,
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.keyboard_backspace_rounded),
        backgroundColor: PainterPalette.lBlue,
        onPressed: () {
          Navigator.of(context).pushReplacement(ReclassificationsPageTwo.route);
        },
      ),
    );
  }
}
