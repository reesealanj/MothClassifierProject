import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:path/path.dart' as path;
import 'dart:io';
import '../../shared/shared.dart';
import '../../services/services.dart';
import '../screens.dart';

class SubmitScreen extends StatefulWidget {
  const SubmitScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const SubmitScreen(),
      );

  SubmitScreenState createState() => SubmitScreenState();
}

class SubmitScreenState extends State<SubmitScreen> {
  ImgService imgService = new ImgService();
  Future<File> fileStream;
  File file;
  PhotoData submittedInformation;
  bool fileUploaded = false;
  bool loaderVisible = false;
  bool fileSelected = false;

  chooseImage() async {
    try {
      Future<File> temp = imgService.choose(Global.currApiData.uid);

      setState(() {
        fileStream = temp;
        fileSelected = true;
      });
    } on PhotoPickerException catch (e) {
      setState(() {
        fileStream = null;
        fileSelected = false;
      });
    }
  }

  uploadImage() async {
    setState(() {
      loaderVisible = true;
    });
    try {
      submittedInformation = await Global.apiService.submitImageForSignedInUser(
        file,
        path.basename(file.path),
      );
    } on ApiException catch (e) {
      var eJson = jsonDecode(e.message);
      var msg = eJson['file'];
      if (msg.contains('Image already exists')) {
        raiseErrorDialogue();
      }

      setState(() {
        loaderVisible = false;
        fileUploaded = false;
      });
    } on InvalidTokenException catch (e) {
      Global.refreshAuthToken(context);
      uploadImage();
    }

    if (submittedInformation != null) {
      await Global.apiService
          .startClassifyJobSignedInUser(submittedInformation.id);

      setState(() {
        loaderVisible = false;
        fileUploaded = true;
      });
    }
  }

  clearImage() {
    setState(() {
      fileUploaded = false;
      fileSelected = false;
      loaderVisible = false;
      fileStream = null;
      file = null;
      submittedInformation = null;
    });
  }

  raiseErrorDialogue() {
    print('oops');
  }

  Widget showImage() {
    return FutureBuilder<File>(
      future: fileStream,
      builder: (BuildContext context, AsyncSnapshot<File> snapshot) {
        if (snapshot.connectionState == ConnectionState.done &&
            null != snapshot.data) {
          file = snapshot.data;
          return Flexible(
            fit: FlexFit.tight,
            child: Image.file(
              snapshot.data,
            ),
          );
        } else if (null != snapshot.error) {
          return const Text(
            'Error Picking Image',
            style: TextStyle(
              color: Colors.red,
            ),
            textAlign: TextAlign.center,
          );
        } else {
          return SizedBox(height: 1);
        }
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Submit'),
      ),
      body: Container(
        margin: EdgeInsets.all(20),
        child: Center(
          child: loaderVisible
              ? Loader()
              : Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(height: 20),
                    RaisedButton(
                      onPressed: () {
                        chooseImage();
                      },
                      child: const Text(
                        'Select Image to Submit',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                    ),
                    (fileSelected)
                        ? RaisedButton(
                            color: Colors.redAccent,
                            onPressed: () {
                              clearImage();
                            },
                            child: const Text(
                              'Clear Selected Image',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 18,
                              ),
                            ),
                          )
                        : SizedBox(height: 1),
                    SizedBox(height: 20),
                    showImage(),
                    SizedBox(height: 20),
                    RaisedButton(
                      color: Colors.greenAccent,
                      onPressed: () async {
                        await uploadImage();
                      },
                      child: const Text(
                        'Upload Image',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                    ),
                    SizedBox(height: 20),
                    fileUploaded
                        ? Text(
                            "File Submitted!",
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 18,
                              color: Colors.green,
                            ),
                          )
                        : Container(),
                    Global.fcmShared,
                  ],
                ),
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
