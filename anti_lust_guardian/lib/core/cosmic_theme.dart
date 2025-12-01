import 'package:flutter/material.dart';

class CosmicColors {
  static const primaryGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF4F46E5),
      Color(0xFF8B5CF6),
    ],
  );
  
  static const primaryColor = Color(0xFF4F46E5);
  static const primaryLight = Color(0xFF8B5CF6);
  
  static const successGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF06B6D4),
      Color(0xFF34D399),
    ],
  );
  
  static const successColor = Color(0xFF34D399);
  
  static const errorGradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFEF4444),
      Color(0xFFF97316),
    ],
  );
  
  static const errorColor = Color(0xFFEF4444);
  
  static const accent1Gradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFFF472B6),
      Color(0xFFA78BFA),
    ],
  );
  
  static const accent2Gradient = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      Color(0xFF0EA5E9),
      Color(0xFF22D3EE),
    ],
  );
  
  static const backgroundDark = Color(0xFF0F172A);
  static const backgroundGradient = RadialGradient(
    center: Alignment.topRight,
    radius: 2.0,
    colors: [
      Color(0xFF1E3A8A),
      Color(0xFF0F172A),
    ],
  );
  
  static const textPrimary = Color(0xFFFFFFFF);
  static const textSecondary = Color(0xFFCBD5E1);
  static const textMuted = Color(0xFF94A3B8);
  
  static const surface = Color(0xFF1E293B);
  static const surfaceLight = Color(0xFF334155);
  static const surfaceBorder = Color(0xFF475569);
}

class GradientButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final Gradient gradient;
  final bool isLoading;
  final IconData? icon;
  final EdgeInsetsGeometry padding;
  
  const GradientButton({
    super.key,
    required this.text,
    this.onPressed,
    this.gradient = CosmicColors.primaryGradient,
    this.isLoading = false,
    this.icon,
    this.padding = const EdgeInsets.symmetric(vertical: 16),
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: gradient,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: gradient.colors.first.withOpacity(0.3),
            blurRadius: 20,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: isLoading ? null : onPressed,
          borderRadius: BorderRadius.circular(16),
          child: Container(
            padding: padding,
            child: Center(
              child: isLoading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                      ),
                    )
                  : Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        if (icon != null) ...[
                          Icon(icon, color: Colors.white, size: 20),
                          const SizedBox(width: 8),
                        ],
                        Text(
                          text,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 0.5,
                          ),
                        ),
                      ],
                    ),
            ),
          ),
        ),
      ),
    );
  }
}

class GradientCard extends StatelessWidget {
  final Widget child;
  final Gradient? gradient;
  final EdgeInsetsGeometry padding;
  final double borderRadius;
  final bool showBorder;
  
  const GradientCard({
    super.key,
    required this.child,
    this.gradient,
    this.padding = const EdgeInsets.all(20),
    this.borderRadius = 16,
    this.showBorder = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: gradient,
        color: gradient == null ? CosmicColors.surface : null,
        borderRadius: BorderRadius.circular(borderRadius),
        border: showBorder
            ? Border.all(color: CosmicColors.surfaceBorder, width: 1)
            : null,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.2),
            blurRadius: 20,
            offset: const Offset(0, 5),
          ),
        ],
      ),
      child: Padding(
        padding: padding,
        child: child,
      ),
    );
  }
}

class CosmicBackground extends StatelessWidget {
  final Widget child;
  
  const CosmicBackground({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: CosmicColors.backgroundGradient,
      ),
      child: child,
    );
  }
}

class GradientText extends StatelessWidget {
  final String text;
  final TextStyle? style;
  final Gradient gradient;
  
  const GradientText({
    super.key,
    required this.text,
    this.style,
    this.gradient = CosmicColors.primaryGradient,
  });

  @override
  Widget build(BuildContext context) {
    return ShaderMask(
      shaderCallback: (bounds) => gradient.createShader(
        Rect.fromLTWH(0, 0, bounds.width, bounds.height),
      ),
      child: Text(
        text,
        style: (style ?? const TextStyle()).copyWith(
          color: Colors.white,
        ),
      ),
    );
  }
}

class StatusBadge extends StatelessWidget {
  final String text;
  final Gradient gradient;
  final IconData? icon;
  
  const StatusBadge({
    super.key,
    required this.text,
    this.gradient = CosmicColors.successGradient,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        gradient: gradient,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: gradient.colors.first.withOpacity(0.3),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            Icon(icon, color: Colors.white, size: 14),
            const SizedBox(width: 4),
          ],
          Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 12,
              fontWeight: FontWeight.bold,
              letterSpacing: 0.5,
            ),
          ),
        ],
      ),
    );
  }
}
