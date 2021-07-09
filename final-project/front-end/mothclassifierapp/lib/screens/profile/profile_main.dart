import 'package:flutter/material.dart';
import '../../shared/shared.dart';
import '../../services/services.dart';
import '../screens.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const ProfileScreen(),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Center(
                  child: Image.asset(
                    'assets/icons/profile_icon.png',
                    height: 80.0,
                    width: 80.0,
                  ),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Column(
                  children: [
                    Text(
                      'Name: ',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 18,
                      ),
                    ),
                  ],
                ),
                Column(
                  children: [
                    Text(
                      '${Global.currUserData.firstName} ${Global.currUserData.lastName}',
                      style: TextStyle(
                        fontSize: 18,
                      ),
                    )
                  ],
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Column(children: [
                  Text(
                    'Email: ',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  )
                ]),
                Column(
                  children: [
                    Text(
                      Global.currUserData.email,
                      style: TextStyle(
                        fontSize: 18,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Column(
                  children: [
                    Text(
                      'Researcher Status: ',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 18,
                      ),
                    )
                  ],
                ),
                Column(
                  children: [
                    Global.currUserData.isResearcher
                        ? Text(
                            'Active',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.green,
                            ),
                          )
                        : Text(
                            'Not Researcher',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.red,
                            ),
                          ),
                  ],
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Column(
                  children: [
                    Text(
                      'Staff Status: ',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 18,
                      ),
                    )
                  ],
                ),
                Column(
                  children: [
                    Global.currUserData.isStaff
                        ? Text(
                            'Active',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.green,
                            ),
                          )
                        : Text(
                            'Not Staff',
                            style: TextStyle(
                              fontSize: 18,
                              color: Colors.red,
                            ),
                          ),
                  ],
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                RaisedButton(
                  onPressed: () {
                    Navigator.of(context)
                        .pushReplacement(ProfileInformationEditScreen.route);
                  },
                  child: const Text(
                    'Change My Information',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                )
              ],
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
}
