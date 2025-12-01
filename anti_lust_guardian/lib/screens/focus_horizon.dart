
import 'package:flutter/material.dart';

class FocusHorizonScreen extends StatefulWidget {
  const FocusHorizonScreen({super.key});

  @override
  _FocusHorizonScreenState createState() => _FocusHorizonScreenState();
}

class _FocusHorizonScreenState extends State<FocusHorizonScreen> {
  final int _streak = 42;

  final List<Map<String, String>> _pathways = [
    {
      'title': 'Channel Your Energy',
      'subtitle': 'Convert temptation into creative work.',
    },
    {
      'title': 'Find Your Purpose',
      'subtitle': 'Define your mission and stay focused.',
    },
    {
      'title': 'Build Healthy Habits',
      'subtitle': 'Replace bad habits with good ones.',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Focus Horizon'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text(
              'Your Current Streak: $_streak days',
              style: const TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20.0),
            const Text(
              'Purpose Pathways',
              style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10.0),
            Expanded(
              child: ListView.builder(
                itemCount: _pathways.length,
                itemBuilder: (context, index) {
                  final pathway = _pathways[index];
                  return Card(
                    child: ListTile(
                      title: Text(pathway['title']!),
                      subtitle: Text(pathway['subtitle']!),
                      onTap: () {
                      },
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
