"""
Test Subscription Flow - End to End Verification
Tests the complete flow from payment to app access
"""

import asyncio
import sys
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app

# Test configuration
TEST_USER_EMAIL = "test@example.com"
TEST_USER_UID = "test_uid_12345"
TEST_SUBSCRIPTION_ID = "sub_test_123"

class SubscriptionFlowTester:
    def __init__(self):
        self.passed = []
        self.failed = []
        
    def test(self, name, condition, details=""):
        """Test a condition and record result"""
        if condition:
            self.passed.append(name)
            print(f"✅ PASS: {name}")
            if details:
                print(f"   {details}")
        else:
            self.failed.append(name)
            print(f"❌ FAIL: {name}")
            if details:
                print(f"   {details}")
        print()
        
    async def test_firestore_connection(self):
        """Test 1: Verify Firestore connection"""
        print("=" * 70)
        print("TEST 1: Firestore Connection")
        print("=" * 70)
        
        try:
            from services.subscription_service import db
            self.test(
                "Firestore Connection",
                db is not None,
                f"Firestore client: {type(db).__name__ if db else 'None'}"
            )
            return db
        except Exception as e:
            self.test("Firestore Connection", False, f"Error: {e}")
            return None
    
    async def test_create_subscription(self, db):
        """Test 2: Create subscription document"""
        print("=" * 70)
        print("TEST 2: Create Subscription in Firestore")
        print("=" * 70)
        
        if not db:
            self.test("Create Subscription", False, "Firestore not available")
            return False
        
        try:
            from services.subscription_service import SubscriptionService
            
            # Create test subscription
            await SubscriptionService.store_subscription(
                user_id=TEST_USER_UID,
                subscription_id=TEST_SUBSCRIPTION_ID,
                customer_id="cus_test_123",
                price_id="price_test_monthly",
                status="active"
            )
            
            self.test(
                "Create Subscription",
                True,
                f"Created subscription for user: {TEST_USER_UID}"
            )
            return True
        except Exception as e:
            self.test("Create Subscription", False, f"Error: {e}")
            return False
    
    async def test_retrieve_subscription(self, db):
        """Test 3: Retrieve subscription from Firestore"""
        print("=" * 70)
        print("TEST 3: Retrieve Subscription")
        print("=" * 70)
        
        if not db:
            self.test("Retrieve Subscription", False, "Firestore not available")
            return None
        
        try:
            doc_ref = db.collection('subscriptions').document(TEST_USER_UID)
            doc = doc_ref.get()
            
            exists = doc.exists
            data = doc.to_dict() if exists else None
            
            self.test(
                "Retrieve Subscription",
                exists,
                f"Document exists: {exists}, Data: {data}"
            )
            return data
        except Exception as e:
            self.test("Retrieve Subscription", False, f"Error: {e}")
            return None
    
    async def test_subscription_status(self, subscription_data):
        """Test 4: Verify subscription status"""
        print("=" * 70)
        print("TEST 4: Subscription Status")
        print("=" * 70)
        
        if not subscription_data:
            self.test("Subscription Status", False, "No subscription data")
            return
        
        status = subscription_data.get('status')
        is_active = status in ['active', 'trialing']
        
        self.test(
            "Subscription Status",
            is_active,
            f"Status: '{status}' - Valid: {is_active}"
        )
    
    async def test_app_subscription_check(self):
        """Test 5: Simulate app checking subscription"""
        print("=" * 70)
        print("TEST 5: App Subscription Check (Simulated)")
        print("=" * 70)
        
        try:
            from services.subscription_service import SubscriptionService
            
            # Simulate what the app does
            has_subscription = await SubscriptionService.has_active_subscription(TEST_USER_UID)
            
            self.test(
                "App Subscription Check",
                has_subscription,
                f"hasActiveSubscription({TEST_USER_UID}): {has_subscription}"
            )
        except Exception as e:
            self.test("App Subscription Check", False, f"Error: {e}")
    
    async def test_cleanup(self, db):
        """Test 6: Cleanup test data"""
        print("=" * 70)
        print("TEST 6: Cleanup")
        print("=" * 70)
        
        if not db:
            print("⚠️  SKIP: Firestore not available")
            return
        
        try:
            doc_ref = db.collection('subscriptions').document(TEST_USER_UID)
            doc_ref.delete()
            
            print(f"✅ Test data cleaned up: {TEST_USER_UID}")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
        print()
    
    def print_summary(self):
        """Print test summary"""
        print()
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        total = len(self.passed) + len(self.failed)
        pass_rate = (len(self.passed) / total * 100) if total > 0 else 0
        
        print(f"✅ Passed: {len(self.passed)}")
        print(f"❌ Failed: {len(self.failed)}")
        print(f"📊 Success Rate: {pass_rate:.1f}%")
        print()
        
        if self.failed:
            print("Failed Tests:")
            for test in self.failed:
                print(f"  ❌ {test}")
        
        print("=" * 70)
        
        return len(self.failed) == 0

async def main():
    """Run all tests"""
    print()
    print("🧪 SUBSCRIPTION FLOW TEST SUITE")
    print("=" * 70)
    print()
    
    tester = SubscriptionFlowTester()
    
    # Run tests
    db = await tester.test_firestore_connection()
    
    if db:
        await tester.test_create_subscription(db)
        subscription_data = await tester.test_retrieve_subscription(db)
        await tester.test_subscription_status(subscription_data)
        await tester.test_app_subscription_check()
        await tester.test_cleanup(db)
    
    # Summary
    success = tester.print_summary()
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
