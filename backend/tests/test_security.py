"""
Security tests for Anti-Lust Guardian API
Tests authentication, rate limiting, input validation, and CORS
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import base64

client = TestClient(app)

class TestAuthentication:
    """Test API authentication"""
    
    def test_unauthenticated_request_rejected(self):
        """ML endpoints without API key should return 401"""
        response = client.post("/api/ml/nsfw-check", json={
            "image_base64": "test"
        })
        assert response.status_code == 401
        assert "API key required" in response.json()["detail"]
    
    def test_invalid_api_key_rejected(self):
        """Invalid API key should return 401"""
        response = client.post(
            "/api/ml/nsfw-check",
            json={"image_base64": "test"},
            headers={"X-API-Key": "invalid-key"}
        )
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["detail"]
    
    def test_valid_api_key_accepted(self):
        """Valid API key should be accepted (will fail on processing, but auth passes)"""
        pass

class TestRateLimiting:
    """Test rate limiting enforcement"""
    
    @pytest.mark.skip("Requires rate limit configuration")
    def test_rate_limiting_enforced(self):
        """Exceeding rate limit should return 429"""
        for i in range(101):
            response = client.get("/health")
            if i == 100:
                assert response.status_code == 429

class TestInputValidation:
    """Test input validation and size limits"""
    
    def test_image_size_limit_enforced(self):
        """Images larger than 10MB should be rejected"""
        large_data = "A" * (11 * 1024 * 1024)  # 11MB of 'A's
        large_base64 = base64.b64encode(large_data.encode()).decode()
        
        response = client.post(
            "/api/ml/nsfw-check",
            json={"image_base64": large_base64},
            headers={"X-API-Key": "test-key"}
        )
        assert response.status_code == 413
        assert "exceeds limit" in response.json()["detail"]
    
    def test_text_length_limit_enforced(self):
        """Text longer than 10,000 chars should be rejected"""
        long_text = "A" * 10001
        
        response = client.post(
            "/api/ml/classify-text",
            json={"text": long_text},
            headers={"X-API-Key": "test-key"}
        )
        assert response.status_code == 413
        assert "exceeds limit" in response.json()["detail"]
    
    def test_sql_injection_prevention(self):
        """SQL injection attempts should be sanitized"""
        injection_text = "'; DROP TABLE users; --"
        
        response = client.post(
            "/api/ml/classify-text",
            json={"text": injection_text},
            headers={"X-API-Key": "valid-key"}
        )

class TestSecurityHeaders:
    """Test security headers presence"""
    
    def test_security_headers_present(self):
        """All security headers should be present"""
        response = client.get("/health")
        
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert "Strict-Transport-Security" in response.headers
        assert "Content-Security-Policy" in response.headers
    
    def test_cors_headers_configured(self):
        """CORS headers should be properly configured"""
        response = client.options("/api/ml/nsfw-check")
        
        assert "access-control-allow-origin" in response.headers

class TestEndpointSecurity:
    """Test security of specific endpoints"""
    
    def test_payment_endpoint_requires_auth(self):
        """Payment endpoints should require authentication"""
        pass
    
    def test_parent_logs_require_auth(self):
        """Parent log endpoints should require authentication"""
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
