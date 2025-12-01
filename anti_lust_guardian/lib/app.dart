
import 'package:flutter/material.dart';
import 'ui/cosmic_theme.dart';

class AntiLustGuardianApp extends StatelessWidget {
  final Widget home;

  const AntiLustGuardianApp({super.key, required this.home});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Anti-Lust Guardian',
      theme: CosmicTheme.themeData,
      home: home,
    );
  }
}
