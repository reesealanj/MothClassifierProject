import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';

import 'decoration_functions.dart';
import 'auth_util_bar.dart';
import 'login_title.dart';

class Register extends StatelessWidget {
  const Register({
    Key key,
    this.onSignInPressed,
  }) : super(key: key);

  final VoidCallback onSignInPressed;

  @override
  Widget build(BuildContext context) {
    final isSubmitting = context.isSubmitting();
    return SignInForm(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Expanded(
              flex: 3,
              child: Align(
                alignment: Alignment.centerLeft,
                child: LoginTitle(
                  title: 'Create\nAccount',
                ),
              ),
            ),
            Expanded(
              flex: 4,
              child: ListView(
                children: [
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    child: EmailTextFormField(
                        style: const TextStyle(
                          fontSize: 18,
                          color: Colors.white,
                        ),
                        decoration: registerInputDecoration(hintText: 'Email')),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    child: PasswordTextFormField(
                      style: const TextStyle(
                        fontSize: 18,
                        color: Colors.white,
                      ),
                      decoration: registerInputDecoration(hintText: 'Password'),
                    ),
                  ),
                  SignUpBar(
                    label: 'Sign up',
                    isLoading: isSubmitting,
                    onPressed: () {
                      try {
                        context.registerWithEmailAndPassword();
                      } catch (e) {
                        print(e);
                        if (e.code == 'email-already-in-use') {
                          final snackBar = SnackBar(
                            content: Text('That email is already in use!'),
                            action: SnackBarAction(
                              label: 'Ok',
                              onPressed: () {},
                            ),
                          );

                          Scaffold.of(context).showSnackBar(snackBar);
                          print('Showed Snackbar');
                        }
                      }
                    },
                  ),
                  SizedBox(height: 40),
                  Center(
                    child: InkWell(
                      splashColor: Colors.white,
                      onTap: () {
                        onSignInPressed?.call();
                      },
                      child: RichText(
                        text: const TextSpan(
                          text: "Already have an account? ",
                          style: TextStyle(color: Colors.black54),
                          children: <TextSpan>[
                            TextSpan(
                              text: 'SIGN IN',
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
