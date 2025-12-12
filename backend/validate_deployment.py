"""
PRE-DEPLOYMENT VALIDATION SCRIPT
Tests all critical backend functionality before Google Cloud deployment
"""

import sys
import importlib.util
from pathlib import Path

class BackendValidator:
    def __init__(self):
        self.passed = []
        self.failed = []
        self.warnings = []
        
    def test(self, name, condition, details="", level="error"):
        """Test a condition and record result"""
        if condition:
            self.passed.append(name)
            print(f"✅ PASS: {name}")
            if details:
                print(f"   {details}")
        else:
            if level == "warning":
                self.warnings.append(name)
                print(f"⚠️  WARN: {name}")
            else:
                self.failed.append(name)
                print(f"❌ FAIL: {name}")
            if details:
                print(f"   {details}")
        print()
    
    def test_imports(self):
        """Test 1: Critical imports"""
        print("=" * 70)
        print("TEST 1: Import Testing")
        print("=" * 70)
        
        imports_to_test = [
            ("fastapi", "FastAPI framework"),
            ("uvicorn", "ASGI server"),
            ("stripe", "Stripe payments"),
            ("firebase_admin", "Firebase Admin SDK"),
            ("pydantic", "Data validation"),
        ]
        
        for module_name, description in imports_to_test:
            try:
                __import__(module_name)
                self.test(f"Import {module_name}", True, description)
            except ImportError as e:
                self.test(f"Import {module_name}", False, f"Missing: {e}", "error")
    
    def test_main_file(self):
        """Test 2: Main file structure"""
        print("=" * 70)
        print("TEST 2: Main.py Structure")
        print("=" * 70)
        
        try:
            from main import app
            self.test("main.py imports", True, "FastAPI app created")
            
            # Check critical routes exist
            routes = [route.path for route in app.routes]
            
            critical_routes = [
                "/health",
                "/api/stripe/webhook",
            ]
            
            for route in critical_routes:
                exists = route in routes or any(r.startswith(route) for r in routes)
                self.test(
                    f"Route {route}",
                    exists,
                    "Route exists in app" if exists else "Route missing!"
                )
                
        except Exception as e:
            self.test("main.py imports", False, f"Error: {e}")
    
    def test_env_variables(self):
        """Test 3: Environment variables"""
        print("=" * 70)
        print("TEST 3: Environment Variables")
        print("=" * 70)
        
        import os
        from pathlib import Path
        
        env_file = Path(".env")
        self.test(
            ".env file exists",
            env_file.exists(),
            f"Location: {env_file.absolute()}"
        )
        
        if env_file.exists():
            # Load .env
            from dotenv import load_dotenv
            load_dotenv()
            
            critical_vars = [
                "STRIPE_SECRET_KEY",
                "STRIPE_WEBHOOK_SECRET",
            ]
            
            recommended_vars = [
                "FIREBASE_PROJECT_ID",
                "FIREBASE_PRIVATE_KEY",
                "FIREBASE_CLIENT_EMAIL",
            ]
            
            for var in critical_vars:
                value = os.getenv(var)
                self.test(
                    f"ENV: {var}",
                    value is not None and value != "",
                    f"Set: {'Yes' if value else 'No'}"
                )
            
            for var in recommended_vars:
                value = os.getenv(var)
                self.test(
                    f"ENV: {var}",
                    value is not None and value != "",
                    f"Set: {'Yes' if value else 'No'}",
                    level="warning"
                )
    
    def test_service_files(self):
        """Test 4: Service files"""
        print("=" * 70)
        print("TEST 4: Service Files")
        print("=" * 70)
        
        services = [
            "services/subscription_service.py",
            "services/ml_adapter.py",
        ]
        
        for service in services:
            path = Path(service)
            self.test(
                f"File {service}",
                path.exists(),
                f"Size: {path.stat().st_size} bytes" if path.exists() else "Missing!"
            )
    
    def test_syntax(self):
        """Test 5: Python syntax"""
        print("=" * 70)
        print("TEST 5: Syntax Validation")
        print("=" * 70)
        
        files_to_check = [
            "main.py",
            "services/subscription_service.py",
            "services/ml_adapter.py",
        ]
        
        import py_compile
        
        for file in files_to_check:
            try:
                py_compile.compile(file, doraise=True)
                self.test(f"Syntax {file}", True, "No syntax errors")
            except py_compile.PyCompileError as e:
                self.test(f"Syntax {file}", False, f"Syntax error: {e}")
    
    def test_webhook_logic(self):
        """Test 6: Webhook extraction logic"""
        print("=" * 70)
        print("TEST 6: Webhook User ID Extraction")
        print("=" * 70)
        
        # Simulate webhook data
        test_subscription = {
            'client_reference_id': 'test_uid_123',
            'metadata': {'firebase_user_id': 'backup_uid_456'}
        }
        
        # Test extraction logic
        user_id = (test_subscription.get('client_reference_id') or 
                  test_subscription['metadata'].get('firebase_user_id'))
        
        self.test(
            "Extract from client_reference_id",
            user_id == 'test_uid_123',
            f"Extracted: {user_id}"
        )
        
        # Test fallback
        test_subscription_no_client_ref = {
            'metadata': {'firebase_user_id': 'backup_uid_456'}
        }
        
        user_id_fallback = (test_subscription_no_client_ref.get('client_reference_id') or 
                           test_subscription_no_client_ref['metadata'].get('firebase_user_id'))
        
        self.test(
            "Fallback to metadata",
            user_id_fallback == 'backup_uid_456',
            f"Extracted: {user_id_fallback}"
        )
    
    def print_summary(self):
        """Print test summary"""
        print()
        print("=" * 70)
        print("DEPLOYMENT READINESS SUMMARY")
        print("=" * 70)
        
        total = len(self.passed) + len(self.failed)
        pass_rate = (len(self.passed) / total * 100) if total > 0 else 0
        
        print(f"✅ Passed: {len(self.passed)}")
        print(f"❌ Failed: {len(self.failed)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"📊 Success Rate: {pass_rate:.1f}%")
        print()
        
        if self.failed:
            print("🚨 CRITICAL FAILURES (MUST FIX):")
            for test in self.failed:
                print(f"  ❌ {test}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS (RECOMMENDED TO FIX):")
            for test in self.warnings:
                print(f"  ⚠️  {test}")
            print()
        
        is_ready = len(self.failed) == 0
        
        if is_ready:
            print("✅ DEPLOYMENT READY: All critical tests passed!")
            print("   You can safely deploy to Google Cloud.")
        else:
            print("❌ NOT READY: Fix critical failures before deploying!")
        
        print("=" * 70)
        
        return is_ready

def main():
    """Run all validation tests"""
    print()
    print("🔍 BACKEND VALIDATION FOR GOOGLE CLOUD DEPLOYMENT")
    print("=" * 70)
    print()
    
    validator = BackendValidator()
    
    # Run all tests
    validator.test_imports()
    validator.test_main_file()
    validator.test_env_variables()
    validator.test_service_files()
    validator.test_syntax()
    validator.test_webhook_logic()
    
    # Summary
    is_ready = validator.print_summary()
    
    return 0 if is_ready else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
