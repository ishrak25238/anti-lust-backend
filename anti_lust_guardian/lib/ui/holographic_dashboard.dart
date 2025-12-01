import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'cosmic_theme.dart';
import 'particle_background.dart';
import 'privacy_dashboard.dart';
import 'education_hub.dart';

class HolographicDashboard extends StatefulWidget {
  const HolographicDashboard({super.key});

  @override
  _HolographicDashboardState createState() => _HolographicDashboardState();
}

class _HolographicDashboardState extends State<HolographicDashboard>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late AnimationController _rotateController;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _rotateController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _rotateController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ParticleBackground(
        child: SafeArea(
          child: Stack(
            children: [
              const Positioned(top: 20, left: 20, child: HudCorner(isTopLeft: true)),
              const Positioned(top: 20, right: 20, child: HudCorner(isTopLeft: false)),
              const Positioned(bottom: 20, left: 20, child: HudCorner(isTopLeft: false, isBottom: true)),
              const Positioned(bottom: 20, right: 20, child: HudCorner(isTopLeft: true, isBottom: true)),

              Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _buildCore(),
                    const SizedBox(height: 40),
                    Text(
                      'SYSTEM ACTIVE',
                      style: CosmicTheme.headerStyle.copyWith(
                        color: CosmicTheme.neonCyan,
                        shadows: [
                          const BoxShadow(
                            color: CosmicTheme.neonCyan,
                            blurRadius: 10,
                            spreadRadius: 2,
                          )
                        ],
                      ),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      'Threats Blocked: 0', // Connect to real data later
                      style: CosmicTheme.hudStyle,
                    ),
                    const SizedBox(height: 40),
                    IconButton(
                      icon: const Icon(Icons.shield, color: CosmicTheme.hudGreen, size: 32),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const PrivacyDashboard()),
                        );
                      },
                      tooltip: 'Privacy Controls',
                    ),
                    const SizedBox(height: 10),
                    IconButton(
                      icon: const Icon(Icons.school, color: CosmicTheme.neonCyan, size: 32),
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const EducationHub()),
                        );
                      },
                      tooltip: 'Education Hub',
                    ),
                    Text(
                      'KNOWLEDGE BASE',
                      style: CosmicTheme.hudStyle.copyWith(fontSize: 10, color: CosmicTheme.neonCyan),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCore() {
    return AnimatedBuilder(
      animation: Listenable.merge([_pulseController, _rotateController]),
      builder: (context, child) {
        return Stack(
          alignment: Alignment.center,
          children: [
            Transform.rotate(
              angle: _rotateController.value * 2 * math.pi,
              child: Container(
                width: 200,
                height: 200,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(
                    color: CosmicTheme.plasmaPurple.withOpacity(0.5),
                    width: 2,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: CosmicTheme.plasmaPurple.withOpacity(0.3),
                      blurRadius: 20,
                      spreadRadius: 5,
                    ),
                  ],
                ),
              ),
            ),
            Transform.scale(
              scale: 1.0 + (_pulseController.value * 0.1),
              child: Container(
                width: 150,
                height: 150,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: RadialGradient(
                    colors: [
                      CosmicTheme.neonCyan.withOpacity(0.8),
                      CosmicTheme.deepSpace.withOpacity(0.0),
                    ],
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: CosmicTheme.neonCyan.withOpacity(0.6),
                      blurRadius: 30,
                      spreadRadius: 10,
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.security,
                  size: 60,
                  color: Colors.white,
                ),
              ),
            ),
          ],
        );
      },
    );
  }
}

class HudCorner extends StatelessWidget {
  final bool isTopLeft;
  final bool isBottom;

  const HudCorner({super.key, this.isTopLeft = true, this.isBottom = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 40,
      height: 40,
      decoration: BoxDecoration(
        border: Border(
          top: !isBottom ? const BorderSide(color: CosmicTheme.neonCyan, width: 2) : BorderSide.none,
          bottom: isBottom ? const BorderSide(color: CosmicTheme.neonCyan, width: 2) : BorderSide.none,
          left: isTopLeft ? const BorderSide(color: CosmicTheme.neonCyan, width: 2) : BorderSide.none,
          right: !isTopLeft ? const BorderSide(color: CosmicTheme.neonCyan, width: 2) : BorderSide.none,
        ),
      ),
    );
  }
}
