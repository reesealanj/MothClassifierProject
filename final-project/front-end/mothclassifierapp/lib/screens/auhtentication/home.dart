import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import 'package:mothclassifierapp/screens/reclassify/reclassify_redo.dart';
import '../../shared/shared.dart';
import '../../services/services.dart';
import '../screens.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const HomeScreen(),
      );

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('DiscoverLife Moth Classifier'),
      ),
      body: Container(
        padding: EdgeInsets.symmetric(vertical: 20.0, horizontal: 2.0),
        child: FutureBuilder<List<Widget>>(
          future: genDashAndCreateGlobalUser(),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return GridView.builder(
                itemCount: snapshot.data.length,
                physics: ScrollPhysics(),
                scrollDirection: Axis.vertical,
                shrinkWrap: true,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                ),
                itemBuilder: (context, index) {
                  return snapshot.data[index];
                },
              );
            } else if (snapshot.hasError) {
              return Column(
                children: <Widget>[
                  Center(
                    child: Card(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(25.0),
                      ),
                      elevation: 1.0,
                      margin: new EdgeInsets.all(8.0),
                      child: Container(
                        decoration: BoxDecoration(
                          color: PainterPalette.dBlue,
                          borderRadius: BorderRadius.circular(25.0),
                        ),
                        child: InkWell(
                          onTap: () {
                            setState(() {});
                          },
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            mainAxisSize: MainAxisSize.min,
                            verticalDirection: VerticalDirection.down,
                            children: <Widget>[
                              SizedBox(height: 40.0),
                              Center(
                                child: Image.asset(
                                  'assets/icons/about_icon.png',
                                  height: 80.0,
                                  width: 80.0,
                                ),
                              ),
                              SizedBox(height: 20.0),
                              Center(
                                child: Text(
                                  'A loading error occurred,\n tap to retry!',
                                  style: new TextStyle(
                                    fontSize: 24,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                              SizedBox(height: 20.0),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                  Center(
                    child: Card(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(25.0),
                      ),
                      elevation: 1.0,
                      margin: new EdgeInsets.all(8.0),
                      child: Container(
                        decoration: BoxDecoration(
                          color: PainterPalette.dBlue,
                          borderRadius: BorderRadius.circular(25.0),
                        ),
                        child: InkWell(
                          onTap: () {
                            context.signOut();
                            Navigator.of(context)
                                .pushReplacement(AuthScreen.route);
                          },
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            mainAxisSize: MainAxisSize.min,
                            verticalDirection: VerticalDirection.down,
                            children: <Widget>[
                              SizedBox(height: 40.0),
                              Center(
                                child: Image.asset(
                                  'assets/icons/sign_out_icon.png',
                                  height: 80.0,
                                  width: 80.0,
                                ),
                              ),
                              SizedBox(height: 20.0),
                              Center(
                                child: Text(
                                  'Sign Out',
                                  style: new TextStyle(
                                    fontSize: 24,
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                              SizedBox(height: 20.0),
                            ],
                          ),
                        ),
                      ),
                    ),
                  )
                ],
              );
            } else {
              return Center(
                child: Loader(),
              );
            }
          },
        ),
      ),
    );
  }

  Future<List<Widget>> genDashAndCreateGlobalUser() async {
    if (Global.currApiData == null) {
      await Global.initUserObjects(context.getSignedInUser());
      List<Widget> output =
          await generateDashboard(Global.currUserData.isResearcher);
      return output;
    } else {
      return await generateDashboard(Global.currUserData.isResearcher);
    }
  }

  Future<List<Widget>> generateDashboard(bool isResearcher) async {
    List<Widget> output = new List<Widget>();

    if (isResearcher) {
      output.add(
        generateDashboardItem(
          "Reclassify",
          'assets/icons/reclassify_icon.png',
          Colors.white,
          PainterPalette.dBlue,
          ReclassificationsPageTwo.route,
          'reclassify',
        ),
      );
    }
    output.add(
      generateDashboardItem(
        "Submit",
        'assets/icons/send_icon.png',
        Colors.white,
        PainterPalette.dBlue,
        SubmitScreen.route,
        'submit',
      ),
    );
    output.add(
      generateDashboardItem(
        "Submissions",
        'assets/icons/submissions_icon.png',
        Colors.white,
        PainterPalette.dBlue,
        SubmissionsPageTwo.route,
        'userSubmissions',
      ),
    );

    output.add(
      generateDashboardItem(
        "About",
        'assets/icons/about_icon.png',
        Colors.white,
        PainterPalette.dBlue,
        AboutScreen.route,
        'about',
      ),
    );
    output.add(
      generateDashboardItem(
        "Profile",
        'assets/icons/profile_icon.png',
        Colors.white,
        PainterPalette.dBlue,
        ProfileScreen.route,
        'profile',
      ),
    );
    output.add(
      generateDashboardItem(
        "Sign Out",
        'assets/icons/sign_out_icon.png',
        Colors.white,
        PainterPalette.dBlue,
        AuthScreen.route,
        'sign-out',
      ),
    );

    if (kDebugMode) {
      output.add(
        Card(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(25.0),
          ),
          elevation: 1.0,
          margin: new EdgeInsets.all(8.0),
          child: Container(
            decoration: BoxDecoration(
              color: PainterPalette.dBlue,
              borderRadius: BorderRadius.circular(25.0),
            ),
            child: InkWell(
              onTap: () {
                print('Auth Token: ${Global.currApiData.token}');
                print('UID: ${Global.currApiData.uid}');
                print('Device Token: ${Global.deviceToken}');
              },
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                mainAxisSize: MainAxisSize.min,
                verticalDirection: VerticalDirection.down,
                children: <Widget>[
                  SizedBox(height: 40.0),
                  Center(
                    child: Image.asset(
                      'assets/icons/debug_icon.png',
                      height: 80.0,
                      width: 80.0,
                    ),
                  ),
                  SizedBox(height: 20.0),
                  Center(
                    child: Text(
                      'Debug Info',
                      style: new TextStyle(
                        fontSize: 24,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      );
      output.add(
        Card(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(25.0),
          ),
          elevation: 1.0,
          margin: new EdgeInsets.all(8.0),
          child: Container(
            decoration: BoxDecoration(
              color: PainterPalette.dBlue,
              borderRadius: BorderRadius.circular(25.0),
            ),
            child: InkWell(
              onTap: () async {
                print('Attempting Refresh Auth Token');
                String currTok = Global.currApiData.token;
                await Global.refreshAuthToken(context);

                if (currTok == Global.currApiData.token) {
                  print('Token Not Updated: Current Token not Expired');
                } else {
                  print('Token Updated: Old Token Expired');
                }
              },
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                mainAxisSize: MainAxisSize.min,
                verticalDirection: VerticalDirection.down,
                children: <Widget>[
                  SizedBox(height: 40.0),
                  Center(
                    child: Image.asset(
                      'assets/icons/debug_icon.png',
                      height: 80.0,
                      width: 80.0,
                    ),
                  ),
                  SizedBox(height: 20.0),
                  Center(
                    child: Text(
                      'Refresh Auth',
                      style: new TextStyle(
                        fontSize: 24,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
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

    output.add(Global.fcmShared);
    return output;
  }

  Card generateDashboardItem(
    String title,
    String image,
    Color textColor,
    Color bgColor,
    MaterialPageRoute route,
    String routeObjective,
  ) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(25.0),
      ),
      elevation: 1.0,
      margin: new EdgeInsets.all(8.0),
      child: Container(
        decoration: BoxDecoration(
          color: bgColor,
          borderRadius: BorderRadius.circular(25.0),
        ),
        child: InkWell(
          onTap: () {
            switch (routeObjective) {
              case 'home':
                return;
              case 'sign-out':
                Global.signOut(context);
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  Navigator.pushAndRemoveUntil(
                    context,
                    route,
                    (Route<dynamic> route1) => false,
                  );
                });

                return;
              default:
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  Navigator.of(context).pushReplacement(route);
                });
                return;
            }
          },
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            mainAxisSize: MainAxisSize.min,
            verticalDirection: VerticalDirection.down,
            children: <Widget>[
              SizedBox(height: 40.0),
              Center(
                child: Image.asset(
                  image,
                  height: 80.0,
                  width: 80.0,
                ),
              ),
              SizedBox(height: 20.0),
              Center(
                child: Text(
                  title,
                  style: new TextStyle(
                    fontSize: 24,
                    color: textColor,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
