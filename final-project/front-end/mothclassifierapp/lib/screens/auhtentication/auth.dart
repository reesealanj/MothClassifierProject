import 'package:animations/animations.dart';
import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import '../../shared/shared.dart';
import '../screens.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({Key key}) : super(key: key);

  static MaterialPageRoute get route => MaterialPageRoute(
        builder: (context) => const AuthScreen(),
      );
  @override
  _AuthScreenState createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen>
    with SingleTickerProviderStateMixin {
  AnimationController _controller;

  ValueNotifier<bool> showSignInPage = ValueNotifier<bool>(true);
  @override
  void initState() {
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );
    super.initState();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: LitAuth.custom(
        errorNotification: const NotificationConfig(
          backgroundColor: PainterPalette.dBlue,
          icon: Icon(
            Icons.error_outline,
            color: Colors.deepOrange,
            size: 32,
          ),
        ),
        onAuthFailure: (failure) {
          print(failure);
        },
        onAuthSuccess: () async {
          //await Global.initUserObjects(context.getSignedInUser());
          Navigator.of(context).pushReplacement(HomeScreen.route);
        },
        child: Stack(
          children: [
            SizedBox.expand(
              child: CustomPaint(
                painter: BackgroundPainter(
                  animation: _controller.view,
                ),
              ),
            ),
            Center(
              child: ConstrainedBox(
                constraints: BoxConstraints(maxWidth: 800),
                child: ValueListenableBuilder<bool>(
                  valueListenable: showSignInPage,
                  builder: (context, value, child) {
                    return PageTransitionSwitcher(
                      duration: Duration(milliseconds: 800),
                      reverse: !value,
                      transitionBuilder:
                          (child, animation, secondaryAnimation) {
                        return SharedAxisTransition(
                          animation: animation,
                          secondaryAnimation: secondaryAnimation,
                          transitionType: SharedAxisTransitionType.vertical,
                          child: child,
                          fillColor: Colors.transparent,
                        );
                      },
                      child: value
                          ? SignIn(
                              key: ValueKey('SignIn'),
                              onRegisterClicked: () {
                                context.resetSignInForm();
                                showSignInPage.value = false;
                                _controller.forward();
                              },
                            )
                          : Register(
                              key: ValueKey('Register'),
                              onSignInPressed: () {
                                context.resetSignInForm();
                                showSignInPage.value = true;
                                _controller.reverse();
                              },
                            ),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
