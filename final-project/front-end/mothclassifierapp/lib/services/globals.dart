import 'package:flutter/material.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import 'package:firebase_analytics/firebase_analytics.dart';
import '../shared/shared.dart';
import 'services.dart';

class Global {
  /// Application Title
  static final String title = 'DiscoverLife Moth Classifier';

  /// Shared FirebaseAnalytics object for Analytics and Crashlytics
  static final FirebaseAnalytics analytics = FirebaseAnalytics();

  /// api base URL for pre-integration testing, uses JSONApi
  static final String apiUrl = "http://10.0.2.2:3000";

  /// api base URL for integrated testing, uses MothClassifierAPI
  static final String mothApiBase = "https://mothclassifier.org/api/v1";

  /// Global variables for tracking user state
  static UserApiObj currApiData;
  static UserDataClass currUserData;
  static String deviceToken;
  static Device device;
  static bool hasInitMessaging = false;

  /// Shared [ApiService] for making calls to the MothClassifierAPI
  static ApiService apiService = ApiService();

  /// Shared [MessagingWidget] to support digestion of notifications on all screens
  static MessagingWidget fcmShared = MessagingWidget();

  /// Initializes Global [UserApiObj] and [UserDataClass] using signed in [LitUser]
  ///
  /// Populates the two objects using API calls handled by the [ApiService]
  static Future<void> initUserObjects(LitUser user) async {
    currApiData = await apiService.getApiRefFromUser(user);
    currUserData = await apiService.getUserDataFromApiRef(currApiData);

    return;
  }

  /// Updates global [UserDataClass]
  ///
  /// Should be called in response to changing of a user's profile information.
  /// This essentially 'refreshes' the global User state
  static Future<void> updateCurrentUser() async {
    currUserData = await apiService.getUserDataFromApiRef(currApiData);
    return;
  }

  static Future<void> refreshAuthToken(BuildContext context) async {
    currApiData = await apiService.getApiRefFromUser(context.getSignedInUser());
    return;
  }

  /// Signs out user signed in under [context]
  ///
  /// Uses the [context.signOut] from LitAuth to sign out current user.
  /// Also, clears global state for [currApiData], [currUserData], and [deviceToken]
  static Future<void> signOut(BuildContext context) async {
    await context.signOut();
    await apiService.toggleActiveTokenForSignedInUser(
        device.id, deviceToken, "false");
    currApiData = null;
    currUserData = null;
    hasInitMessaging = false;
    deviceToken = null;
    device = null;
    return;
  }
}
