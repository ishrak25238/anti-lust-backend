// Basic test to verify app initialization
// Note: Full integration tests require Firebase/Supabase setup

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:anti_lust_guardian/app.dart';

void main() {
  testWidgets('App widget test', (WidgetTester tester) async {
    //Build our app
    await tester.pumpWidget(const AntiLustGuardianApp(
      home: Scaffold(
        body: Center(child: Text('Test')),
      ),
    ));

    // Verify app builds without crashing
    expect(find.text('Test'), findsOneWidget);
  });
}
