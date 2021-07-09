import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class BottomBar extends StatelessWidget {
  final bool isResearcher;
  final int activeScreen;

  const BottomBar({this.isResearcher, this.activeScreen});

  @override
  Widget build(BuildContext context) {
    if (this.isResearcher) {
      // Generate researcher bottom navigation bar
      return BottomNavigationBar(
          type: BottomNavigationBarType.shifting,
          currentIndex: this.activeScreen,
          selectedItemColor: Colors.purpleAccent,
          items: [
            BottomNavigationBarItem(
              icon: Icon(FontAwesomeIcons.upload, size: 20),
              label: "Submit",
            ),
            BottomNavigationBarItem(
              icon: Icon(FontAwesomeIcons.search, size: 20),
              label: "Reclassify",
            ),
            BottomNavigationBarItem(
              icon: Icon(FontAwesomeIcons.bookOpen, size: 20),
              label: "About",
            ),
            BottomNavigationBarItem(
              icon: Icon(FontAwesomeIcons.exclamationCircle, size: 20),
              label: "Notifications",
            ),
            BottomNavigationBarItem(
              icon: Icon(FontAwesomeIcons.userCircle, size: 20),
              label: "Profile",
            ),
          ].toList(),
          onTap: (int index) {
            switch (index) {
              case 0:
                if (this.activeScreen != 0) {
                  Navigator.pushReplacementNamed(context, '/submit');
                }
                break;
              case 1:
                if (this.activeScreen != 1) {
                  Navigator.pushReplacementNamed(context, '/review');
                }
                break;
              case 2:
                if (this.activeScreen != 2) {
                  Navigator.pushReplacementNamed(context, '/about');
                }
                break;
              case 3:
                if (this.activeScreen != 3) {
                  Navigator.pushReplacementNamed(context, '/notifications');
                }
                break;
              case 4:
                if (this.activeScreen != 4) {
                  Navigator.pushReplacementNamed(context, '/profile');
                }
                break;
            }
          });
    } else {
      // Generate non-researcher bottom navigation bar
      int tempScreen;
      if (this.activeScreen > 0) {
        tempScreen = this.activeScreen - 1;
      }
      return BottomNavigationBar(
        type: BottomNavigationBarType.shifting,
        currentIndex: tempScreen,
        selectedItemColor: Colors.purpleAccent,
        items: [
          BottomNavigationBarItem(
            icon: Icon(FontAwesomeIcons.upload, size: 20),
            label: "Submit",
          ),
          BottomNavigationBarItem(
            icon: Icon(FontAwesomeIcons.bookOpen, size: 20),
            label: "About",
          ),
          BottomNavigationBarItem(
            icon: Icon(FontAwesomeIcons.exclamationCircle, size: 20),
            label: "Notifications",
          ),
          BottomNavigationBarItem(
            icon: Icon(FontAwesomeIcons.userCircle, size: 20),
            label: "Profile",
          ),
        ].toList(),
        onTap: (int index) {
          switch (index) {
            case 0:
              if (tempScreen != 0) {
                Navigator.pushReplacementNamed(context, '/submit');
              }
              break;
            case 1:
              if (tempScreen != 1) {
                Navigator.pushReplacementNamed(context, '/about');
              }
              break;
            case 2:
              if (tempScreen != 2) {
                Navigator.pushReplacementNamed(context, '/notifications');
              }
              break;
            case 3:
              if (tempScreen != 3) {
                Navigator.pushReplacementNamed(context, '/profile');
              }
              break;
          }
        },
      );
    }
  }
}

/**
 * Screens (researcher)
 * 0. submit
 * 1. reclassify
 * 2. about
 * 3. notifications
 * 4. profile
 * 
 * Screens (non-researcher)
 * 0. submit
 * 1. about
 * 2. notifications
 * 3. profile
 */
