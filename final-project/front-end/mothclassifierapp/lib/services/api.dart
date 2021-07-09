import 'dart:convert';
import 'dart:io';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:mime/mime.dart';
import 'models.dart';
import 'globals.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:lit_firebase_auth/lit_firebase_auth.dart';
import 'custom_exceptions.dart';

class ApiService {
  // Get list of Classifications needing Review
  // ignore: missing_return
  Future<List<Classification>> fetchReviewClassifications() async {
    String url = '${Global.apiUrl}/classifications/?needs_review=true';
    await http.get(url).then((res) {
      if (res.statusCode == 200) {
        List<Classification> list = Classification.listFromJsonArray(res.body);
        return list;
      } else {
        throw new Exception('Error fetching needs_review Classifications');
      }
    });
  }

  // Get list of ReviewData objects for classifications needing review
  Future<List<ReviewData>> fetchNeedsReviewObjects({int page = 1}) async {
    List<ReviewData> outputList = new List<ReviewData>();
    String classUrl =
        '${Global.mothApiBase}/classifications/?needs_review=true';
    final response = await http.get(classUrl);
    if (response.statusCode == 200) {
      final json = jsonDecode(response.body);
      List<Classification> classList =
          Classification.listFromJsonArray(jsonEncode(json['results']));
      for (var i = 0; i < classList.length; i++) {
        String imgUrl = classList[i].imgUrl;
        PhotoData imgObj = await photoFromUrl(imgUrl);
        ReviewData toAdd =
            new ReviewData(classification: classList[i], photoData: imgObj);
        outputList.add(toAdd);
      }

      return outputList;
    } else {
      throw new Exception('Error fetching needs_review Classifications');
    }
  }

