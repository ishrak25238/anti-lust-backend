import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../../ui/cosmic_theme.dart';
import '../../core/parental_link_service.dart';
import '../../ui/particle_background.dart';

class RoleSelectionScreen extends StatefulWidget {
  final VoidCallback onRoleSelected;

  const RoleSelectionScreen({super.key, required this.onRoleSelected});

  @override
  _RoleSelectionScreenState createState() => _RoleSelectionScreenState();
}

class _RoleSelectionScreenState extends State<RoleSelectionScreen> {
  final ParentalLinkService _linkService = ParentalLinkService();
  final TextEditingController _codeController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  
  String? _generatedCode;
  bool _isParent = false;
  bool _showInput = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: CosmicTheme.spaceBlack,
      body: Stack(
        children: [
          const ParticleBackground(),
          Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'IDENTITY PROTOCOL',
                    style: GoogleFonts.orbitron(
                      fontSize: 24,
                      color: CosmicTheme.hologramBlue,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2.0,
                    ),
                  ),
                  const SizedBox(height: 40),
                  if (!_showInput) ...[
                    _buildRoleButton(
                      title: 'I AM A PARENT',
                      subtitle: 'Monitor & Protect',
                      icon: Icons.security,
                      color: CosmicTheme.neonCyan,
                      onTap: () {
                        setState(() {
                          _isParent = true;
                          _showInput = true;
                        });
                      },
                    ),
                    const SizedBox(height: 20),
                    _buildRoleButton(
                      title: 'I AM A CHILD',
                      subtitle: 'Guardian Active',
                      icon: Icons.child_care,
                      color: CosmicTheme.plasmaPink,
                      onTap: () async {
                        setState(() {
                          _isParent = false;
                          _showInput = true;
                        });
                        final code = await _linkService.generatePairingCode();
                        setState(() {
                          _generatedCode = code;
                        });
                        await _linkService.setUserRole('child');
                      },
                    ),
                  ] else if (_isParent) ...[
                    _buildParentInput(),
                  ] else ...[
                    _buildChildDisplay(),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRoleButton({
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          border: Border.all(color: color.withOpacity(0.5)),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.2),
              blurRadius: 10,
              spreadRadius: 1,
            ),
          ],
        ),
        child: Row(
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(width: 20),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: GoogleFonts.orbitron(
                    fontSize: 18,
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                Text(
                  subtitle,
                  style: GoogleFonts.roboto(
                    fontSize: 14,
                    color: Colors.white70,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildParentInput() {
    return Column(
      children: [
        Text(
          'CONNECT TO CHILD DEVICE',
          style: GoogleFonts.orbitron(color: Colors.white, fontSize: 16),
        ),
        const SizedBox(height: 20),
        TextField(
          controller: _nameController,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            labelText: "Child's Name",
            labelStyle: TextStyle(color: CosmicTheme.hologramBlue),
            enabledBorder: OutlineInputBorder(
              borderSide: BorderSide(color: CosmicTheme.hologramBlue),
            ),
            focusedBorder: OutlineInputBorder(
              borderSide: BorderSide(color: CosmicTheme.neonCyan),
            ),
          ),
        ),
        const SizedBox(height: 10),
        TextField(
          controller: _codeController,
          style: const TextStyle(color: Colors.white),
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(
            labelText: "Enter Pairing Code",
            labelStyle: TextStyle(color: CosmicTheme.hologramBlue),
            enabledBorder: OutlineInputBorder(
              borderSide: BorderSide(color: CosmicTheme.hologramBlue),
            ),
            focusedBorder: OutlineInputBorder(
              borderSide: BorderSide(color: CosmicTheme.neonCyan),
            ),
          ),
        ),
        const SizedBox(height: 30),
        ElevatedButton(
          onPressed: () async {
            final success = await _linkService.linkChildAccount(
              _codeController.text,
              _nameController.text,
            );
            if (success) {
              await _linkService.setUserRole('parent');
              widget.onRoleSelected();
            } else {
              if (!context.mounted) return;
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Invalid Code')),
              );
            }
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: CosmicTheme.neonCyan,
            padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
          ),
          child: Text('LINK & MONITOR', style: GoogleFonts.orbitron(color: Colors.black)),
        ),
      ],
    );
  }

  Widget _buildChildDisplay() {
    return Column(
      children: [
        Text(
          'YOUR PAIRING CODE',
          style: GoogleFonts.orbitron(color: Colors.white, fontSize: 16),
        ),
        const SizedBox(height: 20),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 20),
          decoration: BoxDecoration(
            border: Border.all(color: CosmicTheme.plasmaPink),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            _generatedCode ?? 'GENERATING...',
            style: GoogleFonts.orbitron(
              fontSize: 32,
              color: CosmicTheme.plasmaPink,
              fontWeight: FontWeight.bold,
              letterSpacing: 5,
            ),
          ),
        ),
        const SizedBox(height: 30),
        Text(
          'Enter this code on the Parent device to activate protection.',
          textAlign: TextAlign.center,
          style: GoogleFonts.roboto(color: Colors.white70),
        ),
        const SizedBox(height: 30),
        ElevatedButton(
          onPressed: () {
             widget.onRoleSelected();
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: CosmicTheme.plasmaPink,
            padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 15),
          ),
          child: Text('ACTIVATE GUARDIAN', style: GoogleFonts.orbitron(color: Colors.black)),
        ),
      ],
    );
  }
}
