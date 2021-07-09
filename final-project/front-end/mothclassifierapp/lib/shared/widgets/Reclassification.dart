import 'package:flutter/material.dart';
import '../../services/services.dart';
import '../../screens/screens.dart';

class Reclassification extends StatelessWidget {
  final ReclassificationModel reclassification;

  const Reclassification({
    Key key,
    @required this.reclassification,
  })  : assert(reclassification != null),
        super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Image.network(
        reclassification.fileUrl,
        width: 80.0,
        height: 80.0,
      ),
      title: Text('Species: ${reclassification.species}'),
      onTap: () async {
        PhotoData photo =
            await Global.apiService.photoFromUrl(reclassification.imgUrl);

        Navigator.of(context).pushAndRemoveUntil(
            MaterialPageRoute(
              builder: (context) => ReclassifyDetailScreen(
                imgData: photo,
                classData: reclassification,
              ),
            ),
            (Route<dynamic> route) => false);
      },
    );
  }
}
