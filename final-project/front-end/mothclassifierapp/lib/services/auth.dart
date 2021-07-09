import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:apple_sign_in/apple_sign_in.dart';
import 'custom_exceptions.dart';
import 'dart:async';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  final GoogleSignIn _gSignIn = GoogleSignIn();

  // Stream which updates when there is a change to the current authState
  Stream<User> get user => _auth.authStateChanges();

  // Fn which returns current authenticated user or null if none logged in
  Future<User> currentUser() async {
    User curr = _auth.currentUser;
    if (curr != null) {
      return curr;
    } else {
      return null;
    }
  }

  // Future which can be resolved to decide if appleSignIn is available
  Future<bool> get appleSignInAvailable => AppleSignIn.isAvailable();

  Future<User> anonymousLogin() async {
    UserCredential credential = await _auth.signInAnonymously();
    User user = credential.user;
    return user;
  }

  Future<User> googleSignIn() async {
    GoogleSignInAccount googleUser = await _gSignIn.signIn();
    GoogleSignInAuthentication googleAuth = await googleUser.authentication;
    GoogleAuthCredential googleCredential = GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );

    UserCredential credential =
        await _auth.signInWithCredential(googleCredential);
    User user = credential.user;
    return user;
  }

  Future<User> appleSignIn() async {
    try {
      final AppleIdRequest req =
          AppleIdRequest(requestedScopes: [Scope.email, Scope.fullName]);
      final AuthorizationResult appleRes =
          await AppleSignIn.performRequests([req]);

      if (appleRes.error != null) {
        throw new LoginException(appleRes.error.localizedFailureReason);
      }

      final AuthCredential cred = OAuthProvider(
        'apple.com',
      ).credential(
        accessToken:
            String.fromCharCodes(appleRes.credential.authorizationCode),
        idToken: String.fromCharCodes(appleRes.credential.identityToken),
      );

      UserCredential firebaseRes = await _auth.signInWithCredential(cred);
      User user = firebaseRes.user;
      return user;
    } catch (e) {
      throw new LoginException(e.message);
    }
  }

  // ignore: missing_return
  Future<User> emailSignIn(String email, String password) async {
    try {
      UserCredential credential = await _auth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      User user = credential.user;
      return user;
    } on FirebaseAuthException catch (e) {
      if (e.code == 'user-not-found') {
        throw new LoginException('An account does not exist for that email');
      } else if (e.code == 'wrong-password') {
        throw new LoginException('Incorrect password');
      }
    } catch (e) {
      throw new LoginException(e.message);
    }
  }

  // ignore: missing_return
  Future<User> emailRegister(String email, String password) async {
    try {
      UserCredential credential = await _auth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      User user = credential.user;
      return user;
    } on FirebaseAuthException catch (e) {
      if (e.code == 'weak-password') {
        throw new LoginException('Inputted Password is too weak!');
      } else if (e.code == 'email-already-in-use') {
        throw new LoginException('That email is already registered!');
      }
    } catch (e) {
      throw new LoginException(e.message);
    }
  }

  Future<void> signOut() async {
    await _auth.signOut();
  }
}
