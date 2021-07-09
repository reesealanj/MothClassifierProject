import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../shared/shared.dart';
import '../screens.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const AboutScreen(),
      );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('About'),
      ),
      body: Column(
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
                  onTap: () => _launchURL('https://www.discoverlife.org/moth/'),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    mainAxisSize: MainAxisSize.min,
                    verticalDirection: VerticalDirection.down,
                    children: <Widget>[
                      SizedBox(height: 40.0),
                      Center(
                        child: Image.asset(
                          'assets/icons/internet_globe_icon.png',
                          height: 80.0,
                          width: 80.0,
                        ),
                      ),
                      SizedBox(height: 20.0),
                      Center(
                        child: Text(
                          'View the Project on the Web',
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
                  onTap: () => _launchURL(
                      'https://www.discoverlife.org/who/Pickering,_John.html'),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    mainAxisSize: MainAxisSize.min,
                    verticalDirection: VerticalDirection.down,
                    children: <Widget>[
                      SizedBox(height: 40.0),
                      Center(
                        child: Image.asset(
                          'assets/icons/net_icon.png',
                          height: 80.0,
                          width: 80.0,
                        ),
                      ),
                      SizedBox(height: 20.0),
                      Center(
                        child: Text(
                          'About the Founder, Dr. Pickering',
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
                  // TODO: Change this link to the github pages link for the project
                  onTap: () => _launchURL(
                      'https://github.com/gw-cs-sd/senior-design-template-f20-s21-sd-f20s21-ahmed-giangrasso-jones/'),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    mainAxisSize: MainAxisSize.min,
                    verticalDirection: VerticalDirection.down,
                    children: <Widget>[
                      SizedBox(height: 40.0),
                      Center(
                        child: Image.asset(
                          'assets/icons/program_icon.png',
                          height: 80.0,
                          width: 80.0,
                        ),
                      ),
                      SizedBox(height: 20.0),
                      Center(
                        child: Text(
                          'View Project Code',
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
          Visibility(
            child: MessagingWidget(),
            visible: true,
          ),
        ],
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

  _launchURL(url) async {
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }
}
