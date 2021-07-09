import 'dart:convert';
import 'dart:async';
import 'globals.dart';

// Data model for Users coming from REST API
class UserDataClass {
  final int id;
  final String uid;
  final String url;
  final String email;
  final String firstName;
  final String lastName;
  final String dateJoined;
  final String lastLogin;
  final bool isResearcher;
  final bool isStaff;
  final bool isActive;
  final String images;
  final String devices;

  UserDataClass({
    this.id,
    this.uid,
    this.url,
    this.email,
    this.firstName,
    this.lastName,
    this.dateJoined,
    this.lastLogin,
    this.isResearcher,
    this.isStaff,
    this.isActive,
    this.images,
    this.devices,
  });

  factory UserDataClass.fromJson(Map<String, dynamic> json) {
    return new UserDataClass(
      id: json['id'],
      uid: json['uid'],
      url: json['url'],
      email: json['email'],
      firstName: json['first_name'],
      lastName: json['last_name'],
      dateJoined: json['date_joined'],
      lastLogin: json['last_login'],
      isResearcher: json['is_researcher'],
      isStaff: json['is_staff'],
      isActive: json['is_active'],
      images: json['images'],
      devices: json['devices'],
    );
  }
}

// Data Model for Photos coming from REST API
class PhotoData {
  final int id;
  final String url;
  final String userUrl;
  final String fileUrl;
  final String country;
  final String region;
  final String county;
  final String city;
  final int zipCode;
  final String street;
  final String dateTaken;
  final String jobsUrl;
  final String classificiation;

  PhotoData({
    this.id,
    this.url,
    this.userUrl,
    this.fileUrl,
    this.country,
    this.region,
    this.county,
    this.city,
    this.zipCode,
    this.street,
    this.dateTaken,
    this.jobsUrl,
    this.classificiation,
  });

  factory PhotoData.fromJson(Map<String, dynamic> json) {
    return new PhotoData(
      id: json['id'],
      url: json['url'],
      userUrl: json['user'],
      fileUrl: json['file'],
      country: json['country'],
      city: json['city'],
      zipCode: json['zip_code'],
      street: json['street'],
      dateTaken: json['date_taken'],
      jobsUrl: json['jobs'],
      classificiation: json['classificiation'],
    );
  }

  static List<PhotoData> listFromJsonArray(String jsonArray) {
    final parsedJson = json.decode(jsonArray).cast<Map<String, dynamic>>();
    return parsedJson
        .map<PhotoData>((json) => PhotoData.fromJson(json))
        .toList();
  }
}

// Data Model for Classifications coming from REST API
class Classification {
  final String url;
  final String imgUrl;
  final bool needsReview;
  final bool isAutomated;
  final String species;
  final String accuracy;

  Classification({
    this.url,
    this.imgUrl,
    this.needsReview,
    this.isAutomated,
    this.species,
    this.accuracy,
  });

  factory Classification.fromJson(Map<String, dynamic> json) {
    return new Classification(
      url: json['url'],
      imgUrl: json['image'],
      needsReview: json['needs_review'],
      isAutomated: json['is_automated'],
      species: json['species'],
      accuracy: json['accuracy'],
    );
  }

  static List<Classification> listFromJsonArray(String json) {
    final parsedJson = jsonDecode(json).cast<Map<String, dynamic>>();
    return parsedJson
        .map<Classification>((json1) => Classification.fromJson(json1))
        .toList();
  }

  String printClassification() {
    return 'Classification: {url: $url, imgUrl: $imgUrl, needsReview: $needsReview, isAutomated: $isAutomated, species: $species, accuracy: $accuracy}';
  }
}

class ReviewData {
  final PhotoData photoData;
  final Classification classification;

  ReviewData({this.photoData, this.classification});

  String showContents() {
    return 'ReviewData: { photoData: ${photoData.toString()}, Classification: ${classification.printClassification()}}';
  }
}

class NotificationObj {
  final String title;
  final String body;
  final String dataTitle;
  final String dataBody;

  NotificationObj({this.title, this.body, this.dataTitle, this.dataBody});

  factory NotificationObj.fromJson(Map<String, dynamic> json) {
    final notification = json['notification'];
    final data = json['data'];

    return new NotificationObj(
      body: notification['body'],
      title: notification['title'],
      dataTitle: data['title'],
      dataBody: data['body'],
    );
  }
}

class UserApiObj {
  final String token;
  final String uid;

  UserApiObj({this.token, this.uid});
}

class Device {
  final String registrationId;
  final bool active;
  final String name;
  final int id;

  Device({this.registrationId, this.active, this.name, this.id});

