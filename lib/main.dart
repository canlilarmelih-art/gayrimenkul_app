import 'package:flutter/material.dart';
import 'screens/rapor_list_screen.dart';

void main() {
  runApp(GayrimenkulApp());
}

class GayrimenkulApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Gayrimenkul Değerleme',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: RaporListScreen(),
    );
  }
}
