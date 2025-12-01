import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'cosmic_theme.dart';
import '../core/parental_link_service.dart';
import 'particle_background.dart';

class ParentDashboard extends StatefulWidget {
  const ParentDashboard({super.key});

  @override
  _ParentDashboardState createState() => _ParentDashboardState();
}

class _ParentDashboardState extends State<ParentDashboard> {
  final ParentalLinkService _linkService = ParentalLinkService();
  String _childName = 'Loading...';
  List<Map<String, dynamic>> _logs = [];

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final name = await _linkService.getChildName();
    final logs = await _linkService.fetchChildLogs();
    setState(() {
      _childName = name ?? 'Unknown Child';
      _logs = logs;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.spaceBlack,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: Text('PARENTAL COMMAND', style: GoogleFonts.orbitron(color: CosmicTheme.neonCyan)),
        centerTitle: true,
        elevation: 0,
      ),
      body: Stack(
        children: [
          const ParticleBackground(),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildStatusCard(),
                const SizedBox(height: 20),
                Text(
                  'ACTIVITY LOGS',
                  style: GoogleFonts.orbitron(
                    color: Colors.white,
                    fontSize: 18,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 10),
                Expanded(
                  child: ListView.builder(
                    itemCount: _logs.length,
                    itemBuilder: (context, index) {
                      final log = _logs[index];
                      return _buildLogCard(log);
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: CosmicTheme.hologramBlue.withOpacity(0.1),
        border: Border.all(color: CosmicTheme.neonCyan),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 30,
            backgroundColor: CosmicTheme.neonCyan,
            child: Icon(Icons.child_care, color: Colors.black, size: 30),
          ),
          const SizedBox(width: 20),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                _childName.toUpperCase(),
                style: GoogleFonts.orbitron(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 5),
              Row(
                children: [
                  const Icon(Icons.shield, color: Colors.greenAccent, size: 16),
                  const SizedBox(width: 5),
                  Text(
                    'GUARDIAN ACTIVE',
                    style: GoogleFonts.roboto(color: Colors.greenAccent),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildLogCard(Map<String, dynamic> log) {
    Color statusColor = Colors.white;
    if (log['status'] == 'BLOCKED') statusColor = CosmicTheme.plasmaPink;
    if (log['status'] == 'WARNING') statusColor = Colors.orangeAccent;
    if (log['status'] == 'SECURED') statusColor = CosmicTheme.neonCyan;

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black54,
        border: Border(left: BorderSide(color: statusColor, width: 4)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                log['status'],
                style: GoogleFonts.orbitron(
                  color: statusColor,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                log['timestamp'].toString().substring(11, 16), // HH:mm
                style: GoogleFonts.roboto(color: Colors.white54),
              ),
            ],
          ),
          const SizedBox(height: 5),
          Text(
            log['activity'],
            style: GoogleFonts.roboto(color: Colors.white, fontSize: 16),
          ),
        ],
      ),
    );
  }
}
