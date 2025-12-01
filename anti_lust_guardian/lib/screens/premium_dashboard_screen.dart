import 'package:flutter/material.dart';

class CosmicTheme {
  static const Color neonCyan = Color(0xFF00F3FF);
  static const Color neonPurple = Color(0xFFD946EF);
  static const Color deepSpace = Color(0xFF0A0E27);
  static const Color cardBackground = Color(0xFF1a1f3a);
}

class PremiumDashboardScreen extends StatefulWidget {
  const PremiumDashboardScreen({super.key});

  @override
  _PremiumDashboardScreenState createState() => _PremiumDashboardScreenState();
}

class _PremiumDashboardScreenState extends State<PremiumDashboardScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.deepSpace,
      appBar: AppBar(
        title: const Text('PREMIUM ANALYTICS'),
        backgroundColor: Colors.transparent,
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: CosmicTheme.neonCyan,
          tabs: const [
            Tab(text: 'OVERVIEW'),
            Tab(text: 'PATTERNS'),
            Tab(text: 'PROGRESS'),
            Tab(text: 'INSIGHTS'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildOverviewTab(),
          _buildPatternsTab(),
          _buildProgressTab(),
          _buildInsightsTab(),
        ],
      ),
    );
  }

  Widget _buildOverviewTab() {
    return const Center(child: Text('Overview Tab', style: TextStyle(color: Colors.white)));
  }

  Widget _buildPatternsTab() {
    return const Center(child: Text('Patterns Tab', style: TextStyle(color: Colors.white)));
  }

  Widget _buildProgressTab() {
    return const Center(child: Text('Progress Tab', style: TextStyle(color: Colors.white)));
  }

  Widget _buildInsightsTab() {
    return const Center(child: Text('Insights Tab', style: TextStyle(color: Colors.white)));
  }
}
