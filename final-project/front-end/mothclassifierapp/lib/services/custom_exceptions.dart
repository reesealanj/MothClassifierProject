class LoginException implements Exception {
  String _message;

  LoginException([String message = 'Login Unsuccessful']) {
    this._message = message;
  }

  @override
  String toString() {
    return _message;
  }
}

class InvalidTokenException implements Exception {
  String _message;

  InvalidTokenException([String message = 'Invalid API Token']) {
    this._message = message;
  }

  @override
  String toString() {
    return _message;
  }
}

class ApiException implements Exception {
  String message;

  ApiException({this.message = "API Exception Occurred"});

  @override
  String toString() {
    return message;
  }
}

class PhotoPickerException implements Exception {
  String message;

  PhotoPickerException({this.message = "Photo Picker Exception Occurred"});

  @override
  String toString() {
    return message;
  }
}
