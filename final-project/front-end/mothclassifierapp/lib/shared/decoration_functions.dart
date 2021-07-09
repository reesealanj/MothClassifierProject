import 'package:flutter/material.dart';
import 'painter_palette.dart';

InputDecoration registerInputDecoration({String hintText}) {
  return InputDecoration(
    contentPadding: const EdgeInsets.symmetric(vertical: 18.0),
    hintStyle: const TextStyle(color: Colors.white, fontSize: 18),
    hintText: hintText,
    focusedBorder: const UnderlineInputBorder(
      borderSide: BorderSide(color: Colors.white, width: 2),
    ),
    enabledBorder: const UnderlineInputBorder(
      borderSide: BorderSide(color: Colors.white),
    ),
    errorBorder: const UnderlineInputBorder(
      borderSide: BorderSide(color: PainterPalette.orange),
    ),
    focusedErrorBorder: const UnderlineInputBorder(
      borderSide: BorderSide(width: 2.0, color: PainterPalette.orange),
    ),
    errorStyle: const TextStyle(color: Colors.white),
  );
}

InputDecoration signInInputDecoration({String hintText}) {
  return InputDecoration(
    contentPadding: const EdgeInsets.symmetric(vertical: 18.0),
    hintStyle: const TextStyle(fontSize: 18),
    hintText: hintText,
    focusedBorder: UnderlineInputBorder(
      borderSide: BorderSide(width: 2, color: PainterPalette.dBlue),
    ),
    enabledBorder: UnderlineInputBorder(
      borderSide: BorderSide(color: PainterPalette.dBlue),
    ),
    errorBorder: UnderlineInputBorder(
      borderSide: BorderSide(color: PainterPalette.dOrange),
    ),
    focusedErrorBorder: UnderlineInputBorder(
      borderSide: BorderSide(width: 2.0, color: PainterPalette.dOrange),
    ),
    errorStyle: TextStyle(color: PainterPalette.dOrange),
  );
}
