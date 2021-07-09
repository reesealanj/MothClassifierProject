import 'package:flutter/material.dart';
import '../../shared/shared.dart';
import '../../services/services.dart';
import '../screens.dart';

class ProfileInformationEditScreen extends StatefulWidget {
  const ProfileInformationEditScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const ProfileInformationEditScreen(),
      );

  @override
  _ProfileInformationEditScreenState createState() =>
      _ProfileInformationEditScreenState();
}

final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

class _ProfileInformationEditScreenState
    extends State<ProfileInformationEditScreen> {
  String _firstName;
  String _lastName;
  bool _loaderVisible = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit Profile'),
      ),
      body: Container(
        margin: EdgeInsets.all(20),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              _loaderVisible ? Container() : _buildChangeForm(),
              _loaderVisible ? Loader() : Container(),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.keyboard_backspace_rounded),
        backgroundColor: PainterPalette.lBlue,
        onPressed: () {
          Navigator.of(context).pushReplacement(ProfileScreen.route);
        },
      ),
    );
  }

  /// Creates a [Widget] with a [Form] which has fields to edit
  Widget _buildChangeForm() {
    return Form(
      key: _formKey,
      child: Column(
        children: <Widget>[
          TextFormField(
            initialValue: Global.currUserData.firstName,
            decoration: InputDecoration(labelText: 'First Name'),
            validator: (String value) {
              return (value.isEmpty) ? 'First Name can not be empty!' : null;
            },
            onChanged: (String value) {
              setState(() {
                _firstName = value;
              });
            },
            onSaved: (String value) {
              _firstName = value;
            },
          ),
          TextFormField(
            initialValue: Global.currUserData.lastName,
            decoration: InputDecoration(labelText: 'Last Name'),
            validator: (String value) {
              return (value.isEmpty) ? 'Last Name can not be empty!' : null;
            },
            onSaved: (String value) {
              _lastName = value;
            },
            onChanged: (String value) {
              setState(() {
                _lastName = value;
              });
            },
          ),
          SizedBox(height: 20),
          RaisedButton(
            child: Text(
              'Save Changes',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            onPressed: () {
              if (!_formKey.currentState.validate()) {
                print(_formKey.currentState.validate());
                print(_formKey.currentState.toString());
                return;
              } else {
                _formKey.currentState.save();
                _saveChangesAndUpdate();
              }
            },
          ),
        ],
      ),
    );
  }

  void _saveChangesAndUpdate() async {
    setState(() {
      _loaderVisible = true;
    });
    try {
      bool saved =
          await Global.apiService.updateUserProfile(_firstName, _lastName);

      if (saved) {
        await Global.updateCurrentUser();
        Navigator.of(context).pushReplacement(ProfileScreen.route);
      }
    } on InvalidTokenException catch (e) {
      await Global.refreshAuthToken(context);
      _saveChangesAndUpdate();
    } catch (e) {
      print(e.message);
    }
  }
}
