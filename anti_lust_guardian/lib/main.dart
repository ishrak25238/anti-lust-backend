import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:flutter_windowmanager/flutter_windowmanager.dart'; // Screen Shield
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'app.dart';
import 'core/threat_db.dart';
import 'core/security_service.dart';
import 'core/parental_link_service.dart';
import 'services/subscription_service.dart';
import 'ui/cosmic_theme.dart';
import 'ui/holographic_dashboard.dart';
import 'ui/parent_dashboard.dart';
import 'ui/consent_modal.dart'; // Actually ConsentScreen
import 'screens/auth/role_selection_screen.dart';
import 'screens/auth/login_screen.dart';
import 'screens/paywall_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables (optional - may not exist in some builds)
  try {
    await dotenv.load(fileName: ".env");
    debugPrint('✅ Environment variables loaded');
  } catch (e) {
    debugPrint('⚠️ .env file not found or invalid: $e');
    // Continue without .env - use defaults
  }

  // Initialize Firebase
  await Firebase.initializeApp();

  // Try to initialize Supabase (optional - app works with Firebase only)
  try {
    final supabaseUrl = dotenv.env['SUPABASE_URL'];
    final supabaseKey = dotenv.env['SUPABASE_ANON_KEY'];
    if (supabaseUrl != null && supabaseKey != null && supabaseUrl.isNotEmpty && supabaseKey.isNotEmpty) {
      await Supabase.initialize(
        url: supabaseUrl,
        anonKey: supabaseKey,
      );
      debugPrint('✅ Supabase initialized');
    }
  } catch (e) {
    debugPrint('⚠️ Supabase initialization failed (optional): $e');
    // Continue without Supabase - Firebase is the main backend
  }

  final securityService = SecurityService();
  final parentalLinkService = ParentalLinkService();
  final subscriptionService = SubscriptionService();
  
  try {
    await FlutterWindowManager.addFlags(FlutterWindowManager.FLAG_SECURE);
  } catch (e) {
    // Window manager not available on this platform
  }
  
  if (await securityService.isDeviceCompromised()) {
    runApp(const MaterialApp(
      home: Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: Text(
            'Security Alert: Device is compromised (Rooted/Jailbroken).\nApp cannot run for your safety.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.red, fontSize: 18),
          ),
        ),
      ),
    ));
    return;
  }

  await ThreatDb().init();

  // CHECK AUTHENTICATION FIRST
  final currentUser = FirebaseAuth.instance.currentUser;
  
  Widget initialScreen;
  
  // If not authenticated, show login screen
  if (currentUser == null) {
    initialScreen = const LoginScreen();
  } else {
    // User is authenticated - check subscription
    final hasSubscription = await subscriptionService.hasActiveSubscription(currentUser.uid);
    
    if (!hasSubscription) {
      // No active subscription - show paywall
      initialScreen = const PaywallScreen();
    } else {
      // Has subscription - check role
      final role = await parentalLinkService.getUserRole();
      
      if (role == 'parent') {
        initialScreen = const ParentDashboard();
      } else if (role == 'child') {
        if (await securityService.hasUserConsented()) {
          initialScreen = const HolographicDashboard();
        } else {
          initialScreen = const ConsentScreen(nextScreen: HolographicDashboard());
        }
      } else {
        // No role selected yet
        initialScreen = RoleSelectionScreen(
          onRoleSelected: () {
            main(); 
          },
        );
      }
    }
  }

  runApp(SecurityGate(
    securityService: securityService,
    child: AntiLustGuardianApp(home: initialScreen),
  ));
}

class SecurityGate extends StatefulWidget {
  final Widget child;
  final SecurityService securityService;

  const SecurityGate({super.key, required this.child, required this.securityService});

  @override
  _SecurityGateState createState() => _SecurityGateState();
}

class _SecurityGateState extends State<SecurityGate> with WidgetsBindingObserver {
  bool _isAuthenticated = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _authenticate();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      setState(() {
        _isAuthenticated = false;
      });
      _authenticate();
    }
  }

  Future<void> _authenticate() async {
    final authenticated = await widget.securityService.authenticateUser();
    if (mounted) {
      setState(() {
        _isAuthenticated = authenticated;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_isAuthenticated) {
      return MaterialApp(
        theme: CosmicTheme.themeData,
        home: Scaffold(
          backgroundColor: CosmicTheme.deepSpace,
          body: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.lock, size: 80, color: CosmicTheme.neonCyan),
                const SizedBox(height: 20),
                Text(
                  'SYSTEM LOCKED',
                  style: CosmicTheme.headerStyle.copyWith(color: CosmicTheme.neonCyan),
                ),
              ],
            ),
          ),
        ),
      );
    }
    return widget.child;
  }
}
