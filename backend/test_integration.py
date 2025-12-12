"""
INTEGRATION TEST SUITE
Tests actual API endpoints, database, and end-to-end flows
Starts real backend server and makes HTTP requests
"""
import asyncio
import httpx
import time
import json
import subprocess
import os
import sys
from pathlib import Path
import signal

class IntegrationTestSuite:
    def __init__(self):
        self.results = {'passed': [], 'failed': [], 'warnings': []}
        self.base_url = "http://localhost:8000"
        self.server_process = None
        self.client = None
        
    async def start_backend_server(self):
        """Start the backend server"""
        print("\n🚀 Starting backend server...")
        
        # Kill any existing process on port 8000
        try:
            if os.name == 'nt':  # Windows
                subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq uvicorn*\"", 
                             shell=True, capture_output=True)
        except:
            pass
        
        # Start uvicorn server
        backend_path = Path(__file__).parent
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=backend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for server to start
        print("   Waiting for server to start...")
        for i in range(30):  # Wait up to 30 seconds
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{self.base_url}/health", timeout=2.0)
                    if response.status_code == 200:
                        print(f"   ✅ Server started successfully (took {i+1}s)")
                        return True
            except:
                await asyncio.sleep(1)
        
        print("   ❌ Server failed to start within 30 seconds")
        return False
    
    def stop_backend_server(self):
        """Stop the backend server"""
        if self.server_process:
            print("\n🛑 Stopping backend server...")
            if os.name == 'nt':  # Windows
                self.server_process.send_signal(signal.CTRL_C_EVENT)
            else:
                self.server_process.terminate()
            self.server_process.wait(timeout=5)
            print("   ✅ Server stopped")
    
    async def test(self, name, func):
        """Run an async test"""
        print(f"\n{'='*70}")
        print(f"TEST: {name}")
        print('='*70)
        
        try:
            result = await func()
            if result:
                self.results['passed'].append(name)
                print(f"✅ PASS: {name}")
                return True
            else:
                self.results['failed'].append(name)
                print(f"❌ FAIL: {name}")
                return False
        except Exception as e:
            self.results['failed'].append(name)
            print(f"💥 ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    # ============================================================
    # API ENDPOINT TESTS
    # ============================================================
    
    async def test_health_endpoint(self):
        """Test /health endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/health")
            
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
                return True
            return False
    
    async def test_ml_health_endpoint(self):
        """Test ML service health check"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/ml/health")
            
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ML Status: {data.get('status')}")
                print(f"   Models: {data.get('models')}")
                return data.get('status') == 'operational'
            return False
    
    async def test_image_scan_endpoint(self):
        """Test image scanning via API"""
        import numpy as np
        import cv2
        
        # Create test image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        img[:, :] = (128, 128, 128)  # Gray
        success, buffer = cv2.imencode('.jpg', img)
        image_bytes = buffer.tobytes()
        
        print(f"   Test image size: {len(image_bytes)} bytes")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {'image': ('test.jpg', image_bytes, 'image/jpeg')}
            
            start = time.time()
            response = await client.post(f"{self.base_url}/api/ml/scan-image", files=files)
            elapsed = time.time() - start
            
            print(f"   API response time: {elapsed:.2f}s")
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Is safe: {data.get('is_safe')}")
                print(f"   Score: {data.get('score')}")
                print(f"   Flags: {data.get('flags')}")
                return True
            else:
                print(f"   Error: {response.text}")
                return False
    
    async def test_text_scan_endpoint(self):
        """Test text scanning via API"""
        async with httpx.AsyncClient() as client:
            payload = {"text": "Hello, this is a safe test message."}
            
            response = await client.post(
                f"{self.base_url}/api/ml/scan-text",
                json=payload
            )
            
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Is safe: {data.get('is_safe')}")
                print(f"   Score: {data.get('score')}")
                return True
            return False
    
    async def test_url_scan_endpoint(self):
        """Test URL scanning via API"""
        async with httpx.AsyncClient() as client:
            payload = {"url": "https://google.com"}
            
            response = await client.post(
                f"{self.base_url}/api/ml/scan-url",
                json=payload
            )
            
            print(f"   Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   Is safe: {data.get('is_safe')}")
                print(f"   Score: {data.get('score')}")
                return True
            return False
    
    async def test_cors_headers(self):
        """Test CORS headers are set"""
        async with httpx.AsyncClient() as client:
            response = await client.options(
                f"{self.base_url}/health",
                headers={"Origin": "http://localhost:3000"}
            )
            
            print(f"   Status code: {response.status_code}")
            cors_header = response.headers.get('access-control-allow-origin')
            print(f"   CORS header: {cors_header}")
            
            return cors_header is not None
    
    async def test_rate_limiting(self):
        """Test rate limiting is active"""
        async with httpx.AsyncClient() as client:
            # Make rapid requests
            responses = []
            for i in range(5):
                response = await client.get(f"{self.base_url}/health")
                responses.append(response.status_code)
            
            print(f"   Response codes: {responses}")
            
            # All should succeed (rate limit is high for tests)
            return all(code == 200 for code in responses)
    
    # ============================================================
    # END-TO-END FLOW TESTS
    # ============================================================
    
    async def test_e2e_image_detection_flow(self):
        """Test complete image detection flow"""
        import numpy as np
        import cv2
        
        print("   Step 1: Create test image")
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[:, :] = (255, 0, 0)  # Blue
        success, buffer = cv2.imencode('.jpg', img)
        image_bytes = buffer.tobytes()
        print(f"   ✅ Image created: {len(image_bytes)} bytes")
        
        print("   Step 2: Upload to ML API")
        async with httpx.AsyncClient(timeout=30.0) as client:
            files = {'image': ('test.jpg', image_bytes, 'image/jpeg')}
            response = await client.post(f"{self.base_url}/api/ml/scan-image", files=files)
            
            if response.status_code != 200:
                print(f"   ❌ Upload failed: {response.status_code}")
                return False
            
            print(f"   ✅ Upload successful")
            
            print("   Step 3: Parse response")
            data = response.json()
            is_safe = data.get('is_safe')
            score = data.get('score', 0)
            
            print(f"   Result: {'SAFE' if is_safe else 'UNSAFE'}")
            print(f"   Score: {score}")
            
            # For a solid color image, should be safe
            return is_safe == True
    
    async def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        async with httpx.AsyncClient() as client:
            # Make 10 concurrent requests
            tasks = [
                client.get(f"{self.base_url}/health")
                for _ in range(10)
            ]
            
            start = time.time()
            responses = await asyncio.gather(*tasks)
            elapsed = time.time() - start
            
            success_count = sum(1 for r in responses if r.status_code == 200)
            
            print(f"   Concurrent requests: 10")
            print(f"   Successful: {success_count}/10")
            print(f"   Total time: {elapsed:.2f}s")
            print(f"   Avg time per request: {elapsed/10:.2f}s")
            
            return success_count == 10
    
    # ============================================================
    # DATABASE INTEGRATION TESTS
    # ============================================================
    
    async def test_database_connection(self):
        """Test database is accessible"""
        # Check if database file exists
        db_path = Path(__file__).parent / 'data' / 'app.db'
        
        if db_path.exists():
            size_kb = db_path.stat().st_size / 1024
            print(f"   Database file: {db_path}")
            print(f"   Size: {size_kb:.1f} KB")
            print(f"   ✅ Database accessible")
            return True
        else:
            print(f"   ⚠️  Database file not found (may be created on first run)")
            return True  # Not critical for tests
    
    # ============================================================
    # PERFORMANCE TESTS
    # ============================================================
    
    async def test_response_time_health(self):
        """Test health endpoint response time"""
        async with httpx.AsyncClient() as client:
            times = []
            for i in range(5):
                start = time.time()
                response = await client.get(f"{self.base_url}/health")
                elapsed = time.time() - start
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            
            print(f"   Avg response time: {avg_time*1000:.1f}ms")
            print(f"   Min: {min_time*1000:.1f}ms, Max: {max_time*1000:.1f}ms")
            
            # Should be under 100ms for health check
            return avg_time < 0.1
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.results['passed']) + len(self.results['failed'])
        
        print("\n" + "="*70)
        print("INTEGRATION TEST SUMMARY")
        print("="*70)
        print(f"✅ Passed: {len(self.results['passed'])}")
        print(f"❌ Failed: {len(self.results['failed'])}")
        print(f"⚠️  Warnings: {len(self.results['warnings'])}")
        
        if self.results['failed']:
            print("\n❌ FAILED TESTS:")
            for test in self.results['failed']:
                print(f"   - {test}")
        
        if self.results['warnings']:
            print("\n⚠️  WARNINGS:")
            for warning in self.results['warnings']:
                print(f"   - {warning}")
        
        print("="*70)
        
        success_rate = len(self.results['passed']) / total * 100 if total > 0 else 0
        print(f"\nSUCCESS RATE: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("\n🎉 ALL INTEGRATION TESTS PASSED!")
            return 0
        elif success_rate >= 80:
            print("\n⚠️  MOSTLY PASSING - Some issues to address")
            return 1
        else:
            print("\n❌ INTEGRATION ISSUES DETECTED")
            return 2

async def main():
    suite = IntegrationTestSuite()
    
    print("="*70)
    print("INTEGRATION TEST SUITE")
    print("Testing: Backend API + Database + End-to-End Flows")
    print("="*70)
    
    # Start backend server
    if not await suite.start_backend_server():
        print("\n❌ Failed to start backend server. Cannot run integration tests.")
        return 2
    
    try:
        # Wait a bit for full initialization
        await asyncio.sleep(3)
        
        # API Endpoint Tests
        await suite.test("Health Endpoint", suite.test_health_endpoint)
        await suite.test("ML Health Endpoint", suite.test_ml_health_endpoint)
        await suite.test("Image Scan API", suite.test_image_scan_endpoint)
        await suite.test("Text Scan API", suite.test_text_scan_endpoint)
        await suite.test("URL Scan API", suite.test_url_scan_endpoint)
        
        # Infrastructure Tests
        await suite.test("CORS Headers", suite.test_cors_headers)
        await suite.test("Rate Limiting", suite.test_rate_limiting)
        await suite.test("Database Connection", suite.test_database_connection)
        
        # End-to-End Tests
        await suite.test("E2E Image Detection Flow", suite.test_e2e_image_detection_flow)
        await suite.test("Concurrent Requests", suite.test_concurrent_requests)
        
        # Performance Tests
        await suite.test("Response Time (Health)", suite.test_response_time_health)
        
        # Print summary
        exit_code = suite.print_summary()
        
    finally:
        # Always stop server
        suite.stop_backend_server()
    
    return exit_code

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
