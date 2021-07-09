import 'dart:io';
import 'dart:async';
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart' as p;
import 'custom_exceptions.dart';

class ImgService {
  PickedFile pfile;
  File file;

  final _picker = ImagePicker();

  Future<File> choose(String uid) async {
    pfile = await _picker.getImage(
      source: ImageSource.gallery,
    );

    if (pfile?.path == null) {
      throw new PhotoPickerException(message: "No Photo Selected");
    }

    file = File(pfile.path);
    String ext = p.extension(file.path);
    String dir = p.dirname(file.path);
    String time = (DateTime.now().toUtc().millisecondsSinceEpoch).toString();
    String fileName = "${uid}_$time.$ext";
    String newPath = p.join(dir, fileName);
    file = file.renameSync(newPath);
    return file;
  }

  Future<void> take() async {
    pfile = await _picker.getImage(
      source: ImageSource.camera,
      maxWidth: 360,
      maxHeight: 360,
    );

    file = File(pfile.path);
  }

  void clear() {
    pfile = null;
    file = null;
  }
}