  // Get list of Images bound to one user
  Future<List<PhotoData>> fetchUserImages() async {
    String url =
        '${Global.mothApiBase}/users/${Global.currApiData.uid}/images/';
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer ${Global.currApiData.token}',
      },
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> json = jsonDecode(response.body);
      List<PhotoData> photos =
          PhotoData.listFromJsonArray(jsonEncode(json['results']));
      return photos;
    } else {
      throw new ApiException(message: response.body);
    }
  }

  Future<Map> getUserSubmissions({int page = 1}) async {
    String url =
        '${Global.mothApiBase}/users/${Global.currApiData.uid}/images/?page=$page';

    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer ${Global.currApiData.token}'},
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> json = jsonDecode(response.body);
      List submissions = json['results'];
      bool hasMore = (json['next'] != null) ? true : false;

      return {
        'results': submissions,
        'hasMore': hasMore,
      };
    } else {
      return {
        'hasMore': false,
      };
    }
  }

  Future<Map> getNeedReview({int page = 1}) async {
    String url =
        '${Global.mothApiBase}/classifications/?needs_review=true&page=$page';

    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer ${Global.currApiData.token}'},
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> json = jsonDecode(response.body);
      List reclassifications = json['results'];
      bool hasMore = (json['next'] != null) ? true : false;

      return {
        'results': reclassifications,
        'hasMore': hasMore,
      };
    } else {
      return {
        'hasMore': false,
      };
    }
  }

  // Get individual PhotoData object when given url from classification
  Future<PhotoData> photoFromUrl(String url) async {
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer ${Global.currApiData.token}'},
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> imgJson = json.decode(response.body);
      PhotoData imgObj = PhotoData.fromJson(imgJson);
      return imgObj;
    } else {
      throw new Exception('Error fetching image object from $url');
    }
  }

  Future<Classification> classificationFromUrl(String url) async {
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer ${Global.currApiData.token}'},
    );
    if (response.statusCode == 200) {
      Map classJson = json.decode(response.body);
      Classification classObj = Classification.fromJson(classJson);
      return classObj;
    } else {
      throw new Exception('Error fetching classification object from $url');
    }
  }

  Future<bool> updateClassification(String classification, int imgId) async {
    String url = '${Global.mothApiBase}/images/$imgId/classification/';

    final response = await http.patch(
      url,
      headers: {
        'Authorization': 'Bearer ${Global.currApiData.token}',
      },
      body: {
        'is_automated': 'false',
        'needs_review': 'false',
        'accuracy': "100.000",
        'species': classification
      },
    );

    Map json = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return true;
    } else if (response.statusCode == 401) {
      if (json["detail"] == "Token is invalid.") {
        throw new InvalidTokenException();
      }
    } else {
      throw new ApiException(message: json["detail"]);
    }
  }

  /// Get [FirebaseAuth.User] object from a [LitUser] auth object
  Future<User> getUserFromLitUser(LitUser user) async {
    User output;

    user.when(
      (user) => output = user,
      empty: () {},
      initializing: () {},
    );

    return output;
  }

  /// Get [UserApiObj] with auth data from [LitUser] auth object
  Future<UserApiObj> getApiRefFromUser(LitUser user) async {
    User fbuser = await getUserFromLitUser(user);

    String token = await fbuser.getIdToken();
    String uid = fbuser.uid;

    UserApiObj output = new UserApiObj(token: token, uid: uid);
    return output;
  }

  /// Creates [UserDataClass] using API connection information in [UserApiObj]
  ///
  /// Submits a request to the moth classifier API to get a User's stored data
  // ignore: missing_return
  Future<UserDataClass> getUserDataFromApiRef(UserApiObj apiInfo) async {
    String url = '${Global.mothApiBase}/users/${apiInfo.uid}';
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer ${apiInfo.token}',
      },
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> json = jsonDecode(response.body);
      UserDataClass output = UserDataClass.fromJson(json);
      return output;
    } else if (response.statusCode == 401) {
      Map<String, dynamic> json = jsonDecode(response.body);
      if (json["detail"] == "Token is invalid.") {
        throw InvalidTokenException;
      }
    } else {
      return null;
    }
  }

  // ignore: missing_return
  Future<bool> updateUserProfile(String firstName, String lastName) async {
    String url = '${Global.mothApiBase}/users/${Global.currApiData.uid}/';

    final response = await http.patch(
      url,
      headers: {
        'Authorization': 'Bearer ${Global.currApiData.token}',
      },
      body: {
        "first_name": firstName,
        "last_name": lastName,
      },
    );
    Map<String, dynamic> json = jsonDecode(response.body);

    if (response.statusCode == 200) {
      return true;
    } else if (response.statusCode == 401) {
      if (json["detail"] == "Token is invalid.") {
        throw new InvalidTokenException();
      }
    } else {
      throw new ApiException(message: json["detail"]);
    }
  }

  /// Submits [file] to MothClassifier API using [Global.currApiData]
  ///
  /// Submits the file to the currently signed in account.
  /// Returns [PhotoData] object containing submission information.
  Future<PhotoData> submitImageForSignedInUser(
      File file, String fileName) async {
    String url =
        '${Global.mothApiBase}/users/${Global.currApiData.uid}/images/';
    var request = http.MultipartRequest('POST', Uri.parse(url));

    Map<String, String> headers = {
      'Authorization': 'Bearer ${Global.currApiData.token}',
      'Content-type': 'multipart/form-data'
    };

    var fileContentType = lookupMimeType(file.path);
    var contentTypeArr = fileContentType.split("/");
    request.files.add(http.MultipartFile(
      'file',
      file.readAsBytes().asStream(),
      file.lengthSync(),
      filename: fileName,
      contentType: MediaType(contentTypeArr[0], contentTypeArr[1]),
    ));

    request.headers.addAll(headers);

    final response = await request.send();

    var unstreamResponse = await http.Response.fromStream(response);
    Map<String, dynamic> json = jsonDecode(unstreamResponse.body);

    if (response.statusCode == 201) {
      return PhotoData.fromJson(json);
    } else if (response.statusCode == 401) {
      if (json['detail'] == "Token is invalid.") {
        throw new InvalidTokenException();
      } else {
        throw new ApiException(message: json['detail']);
      }
    } else {
      throw new ApiException(message: jsonEncode(json));
    }
  }

  /// Get list of [String] with FCM Tokens registered to signed in User
  Future<List<Device>> getSignedInUserDevices() async {
    String url =
        '${Global.mothApiBase}/users/${Global.currApiData.uid}/devices/';

    final request = http.Request('GET', Uri.parse(url));

    Map<String, String> headers = {
      'Authorization': 'Bearer ${Global.currApiData.token}',
      'Content-type': 'application/json'
    };

    request.headers.addAll(headers);
    request.body = jsonEncode({"page_size": 100});

    final streamRes = await request.send();
    final response = await http.Response.fromStream(streamRes);
    Map<String, dynamic> json = jsonDecode(response.body);

    if (response.statusCode == 200) {
      List<Device> devices =
          Device.listFromJsonArray(jsonEncode(json['results']));

      return devices;
    } else if (response.statusCode == 401) {
      if (json['detail'] == "Token is invalid.") {
        throw new InvalidTokenException();
      } else {
        throw new ApiException(message: json['detail']);
      }
    } else {
      throw new ApiException(message: json.toString());
    }
  }

  Future<Device> registerTokenForSignedInUser(String token) async {
    String url =
        '${Global.mothApiBase}/users/${Global.currApiData.uid}/devices/';

    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer ${Global.currApiData.token}',
      },
      body: {
        "registration_id": token,
        "type": Platform.isAndroid ? "android" : "ios",
      },
    );

    Map<String, dynamic> json = jsonDecode(response.body);
    if (response.statusCode == 201) {
      return Device.fromJson(json);
    } else if (response.statusCode == 401) {
      if (json['detail'] == "Token is invalid.") {
        throw new InvalidTokenException();
      } else {
        throw new ApiException(message: json['detail']);
      }
    } else {
      throw new ApiException(message: json.toString());
    }
  }

  Future<Device> toggleActiveTokenForSignedInUser(
      int id, String token, String active) async {
    String url = '${Global.mothApiBase}/devices/$id/';

    final response = await http.patch(
      url,
      headers: {
        'Authorization': 'Bearer ${Global.currApiData.token}',
      },
      body: {
        "registration_id": token,
        "active": active,
      },
    );

    Map<String, dynamic> json = jsonDecode(response.body);
    if (response.statusCode == 200) {
      return Device.fromJson(json);
    } else if (response.statusCode == 401) {
      if (json['detail'] == "Token is invalid.") {
        throw new InvalidTokenException();
      } else {
        throw new ApiException(message: json['detail']);
      }
    } else {
      throw new ApiException(message: json.toString());
    }
  }

  Future<void> startClassifyJobSignedInUser(int id) async {
    String url = '${Global.mothApiBase}/images/$id/jobs/';
    Map<String, String> headers = {
      'Authorization': 'Bearer ${Global.currApiData.token}',
      'Content-type': 'application/json'
    };

    var request = http.Request('POST', Uri.parse(url));
    request.headers.addAll(headers);
    request.body = jsonEncode({"job_type": "classify"});

    final streamRes = await request.send();
    final response = await http.Response.fromStream(streamRes);
    Map<String, dynamic> json = jsonDecode(response.body);

    if (response.statusCode == 201) {
      return;
    } else if (response.statusCode == 401) {
      if (json['detail'] == "Token is invalid.") {
        throw new InvalidTokenException();
      } else {
        throw new ApiException(message: json['detail']);
      }
    } else {
      throw new ApiException(message: json.toString());
    }
  }
}
