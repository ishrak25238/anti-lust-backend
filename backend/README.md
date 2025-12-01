# 🚀 Quick Start Guide - Anti-Lust Guardian Backend (SECURE VERSION)

## ⚡ Installation

### 1. Clone & Install
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example
cp .env.example .env

# Generate secure secrets
python -c "import secrets; print('API_SECRET_KEY=' + secrets.token_urlsafe(32))" >> .env
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe( 32))" >> .env
python -c "import secrets; print('ML_API_KEYS=' + secrets.token_urlsafe(32))" >> .env

# Edit .env and add:
# - Stripe keys
# - Email configuration  
# - Allowed origins
```

### 3. Initialize Database
```bash
python migrations/add_security_tables.py
```

### 4. Start Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

---

## 🔑 API Authentication

All ML endpoints require API key authentication:

```bash
# Set X-API-Key header
curl -H "X-API-Key: YOUR_KEY" \
  -X POST http://localhost:8000/api/ml/nsfw-check \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "..."}'
```

---

## 📋 Available Endpoints

### Health & Monitoring
- `GET /` - Service info
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /api/stats/ml` - ML service statistics

### ML Detection (Requires API Key)
- `POST /api/ml/nsfw-check` - NSFW image detection
- `POST /api/ml/classify-text` - Text toxicity classification
- `POST /api/ml/threat-url` - URL threat analysis

### Pattern Analysis (Requires API Key)
- `GET /api/patterns/analysis/{device_id}?days=7` - Get behavioral patterns
- `POST /api/patterns/false-positive` - Report false positive

### Parent-Child Sync
- `POST /api/pairing/link` - Link parent to child device
- `POST /api/logs/push` - Push child logs
- `GET /api/logs/fetch/{parent_email}` - Fetch child logs for parent

### Payment
- `POST /api/payment/create-intent` - Create Stripe payment
- `POST /api/payment/confirm` - Confirm payment

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run security tests only
pytest tests/test_security.py -v

# Run pattern analysis tests
pytest tests/test_pattern_analysis.py -v
```

---

## 🔒 Security Features

✅ **API Key Authentication** on all ML endpoints  
✅ **Rate Limiting** (100 requests/minute)  
✅ **Input Validation** (10MB image limit, 10K char text limit)  
✅ **Security Headers** (HSTS, CSP, X-Frame-Options, etc.)  
✅ **CORS** restricted to allowed origins  
✅ **Audit Logging** for all security events  
✅ **SQL Injection Prevention** (parameterized queries)  
✅ **XSS Prevention** (input sanitization)  

---

## 📊 Monitoring

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

Metrics include:
- Request count by endpoint
- Request latency (p50, p95, p99)
- ML prediction count and duration
- Authentication failures
- Rate limit violations

### Audit Logs
```sql
-- View recent auth failures
SELECT * FROM audit_logs 
WHERE event_type = 'auth_failure' 
ORDER BY timestamp DESC 
LIMIT 10;

-- View API usage by endpoint
SELECT resource, COUNT(*) as count
FROM audit_logs 
WHERE event_type = 'api_access'
GROUP BY resource 
ORDER BY count DESC;
```

---

## 🎯 Quick Test

```bash
# Health check (no auth required)
curl http://localhost:8000/health

# ML service stats (requires API key)
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:8000/api/stats/ml

# Pattern analysis (requires API key)
curl -H "X-API-Key: YOUR_KEY" \
  http://localhost:8000/api/patterns/analysis/device_001?days=7
```

---

## 📚 Documentation

- [SECURITY.md](SECURITY.md) - Security best practices
- [ML_PATTERN_WORKFLOW.md](ML_PATTERN_WORKFLOW.md) - Pattern analysis documentation
- [ML_SYSTEM_DOCS.md](ML_SYSTEM_DOCS.md) - ML system overview

---

## ⚠️ Before Production

See [SECURITY.md](SECURITY.md) deployment checklist:

1. ✅ Set strong secrets in `.env`
2. ✅ Configure CORS to specific origins
3. ✅ Use PostgreSQL (not SQLite)
4. ✅ Deploy behind HTTPS reverse proxy
5. ✅ Set up monitoring (Sentry, Prometheus)
6. ✅ Configure backup schedule
7. ✅ Review security checklist

---

## 🆘 Troubleshooting

### "API key required"
Add `X-API-Key` header with valid key from `.env:ML_API_KEYS`

### "Rate limit exceeded"
Wait 1 minute or increase `RATE_LIMIT_PER_MINUTE` in `.env`

### "Image size exceeds limit"
Images must be < 10MB. Adjust `MAX_IMAGE_SIZE_MB` if needed

### Database errors
Run migration: `python migrations/add_security_tables.py`

---

## 📞 Support

For issues or questions:
1. Check [SECURITY.md](SECURITY.md) and [ML_PATTERN_WORKFLOW.md](ML_PATTERN_WORKFLOW.md)
2. Review audit logs for errors
3. Check Prometheus metrics for anomalies
