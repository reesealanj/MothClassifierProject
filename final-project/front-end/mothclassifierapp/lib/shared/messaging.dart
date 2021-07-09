import 'package:flutter/material.dart';

import 'dart:async';
import 'dart:io';

import 'package:firebase_messaging/firebase_messaging.dart';
import '../services/services.dart';

class MessagingWidget extends StatefulWidget {
  const MessagingWidget({Key key, this.child}) : super(key: key);

  final Widget child;
  @override
  _MessagingWidgetState createState() => _MessagingWidgetState();
}

class _MessagingWidgetState extends State<MessagingWidget> {
  final FirebaseMessaging _fcm = FirebaseMessaging();

  String deviceToken;
  StreamSubscription iosSubscription;

  @override
  void initState() {
    super.initState();

    if (Platform.isIOS) {
      iosSubscription = _fcm.onIosSettingsRegistered.listen((data) {
        if (Global.deviceToken == null) {
          _saveDeviceToken();
        }
      });

      _fcm.requestNotificationPermissions(IosNotificationSettings());
    } else {
      if (Global.deviceToken == null) {
        _saveDeviceToken();
      }
    }

    _fcm.configure(
      // runs when app is open and running in the foreground and a message is recieved
      onMessage: (Map<String, dynamic> message) async {
        print('onMessage: $message');
        _alertNotification(message, context);
      },
      // runs when app is closed and opened via the push notification
      onLaunch: (Map<String, dynamic> message) async {
        print('onLaunch: $message');
        _dataMessageAlert(message, context);
      },
      // runs when app is in the background and opened via push notification
      onResume: (Map<String, dynamic> message) async {
        print('onResume: $message');
        _dataMessageAlert(message, context);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: widget.child,
    );
  }

  @override
  void dispose() {
    if (iosSubscription != null) {
      iosSubscription.cancel();
    }

    super.dispose();
  }

  _alertNotification(Map<String, dynamic> mMap, BuildContext context) {
    Widget button = FlatButton(
      child: Text('Ok'),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
    NotificationObj noti = NotificationObj.fromJson(mMap);
    AlertDialog alert = AlertDialog(
      title: Text(noti.title),
      content: Text(noti.body),
      actions: [
        button,
      ],
    );

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return alert;
      },
    );
  }

  _snackbarNotification(Map<String, dynamic> mMap) {
    NotificationObj noti = NotificationObj.fromJson(mMap);
    final snackbar = SnackBar(
      content: Text(noti.title),
      action: SnackBarAction(
        label: 'Ok!',
        onPressed: () => null,
      ),
    );

    Scaffold.of(context).showSnackBar(snackbar);
  }

  _dataMessageAlert(Map<String, dynamic> dMap, BuildContext context) {
    Widget button = FlatButton(
      child: Text('Ok'),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
    NotificationObj noti = NotificationObj.fromJson(dMap);
    AlertDialog alert = AlertDialog(
      title: Text(noti.dataTitle),
      content: Text(noti.dataBody),
      actions: [
        button,
      ],
    );

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return alert;
      },
    );
  }

  _saveDeviceToken() async {
    deviceToken = await _fcm.getToken();
    Global.deviceToken = deviceToken;

    List<Device> userDevices = await Global.apiService.getSignedInUserDevices();

    for (var i = 0; i < userDevices.length; i++) {
      if (userDevices[i].registrationId == deviceToken) {
        Global.device =
            await Global.apiService.toggleActiveTokenForSignedInUser(
          userDevices[i].id,
          userDevices[i].registrationId,
          "true",
        );
        return;
      }
    }
    Global.device =
        await Global.apiService.registerTokenForSignedInUser(deviceToken);
    return;
  }
}