  factory Device.fromJson(Map<String, dynamic> json) {
    return new Device(
      id: json['id'],
      active: json['active'],
      registrationId: json['registration_id'],
      name: json['name'],
    );
  }

  static List<Device> listFromJsonArray(String jsonArray) {
    final parsedJson = json.decode(jsonArray).cast<Map<String, dynamic>>();
    return parsedJson.map<Device>((json) => Device.fromJson(json)).toList();
  }
}

class SubmissionModel {
  final int id;
  final String fileUrl;
  final String imageUrl;
  final String classUrl;
  final String jobsUrl;
  final bool isTraining;
  final String dateTaken;

  SubmissionModel({
    this.id,
    this.fileUrl,
    this.imageUrl,
    this.classUrl,
    this.jobsUrl,
    this.isTraining,
    this.dateTaken,
  });

  factory SubmissionModel.fromJson(Map json) {
    return new SubmissionModel(
      id: json['id'],
      fileUrl: json['file'],
      imageUrl: json['url'],
      classUrl: json['classification'],
      jobsUrl: json['jobs'],
      isTraining: json['is_training'],
      dateTaken: json['date_taken'],
    );
  }
}

class ReclassificationModel {
  final String classUrl;
  final String species;
  final String accuracy;
  final String imgUrl;
  final String fileUrl;
  final bool isAutomated;
  final bool needsReview;

  ReclassificationModel({
    this.classUrl,
    this.species,
    this.accuracy,
    this.imgUrl,
    this.fileUrl,
    this.isAutomated,
    this.needsReview,
  });

  factory ReclassificationModel.fromJson(Map json) {
    return new ReclassificationModel(
      classUrl: json['url'],
      species: json['species'],
      accuracy: json['accuracy'],
      imgUrl: json['image'],
      fileUrl: json['file'],
      isAutomated: json['is_automated'],
      needsReview: json['needs_review'],
    );
  }
}

/// SubmissionsModel controls a `Stream` of submissions and handles refresh/pagination
class SubmissionsModel {
  Stream<List<SubmissionModel>> stream;
  bool hasMore;

  bool _isLoading;
  List<Map> _data;
  StreamController<List<Map>> _controller;
  int page;

  SubmissionsModel() {
    _data = List<Map>();
    _controller = StreamController<List<Map>>.broadcast();
    _isLoading = false;
    page = 1;
    stream = _controller.stream.map((List<Map> submissionsData) {
      return submissionsData.map((Map submissionData) {
        return SubmissionModel.fromJson(submissionData);
      }).toList();
    });
    hasMore = true;
    refresh();
  }

  Future<void> refresh() {
    return loadMore(clearCachedData: false);
  }

  Future<void> loadMore({bool clearCachedData = false}) {
    if (clearCachedData) {
      _data = List<Map>();
      hasMore = true;
    }
    if (_isLoading || !hasMore) {
      return Future.value();
    }
    _isLoading = true;
    return Global.apiService
        .getUserSubmissions(page: page)
        .then((submissionsData) {
      _isLoading = false;
      List submissions = submissionsData['results'];
      for (var i = 0; i < submissions.length; i++) {
        _data.add(submissions[i]);
      }

      hasMore = submissionsData['hasMore'];
      if (hasMore) {
        page++;
      }
      _controller.add(_data);
    });
  }
}

class ReclassificationsModel {
  Stream<List<ReclassificationModel>> stream;
  bool hasMore;

  bool _isLoading;
  List<Map> _data;
  StreamController<List<Map>> _controller;
  int page;

  ReclassificationsModel() {
    _data = List<Map>();
    _controller = StreamController<List<Map>>.broadcast();
    _isLoading = false;
    page = 1;
    stream = _controller.stream.map((List<Map> reclassificationsData) {
      return reclassificationsData.map((Map reclassificationData) {
        return ReclassificationModel.fromJson(reclassificationData);
      }).toList();
    });

    hasMore = true;
    refresh();
  }

  Future<void> refresh() {
    return loadMore(clearCachedData: false);
  }

  Future<void> loadMore({bool clearCachedData = false}) {
    if (clearCachedData) {
      _data = List<Map>();
      hasMore = true;
    }
    if (_isLoading || !hasMore) {
      return Future.value();
    }
    _isLoading = true;
    return Global.apiService
        .getNeedReview(page: page)
        .then((reclassificationsData) {
      _isLoading = false;
      List reclassifications = reclassificationsData['results'];

      for (var i = 0; i < reclassifications.length; i++) {
        _data.add(reclassifications[i]);
      }

      hasMore = reclassificationsData['hasMore'];
      if (hasMore) {
        page++;
      }
      _controller.add(_data);
    });
  }
}
