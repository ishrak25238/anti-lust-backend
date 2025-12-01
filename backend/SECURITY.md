# Anti-Lust Guardian Backend - Security Best Practices

## 🔒 Security Overview

This backend implements **enterprise-grade security** with the following layers:

### Authentication & Authorization
- **API Key Authentication**: All ML endpoints require X-API-Key header
- **JWT Token Authentication**: Parent/child endpoints use JWT tokens
- **Rate Limiting**: 100 requests/minute per client
- **Input Validation**: Size limits and sanitization on all inputs

### Security Headers
All responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`
- `Content-Security-Policy: default-src 'self'`

### Data Protection
- Secrets stored in environment variables (.env)
- Database encryption at rest
- API keys hashed before storage
- Audit logging for all security events

---

## 🚀 Deployment Checklist

### Before Going to Production

#### 1. Environment Variables
```bash
# Generate secure secrets
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set in .env (NEVER commit .env to git!)
API_SECRET_KEY=<generated-secret>
JWT_SECRET_KEY=<another-generated-secret>
ML_API_KEYS=<api-key-1>,<api-key-2>,<api-key-3>
```

#### 2. CORS Configuration
```bash
# Set allowed origins (NO wildcards!)
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

#### 3. Database Security
```bash
# Use PostgreSQL in production (more secure than SQLite)
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname?ssl=require
```

#### 4. HTTPS Only
- Deploy behind reverse proxy (Nginx/Caddy)
- Enforce HTTPS redirect
- Use Let's Encrypt for SSL certificates

#### 5. Rate Limiting
```bash
# Adjust based on expected traffic
RATE_LIMIT_PER_MINUTE=100
```

#### 6. Monitoring
```bash
# Set up Sentry for error tracking
SENTRY_DSN=https://...@sentry.io/...

# Prometheus for metrics
PROMETHEUS_PORT=9090
```

---

## 🔑 API Key Management

### Generating API Keys
```bash
# Generate a secure API key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Adding API Keys
```bash
# Add to .env (comma-separated)
ML_API_KEYS=key1,key2,key3
```

### Using API Keys
```bash
# Include in request headers
curl -H "X-API-Key: YOUR_API_KEY" \
  -X POST https://api.example.com/api/ml/nsfw-check \
  -d '{"image_base64": "..."}'
```

### Rotating API Keys
1. Generate new key
2. Add to `ML_API_KEYS` list
3. Distribute to clients
4. Monitor usage
5. Remove old key after migration

---

## 🛡️ Security Audit Checklist

Use this checklist before deployment:

- [ ] All secrets in environment variables (not hardcoded)
- [ ] `.env` file in `.gitignore`
- [ ] No secrets in git history
- [ ] CORS restricted to known origins (no wildcards)
- [ ] HTTPS enforced in production
- [ ] API key authentication on all ML endpoints
- [ ] JWT authentication on parent/child endpoints
- [ ] Rate limiting configured and tested
- [ ] Input validation on all endpoints
- [ ] Security headers on all responses
- [ ] Database connections encrypted (SSL/TLS)
- [ ] Audit logging enabled
- [ ] Monitoring and alerting configured
- [ ] Error messages don't leak sensitive info
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection on state-changing operations

---

## 📊 Monitoring & Logging

### Prometheus Metrics
Access at: `http://localhost:8000/metrics`

Metrics exported:
- Request count by endpoint
- Request latency (p50, p95, p99)
- ML prediction count and latency
- Authentication failures
- Rate limit violations

### Audit Logging
All security events are logged to `audit_logs` table:
- Authentication attempts
- API access
- Data access (who viewed what)
- Configuration changes
- Payment transactions

Query logs:
```sql
SELECT * FROM audit_logs 
WHERE event_type = 'auth_failure' 
ORDER BY timestamp DESC 
LIMIT 10;
```

---

## 🚨 Incident Response

### Suspected API Key Compromise
1. Immediately remove key from `ML_API_KEYS`
2. Check audit logs for unauthorized usage
3. Generate and distribute new key
4. Notify affected clients

### Suspicious Activity
1. Check audit logs:
   ```sql
   SELECT * FROM audit_logs 
   WHERE ip_address = 'SUSPICIOUS_IP' 
   ORDER BY timestamp DESC;
   ```

2. Block IP if malicious (configure at reverse proxy level)

3. Review rate limit violations:
   ```sql
   SELECT ip_address, COUNT(*) as attempts
   FROM audit_logs 
   WHERE result = 'failure'
   GROUP BY ip_address 
   ORDER BY attempts DESC;
   ```

---

## 🔐 Password & Secret Management

### Never Do This ❌
```python
# Hardcoded secrets
stripe.api_key = "sk_live_abc123..."  # WRONG!
```

### Always Do This ✅
```python
# Environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
```

### Secret Rotation
1. Generate new secret
2. Update in environment
3. Restart service
4. Verify old secret no longer works

---

## 📝 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Guide](https://fastapi.tiangolo.com/tutorial/security/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Security Headers](https://securityheaders.com/)
