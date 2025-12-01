import 'package:flutter/material.dart';
import '../core/privacy_service.dart';
import 'cosmic_theme.dart';
import 'particle_background.dart';

class PrivacyDashboard extends StatefulWidget {
  const PrivacyDashboard({super.key});

  @override
  _PrivacyDashboardState createState() => _PrivacyDashboardState();
}

class _PrivacyDashboardState extends State<PrivacyDashboard> {
  final PrivacyService _privacyService = PrivacyService();
  bool _isIncognito = false;
  String _dataFootprint = 'Calculating...';

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final incognito = await _privacyService.isIncognitoMode();
    final footprint = await _privacyService.getDataFootprint();
    if (mounted) {
      setState(() {
        _isIncognito = incognito;
        _dataFootprint = footprint;
      });
    }
  }

  Future<void> _toggleIncognito(bool value) async {
    await _privacyService.setIncognitoMode(value);
    setState(() {
      _isIncognito = value;
    });
  }

  Future<void> _incinerateData() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => Dialog(
        backgroundColor: CosmicTheme.deepSpace.withOpacity(0.95),
        shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: CosmicTheme.alertRed, width: 2)),
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.warning_amber_rounded,
                  color: CosmicTheme.alertRed, size: 48),
              const SizedBox(height: 16),
              Text('CONFIRM INCINERATION',
                  style: CosmicTheme.headerStyle
                      .copyWith(color: CosmicTheme.alertRed, fontSize: 20)),
              const SizedBox(height: 12),
              Text(
                'This will permanently delete all local logs, settings, and keys. This action cannot be undone.',
                style: CosmicTheme.bodyStyle,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  TextButton(
                    onPressed: () => Navigator.pop(context, false),
                    child: Text('CANCEL', style: CosmicTheme.hudStyle),
                  ),
                  ElevatedButton(
                    onPressed: () => Navigator.pop(context, true),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: CosmicTheme.alertRed,
                      foregroundColor: Colors.white,
                    ),
                    child: const Text('BURN IT ALL'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );

    if (confirmed == true) {
      await _privacyService.incinerateData();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('All data incinerated successfully.'),
            backgroundColor: CosmicTheme.alertRed,
          ),
        );
        _loadData();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.deepSpace,
      appBar: AppBar(
        title: Text('PRIVACY CONTROL', style: CosmicTheme.headerStyle),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      extendBodyBehindAppBar: true,
      body: ParticleBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoCard(),
                const SizedBox(height: 24),
                _buildToggleCard(),
                const Spacer(),
                _buildIncineratorButton(),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildInfoCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: CosmicTheme.voidBlack.withOpacity(0.6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: CosmicTheme.neonCyan.withOpacity(0.5)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('LOCAL DATA FOOTPRINT',
                  style: CosmicTheme.hudStyle.copyWith(fontSize: 10)),
              const SizedBox(height: 8),
              Text(_dataFootprint,
                  style: CosmicTheme.headerStyle.copyWith(fontSize: 28)),
            ],
          ),
          const Icon(Icons.sd_storage, color: CosmicTheme.neonCyan, size: 32),
        ],
      ),
    );
  }

  Widget _buildToggleCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: CosmicTheme.voidBlack.withOpacity(0.6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: CosmicTheme.plasmaPurple.withOpacity(0.5)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('INCOGNITO MODE',
                  style: CosmicTheme.hudStyle.copyWith(fontSize: 10)),
              const SizedBox(height: 4),
              Text(_isIncognito ? 'ACTIVE' : 'INACTIVE',
                  style: CosmicTheme.headerStyle.copyWith(
                      fontSize: 20,
                      color: _isIncognito
                          ? CosmicTheme.hudGreen
                          : CosmicTheme.starlightWhite)),
            ],
          ),
          Switch(
            value: _isIncognito,
            onChanged: _toggleIncognito,
            activeColor: CosmicTheme.hudGreen,
            activeTrackColor: CosmicTheme.hudGreen.withOpacity(0.3),
            inactiveThumbColor: CosmicTheme.starlightWhite,
            inactiveTrackColor: CosmicTheme.voidBlack,
          ),
        ],
      ),
    );
  }

  Widget _buildIncineratorButton() {
    return SizedBox(
      width: double.infinity,
      height: 60,
      child: ElevatedButton(
        onPressed: _incinerateData,
        style: ElevatedButton.styleFrom(
          backgroundColor: CosmicTheme.alertRed.withOpacity(0.1),
          side: const BorderSide(color: CosmicTheme.alertRed, width: 2),
        ),
        child: Text(
          'INCINERATE ALL DATA',
          style: CosmicTheme.hudStyle.copyWith(
            fontWeight: FontWeight.bold,
            fontSize: 16,
            color: CosmicTheme.alertRed,
          ),
        ),
      ),
    );
  }
}
