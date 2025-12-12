"""
Test Critical Backend Files - ML and Core Services
"""
import sys

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def test_import(module_path, description):
    """Test importing a module"""
    print(f"\nTesting: {description}")
    print(f"  File: {module_path}")
    try:
        __import__(module_path.replace('/', '.').replace('\\', '.').rstrip('.py'))
        print(f"  [OK] Import successful")
        return True
    except Exception as e:
        print(f"  [ERROR] {type(e).__name__}: {e}")
        return False

def main():
    print("="*80)
    print("CRITICAL FILES IMPORT TEST")
    print("="*80)
    
    critical_files = [
        # Core ML Files
        ("services.ml_core", "ML Core - Main ML Engine"),
        ("services.ml_service", "ML Service - ML API Layer"),
        ("services.ml_evaluation", "ML Evaluation - Model Testing"),
        ("services.ml_training", "ML Training - Model Training Pipeline"),
        ("services.ml_data", "ML Data - Training Data Management"),
        
        # Notification System
        ("services.notification_service", "Notification Service"),
        ("services.notification_providers", "Notification Providers"),
        ("services.notification_data", "Notification Templates"),
        ("services.email_service", "Email Service"),
        
        # Parent/Security
        ("services.parent_child_service", "Parent-Child Control"),
        ("services.security_service", "Security & VPN Detection"),
        ("services.vpn_detection_service", "VPN Detection"),
        ("services.darkweb_detection_service", "Dark Web Detection"),
        
        # Core Backend
        ("database", "Database Models"),
        ("main", "FastAPI Main Application"),
        
        # Payment & Subscription
        ("services.payment_service", "Payment Service"),
        ("services.subscription_service", "Subscription Management"),
        
        # Analytics & Reporting
        ("services.advanced_analytics", "Advanced Analytics"),
        ("services.realtime_dashboard", "Real-time Dashboard"),
        ("services.monthly_report_service", "Monthly Reports"),
        
        # Additional Services
        ("services.pattern_storage", "Pattern Storage"),
        ("services.pattern_learning_engine", "Pattern Learning"),
        ("services.wellness_coach", "Wellness Coach AI"),
        ("services.gamification_engine", "Gamification System"),
    ]
    
    results = {'passed': 0, 'failed': 0, 'errors': []}
    
    for module, description in critical_files:
        success = test_import(module, description)
        if success:
            results['passed'] += 1
        else:
            results['failed'] += 1
            results['errors'].append(description)
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total tested: {len(critical_files)}")
    print(f"[PASS] Passed: {results['passed']}")
    print(f"[FAIL] Failed: {results['failed']}")
    
    if results['failed'] > 0:
        print(f"\nFailed imports:")
        for err in results['errors']:
            print(f"  - {err}")
        print("\n[CRITICAL] Some imports failed!")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All critical files imported successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
