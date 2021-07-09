import 'package:flutter/material.dart';
import '../../services/services.dart';
import '../../shared/shared.dart';
import '../screens.dart';

class ReclassifyScreen extends StatefulWidget {
  const ReclassifyScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const ReclassifyScreen(),
      );

  createState() => ReclassifyScreenState();
}

class ReclassifyScreenState extends State<ReclassifyScreen> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Reclassify'),
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            FutureBuilder<List<ReviewData>>(
              future: Global.apiService.fetchNeedsReviewObjects(),
              builder: (BuildContext context, AsyncSnapshot snapshot) {
                if (snapshot.connectionState == ConnectionState.done) {
                  if (snapshot.hasError) {
                    print('Snapshot.error! ${snapshot.error}');
                    return Center(
                      child: Loader(),
                    );
                  } else if (!snapshot.hasData) {
                    print('Snapshot.data is empty!');
                    return Center(
                      child: Loader(),
                    );
                  } else {
                    return Container(
                      child: _reviewGridGenerator(snapshot.data),
                    );
                  }
                } else {
                  return Center(
                    child: Loader(),
                  );
                }
              },
            ),
            Global.fcmShared,
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

  GridView _reviewGridGenerator(List<ReviewData> data) {
    return GridView.builder(
      physics: ScrollPhysics(),
      scrollDirection: Axis.vertical,
      shrinkWrap: true,
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
      ),
      padding: EdgeInsets.all(2.0),
      itemBuilder: (BuildContext context, int index) {
        return _reviewTile(data[index]);
      },
      itemCount: data.length,
    );
  }

  GridTile _reviewTile(ReviewData data) {
    return GridTile(
      child: InkWell(
        onTap: () {
          showDialog(
              context: context,
              builder: (BuildContext context) {
                return AlertDialog(
                  title: Text('Tapped Photo'),
                  content: Text(
                      'Tile with photo id ${data.photoData.id} tapped! Would you like to classify this image?'),
                  actions: [
                    FlatButton(
                      child: Text("Reclassify"),
                      onPressed: () {
                        Navigator.of(context).pushAndRemoveUntil(
                          MaterialPageRoute(
                            builder: (context) => ReclassifyDetailScreen(
                              imgData: data.photoData,
                              classData: null,
                            ),
                          ),
                          (Route<dynamic> route) => false,
                        );
                      },
                    ),
                    FlatButton(
                      child: Text("Cancel"),
                      onPressed: () {
                        Navigator.of(context).pop();
                      },
                    )
                  ],
                );
              });
        },
        child: Padding(
          padding: EdgeInsets.all(8),
          child: Container(
            decoration: BoxDecoration(
              borderRadius: BorderRadius.all(Radius.circular(6)),
              color: Colors.grey[100],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Container(
                  child: Image.network(
                    data.photoData.fileUrl,
                    fit: BoxFit.contain,
                  ),
                ),
                Container(
                  child: Text(
                    'Submitted On: ${data.photoData.dateTaken}',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 10,
                      color: Colors.black,
                    ),
                  ),
                ),
                Container(
                  child: Text(
                    'Classification: ${data.classification.species}',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                      color: Colors.black,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
