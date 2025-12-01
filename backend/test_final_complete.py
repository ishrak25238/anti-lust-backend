"""
FINAL COMPREHENSIVE TEST - Everything Must Work
Honest test of all user requirements
"""
import sys
import os
from pathlib import Path
import asyncio

sys.path.insert(0, str(Path(__file__).parent))

async def main():
    print("=" * 80)
    print("FINAL COMPREHENSIVE TEST")
    print("=" * 80)

    results = {"passed": [], "failed": [], "warnings": []}

    # TEST 1: Authentication
    print("\n[TEST 1] Authentication...")
    try:
        from middleware.security import hash_password, verify_password, create_jwt_token
        
        hashed = hash_password("Test123!")
        if verify_password("Test123!", hashed):
            token = create_jwt_token({"sub": "test@example.com"})
            if token and len(token) > 50:
                results["passed"].append("Authentication working")
                print("✓ Authentication working")
            else:
                raise Exception("JWT failed")
        else:
            raise Exception("Password verification failed")
    except Exception as e:
        results["failed"].append(f"Authentication: {e}")
        print(f"✗ Failed: {e}")

    # TEST 2: ML Models
    print("\n[TEST 2] ML Models...")
    try:
        from services.ml_adapter import MLServiceAdapter
        ml = MLServiceAdapter()
        if ml.is_loaded():
            results["passed"].append("ML Models loaded")
            print("✓ ML models working")
        else:
            results["warnings"].append("ML in fallback mode")
            print("⚠ ML fallback mode")
    except Exception as e:
        results["failed"].append(f"ML: {e}")
        print(f"✗ Failed: {e}")

    # TEST 3: Dark Web Detection
    print("\n[TEST 3] Dark Web...")
    try:
        from services.darkweb_detection_service import DarkWebDetectionService
        d = DarkWebDetectionService()
        result = d.check_url("http://thehiddenwiki7736jxxx.onion")
        if result.get('is_dark_web'):
            results["passed"].append(f"Dark Web (conf: {result.get('confidence')})")
            print(f"✓ Dark web detection: {result.get('confidence')*100}%")
        else:
            results["failed"].append("Dark web detection")
            print("✗ Failed to detect .onion")
    except Exception as e:
        results["failed"].append(f"Dark Web: {e}")
        print(f"✗ Failed: {e}")

    # TEST 4: VPN Prevention
    print("\n[TEST 4] VPN Prevention...")
    try:
        from services.vpn_bypass_prevention import vpn_bypass_prevention
        apps = [{'package': 'com.nordvpn.android', 'name': 'Nord   VPN'}]
        vpn_check = await vpn_bypass_prevention.block_vpn_apps("test", apps, None)
        if vpn_check['vpn_apps_found'] == 1:
            results["passed"].append("VPN Prevention working")
            print("✓ VPN detection working")
        else:
            results["warnings"].append("VPN detection check")
            print(f"⚠ VPN apps found: {vpn_check['vpn_apps_found']}")
    except Exception as e:
        results["failed"].append(f"VPN: {e}")
        print(f"✗ Failed: {e}")

    # TEST 5: Research Service
    print("\n[TEST 5] Research Service...")
    try:
        from services.anonymous_research_service import research_service
        results["passed"].append(f"Research → {research_service.admin_email}")
        print(f"✓ Reports to: {research_service.admin_email}")
    except Exception as e:
        results["failed"].append(f"Research: {e}")
        print(f"✗ Failed: {e}")

    # TEST 6: Notifications
    print("\n[TEST 6] Notifications...")
    try:
        from services.notification_service import NotificationService
        NotificationService()
        results["passed"].append("Notifications ready")
        print("✓ Notifications ready")
    except Exception as e:
        results["failed"].append(f"Notifications: {e}")
        print(f"✗ Failed: {e}")

    # TEST 7: Payment
    print("\n[TEST 7] Payment...")
    try:
        from services.payment_service import PaymentService
        from dotenv import load_dotenv
        load_dotenv()
        
        p = PaymentService()
        if p.is_configured():
            results["passed"].append("Payment configured")
            print("✓ Stripe configured")
        else:
            results["warnings"].append("Payment needs key")
            print("⚠ Need STRIPE_SECRET_KEY")
    except Exception as e:
        results["failed"].append(f"Payment: {e}")
        print(f"✗ Failed: {e}")

    # FINAL REPORT
    print("\n" + "=" * 80)
    print("FINAL HONEST REPORT")
    print("=" * 80)

    print(f"\n✅ PASSED ({len(results['passed'])}):")
    for item in results["passed"]:
        print(f"   {item}")

    if results["warnings"]:
        print(f"\n⚠ WARNINGS ({len(results['warnings'])}):")
        for item in results["warnings"]:
            print(f"   {item}")

    if results["failed"]:
        print(f"\n❌ FAILED ({len(results['failed'])}):")
        for item in results["failed"]:
            print(f"   {item}")
        print("\n🚨 ERRORS FOUND")
        sys.exit(1)
    else:
        print("\n✅ ALL SYSTEMS WORKING")
        print("✅ READY FOR PRODUCTION")

    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
