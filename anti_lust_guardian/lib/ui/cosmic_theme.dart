import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CosmicTheme {
  static const Color deepSpace = Color(0xFF0B0D17);
  static const Color voidBlack = Color(0xFF050508);
  static const Color neonCyan = Color(0xFF00F0FF);
  static const Color plasmaPurple = Color(0xFFBC13FE);
  static const Color alertRed = Color(0xFFFF2A6D);
  static const Color starlightWhite = Color(0xFFE0E6ED);
  static const Color hudGreen = Color(0xFF00FF9D);
  
  static const Color spaceBlack = deepSpace;
  static const Color hologramBlue = neonCyan;
  static const Color plasmaPink = plasmaPurple;

  static const LinearGradient primaryGradient = LinearGradient(
    colors: [neonCyan, plasmaPurple],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient hudGradient = LinearGradient(
    colors: [Color(0x0000F0FF), Color(0x3300F0FF)],
    begin: Alignment.topCenter,
    end: Alignment.bottomCenter,
  );

  static TextStyle get headerStyle => GoogleFonts.orbitron(
    color: starlightWhite,
    fontWeight: FontWeight.bold,
    letterSpacing: 1.5,
  );

  static TextStyle get hudStyle => GoogleFonts.robotoMono(
    color: neonCyan,
    fontSize: 12,
    letterSpacing: 1.0,
  );

  static TextStyle get bodyStyle => GoogleFonts.rajdhani(
    color: starlightWhite.withOpacity(0.9),
    fontSize: 16,
  );

  static ThemeData get themeData => ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: deepSpace,
    primaryColor: neonCyan,
    colorScheme: const ColorScheme.dark(
      primary: neonCyan,
      secondary: plasmaPurple,
      surface: voidBlack,
      background: deepSpace,
      error: alertRed,
    ),
    textTheme: TextTheme(
      displayLarge: headerStyle.copyWith(fontSize: 32),
      displayMedium: headerStyle.copyWith(fontSize: 24),
      bodyLarge: bodyStyle,
      bodyMedium: bodyStyle,
      labelSmall: hudStyle,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.transparent,
        foregroundColor: deepSpace,
        textStyle: headerStyle.copyWith(fontSize: 14),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
          side: const BorderSide(color: neonCyan, width: 1),
        ),
      ),
    ),
  );
}
