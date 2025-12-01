import 'package:flutter/material.dart';
import 'cosmic_theme.dart';
import 'particle_background.dart';

class EducationHub extends StatelessWidget {
  const EducationHub({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.deepSpace,
      appBar: AppBar(
        title: Text('KNOWLEDGE BASE', style: CosmicTheme.headerStyle),
        backgroundColor: Colors.transparent,
        elevation: 0,
        centerTitle: true,
      ),
      extendBodyBehindAppBar: true,
      body: ParticleBackground(
        child: SafeArea(
          child: ListView(
            padding: const EdgeInsets.all(24),
            children: [
              _buildStatCard(),
              const SizedBox(height: 32),
              Text('THE SCIENCE OF ADDICTION', style: CosmicTheme.headerStyle.copyWith(fontSize: 20)),
              const SizedBox(height: 16),
              _buildArticleCard(
                'The Dopamine Trap',
                'Why "just one more scroll" turns into hours of wasted time.',
                Icons.loop,
              ),
              _buildArticleCard(
                'Your Brain on Lust',
                'How hyper-stimulating content rewires your reward pathways.',
                Icons.psychology,
              ),
              _buildArticleCard(
                'Reclaiming Focus',
                'Practical steps to rebuild your attention span and willpower.',
                Icons.self_improvement,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatCard() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: CosmicTheme.primaryGradient,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: CosmicTheme.neonCyan.withOpacity(0.4),
            blurRadius: 20,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Column(
        children: [
          Text(
            'TIME RECLAIMED',
            style: CosmicTheme.hudStyle.copyWith(color: CosmicTheme.deepSpace, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(
            '12h 30m', // Mock data
            style: CosmicTheme.headerStyle.copyWith(color: CosmicTheme.deepSpace, fontSize: 36),
          ),
          const SizedBox(height: 8),
          Text(
            'This Week',
            style: CosmicTheme.bodyStyle.copyWith(color: CosmicTheme.deepSpace.withOpacity(0.8)),
          ),
        ],
      ),
    );
  }

  Widget _buildArticleCard(String title, String subtitle, IconData icon) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: CosmicTheme.voidBlack.withOpacity(0.6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: CosmicTheme.plasmaPurple.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: CosmicTheme.plasmaPurple.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: CosmicTheme.plasmaPurple, size: 28),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: CosmicTheme.headerStyle.copyWith(fontSize: 18)),
                const SizedBox(height: 4),
                Text(subtitle, style: CosmicTheme.bodyStyle.copyWith(fontSize: 14, color: Colors.grey)),
              ],
            ),
          ),
          const Icon(Icons.arrow_forward_ios, color: Colors.grey, size: 16),
        ],
      ),
    );
  }
}
