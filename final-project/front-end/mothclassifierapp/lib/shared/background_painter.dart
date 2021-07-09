import 'dart:ui';

import 'package:flutter/material.dart';
import 'painter_palette.dart';
import 'dart:math';

class BackgroundPainter extends CustomPainter {
  BackgroundPainter({Animation<double> animation})
      : bluePaint = Paint()
          ..color = PainterPalette.lBlue
          ..style = PaintingStyle.fill,
        orangePaint = Paint()
          ..color = PainterPalette.orange
          ..style = PaintingStyle.fill,
        greyPaint = Paint()
          ..color = PainterPalette.dBlue
          ..style = PaintingStyle.fill,
        liquidAnimation = CurvedAnimation(
          curve: Curves.elasticOut,
          reverseCurve: Curves.easeInBack,
          parent: animation,
        ),
        orangeAnimation = CurvedAnimation(
          parent: animation,
          curve: const Interval(
            0,
            0.7,
            curve: Interval(0, 0.8, curve: SpringCurve()),
          ),
          reverseCurve: Curves.linear,
        ),
        greyAnimation = CurvedAnimation(
          parent: animation,
          curve: const Interval(
            0,
            0.8,
            curve: Interval(0, 0.9, curve: SpringCurve()),
          ),
          reverseCurve: Curves.easeInCirc,
        ),
        blueAnimation = CurvedAnimation(
          parent: animation,
          curve: const SpringCurve(),
          reverseCurve: Curves.easeInCirc,
        ),
        super(repaint: animation);

  final Animation<double> liquidAnimation;
  final Animation<double> blueAnimation;
  final Animation<double> greyAnimation;
  final Animation<double> orangeAnimation;

  final Paint bluePaint;
  final Paint orangePaint;
  final Paint greyPaint;

  @override
  void paint(Canvas canvas, Size size) {
    paintBlue(canvas, size);
    paintGrey(canvas, size);
    paintOrange(canvas, size);
  }

  void paintBlue(Canvas canvas, Size size) {
    final path = Path();

    path.moveTo(size.width, size.height / 2);
    path.lineTo(size.width, 0);
    path.lineTo(0, 0);
    path.lineTo(
      0,
      lerpDouble(0, size.height, blueAnimation.value),
    );
    _addPointsToPath(path, [
      Point(
        lerpDouble(0, size.width / 3, blueAnimation.value),
        lerpDouble(0, size.height, blueAnimation.value),
      ),
      Point(
        lerpDouble(size.width / 2, size.width / 4 * 3, liquidAnimation.value),
        lerpDouble(size.height / 2, size.height / 4 * 3, liquidAnimation.value),
      ),
      Point(
        size.width,
        lerpDouble(size.height / 2, size.height * 3 / 4, liquidAnimation.value),
      ),
    ]);

    canvas.drawPath(path, bluePaint);
  }

  void paintGrey(Canvas canvas, Size size) {
    final path = Path();
    path.moveTo(size.width, 300);
    path.lineTo(size.width, 0);
    path.lineTo(0, 0);
    path.lineTo(
      0,
      lerpDouble(
        size.height / 4,
        size.height / 2,
        greyAnimation.value,
      ),
    );
    _addPointsToPath(
      path,
      [
        Point(
          size.width / 4,
          lerpDouble(
              size.height / 2, size.height * 3 / 4, liquidAnimation.value),
        ),
        Point(
          size.width * 3 / 5,
          lerpDouble(size.height / 4, size.height / 2, liquidAnimation.value),
        ),
        Point(
          size.width * 4 / 5,
          lerpDouble(size.height / 6, size.height / 3, greyAnimation.value),
        ),
        Point(
          size.width,
          lerpDouble(size.height / 5, size.height / 4, greyAnimation.value),
        ),
      ],
    );

    canvas.drawPath(path, greyPaint);
  }

  void paintOrange(Canvas canvas, Size size) {
    if (orangeAnimation.value > 0) {
      final path = Path();

      path.moveTo(size.width * 3 / 4, 0);
      path.lineTo(0, 0);
      path.lineTo(
        0,
        lerpDouble(0, size.height / 12, orangeAnimation.value),
      );

      _addPointsToPath(path, [
        Point(
          size.width / 7,
          lerpDouble(0, size.height / 6, liquidAnimation.value),
        ),
        Point(
          size.width / 3,
          lerpDouble(0, size.height / 10, liquidAnimation.value),
        ),
        Point(
          size.width / 3 * 2,
          lerpDouble(0, size.height / 8, liquidAnimation.value),
        ),
        Point(
          size.width * 3 / 4,
          0,
        ),
      ]);

      canvas.drawPath(path, orangePaint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return true;
  }

  void _addPointsToPath(Path path, List<Point> points) {
    if (points.length < 3) {
      throw UnsupportedError('Insufficient points in call to AddPointsToPath');
    }

    for (var i = 0; i < points.length - 2; i++) {
      final xc = (points[i].x + points[i + 1].x) / 2;
      final yc = (points[i].y + points[i + 1].y) / 2;
      path.quadraticBezierTo(points[i].x, points[i].y, xc, yc);
    }

    path.quadraticBezierTo(
        points[points.length - 2].x,
        points[points.length - 2].y,
        points[points.length - 1].x,
        points[points.length - 1].y);
  }
}

class Point {
  final double x;
  final double y;

  Point(this.x, this.y);
}

class SpringCurve extends Curve {
  const SpringCurve({
    this.a = 0.15,
    this.w = 19.4,
  });
  final double a;
  final double w;

  @override
  double transformInternal(double t) {
    return (-(pow(e, -t / a) * cos(t * w)) + 1).toDouble();
  }
}
