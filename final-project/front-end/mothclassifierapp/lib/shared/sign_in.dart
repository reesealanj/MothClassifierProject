import 'dart:io';

import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import 'package:mothclassifierapp/shared/decoration_functions.dart';
import 'shared.dart';

class SignIn extends StatelessWidget {
  const SignIn({
    Key key,
    @required this.onRegisterClicked,
  }) : super(key: key);

  final VoidCallback onRegisterClicked;
  @override
  Widget build(BuildContext context) {
    final isSubmitting = context.isSubmitting();
    final appleSignInAvailable = Platform.isIOS;
    return SignInForm(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          children: [
            Expanded(
              flex: 3,
              child: Align(
                alignment: Alignment.centerLeft,
                child: LoginTitle(
                  title: 'Welcome\nBack',
                ),
              ),
            ),
            Expanded(
              flex: 4,
              child: ListView(
                children: [
                  Padding(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    child: EmailTextFormField(
                      decoration: signInInputDecoration(hintText: 'Email'),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    child: PasswordTextFormField(
                      decoration: signInInputDecoration(hintText: 'Password'),
                    ),
                  ),
                  SignInBar(
                    isLoading: isSubmitting,
                    label: 'Sign In',
                    onPressed: () {
                      context.signInWithEmailAndPassword();
                    },
                  ),
                ],
              ),
            ),
            Expanded(
              flex: 2,
              child: Align(
                alignment: Alignment.bottomCenter,
                child: Column(
                  children: [
                    const Text(
                      "or sign in with",
                      style: TextStyle(
                        color: Colors.black54,
                      ),
                    ),
                    const SizedBox(
                      height: 24.0,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        ProviderButton(
                          context: context,
                          signInType: "google",
                        ),
                        if (appleSignInAvailable)
                          ProviderButton(
                            context: context,
                            signInType: "apple",
                          ),
                      ],
                    ),
                    const Spacer(),
                    InkWell(
                      splashColor: Colors.white,
                      onTap: () {
                        onRegisterClicked?.call();
                      },
                      child: RichText(
                        text: const TextSpan(
                          text: "Don't have an account? ",
                          style: TextStyle(color: Colors.black54),
                          children: <TextSpan>[
                            TextSpan(
                              text: 'SIGN UP',
                              style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                  color: Colors.black),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
