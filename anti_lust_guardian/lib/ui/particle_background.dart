import 'dart:math';
import 'package:flutter/material.dart';
import 'cosmic_theme.dart';

class ParticleBackground extends StatefulWidget {
  final Widget? child;

  const ParticleBackground({super.key, this.child});

  @override
  _ParticleBackgroundState createState() => _ParticleBackgroundState();
}

class _ParticleBackgroundState extends State<ParticleBackground>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<Particle> _particles = [];
  final Random _random = Random();

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat();

    for (int i = 0; i < 100; i++) {
      _particles.add(_generateParticle());
    }
  }

  Particle _generateParticle() {
    return Particle(
      x: _random.nextDouble(),
      y: _random.nextDouble(),
      size: _random.nextDouble() * 2 + 0.5,
      speed: _random.nextDouble() * 0.2 + 0.05,
      opacity: _random.nextDouble() * 0.5 + 0.1,
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [CosmicTheme.deepSpace, CosmicTheme.voidBlack],
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
            ),
          ),
        ),
        AnimatedBuilder(
          animation: _controller,
          builder: (context, child) {
            return CustomPaint(
              painter: ParticlePainter(_particles, _controller.value),
              size: Size.infinite,
            );
          },
        ),
        if (widget.child != null) widget.child!,
      ],
    );
  }
}

class Particle {
  double x;
  double y;
  double size;
  double speed;
  double opacity;

  Particle({
    required this.x,
    required this.y,
    required this.size,
    required this.speed,
    required this.opacity,
  });
}

class ParticlePainter extends CustomPainter {
  final List<Particle> particles;
  final double animationValue;

  ParticlePainter(this.particles, this.animationValue);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = Colors.white;

    for (var particle in particles) {
      double y = particle.y - (particle.speed * 0.01);
      if (y < 0) {
        y = 1.0;
        particle.x = Random().nextDouble();
      }
      particle.y = y;

      paint.color = Colors.white.withOpacity(particle.opacity);
      
      canvas.drawCircle(
        Offset(particle.x * size.width, particle.y * size.height),
        particle.size,
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
