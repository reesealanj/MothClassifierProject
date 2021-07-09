import 'package:flutter/material.dart';
import '../../services/services.dart';
import 'Reclassification.dart';

class Reclassifications extends StatefulWidget {
  const Reclassifications({
    Key key,
  }) : super(key: key);

  @override
  _ReclassificationsState createState() => _ReclassificationsState();
}

class _ReclassificationsState extends State<Reclassifications> {
  final scrollController = ScrollController();
  ReclassificationsModel reclassifications;

  @override
  void initState() {
    reclassifications = ReclassificationsModel();
    scrollController.addListener(() {
      if (scrollController.position.maxScrollExtent ==
          scrollController.offset) {
        reclassifications.loadMore();
      }
    });

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: reclassifications.stream,
      builder: (BuildContext _context, AsyncSnapshot _snapshot) {
        if (!_snapshot.hasData) {
          return Center(child: CircularProgressIndicator());
        } else {
          return ListView.separated(
            padding: EdgeInsets.symmetric(vertical: 8.0),
            controller: scrollController,
            separatorBuilder: (context, index) => Divider(),
            itemCount: _snapshot.data.length + 1,
            itemBuilder: (BuildContext _context, int index) {
              if (index < _snapshot.data.length) {
                return Reclassification(
                    reclassification: _snapshot.data[index]);
              } else if (reclassifications.hasMore) {
                return Padding(
                  padding: EdgeInsets.symmetric(vertical: 32.0),
                  child: Center(child: CircularProgressIndicator()),
                );
              } else {
                return Padding(
                  padding: EdgeInsets.symmetric(vertical: 32.0),
                  child: Center(
                    child: Text('No more to load!'),
                  ),
                );
              }
            },
          );
        }
      },
    );
  }
}
