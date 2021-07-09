import 'package:flutter/material.dart';
import '../../services/services.dart';
import 'Submission.dart';

class Submissions extends StatefulWidget {
  const Submissions({
    Key key,
  }) : super(key: key);

  @override
  _SubmissionsState createState() => _SubmissionsState();
}

class _SubmissionsState extends State<Submissions> {
  final scrollController = ScrollController();
  SubmissionsModel submissions;

  @override
  void initState() {
    submissions = SubmissionsModel();
    scrollController.addListener(() {
      if (scrollController.position.maxScrollExtent ==
          scrollController.offset) {
        submissions.loadMore();
      }
    });

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: submissions.stream,
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
                return Submission(submission: _snapshot.data[index]);
              } else if (submissions.hasMore) {
                return Padding(
                  padding: EdgeInsets.symmetric(vertical: 32.0),
                  child: Center(child: CircularProgressIndicator()),
                );
              } else {
                return Padding(
                  padding: EdgeInsets.symmetric(vertical: 32.0),
                  child: Center(
                    child: Text('No more submissions to load!'),
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
