# START THE SERVER

Run this command to start the Anti-Lust Guardian backend:

```bash
cd "E:\Anti-Lust app\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Server will be at**: `http://localhost:8000`

---

## Quick Test

Once started, open in browser: `http://localhost:8000`

You should see:
```json
{
  "service": "Anti-Lust Guardian API",
  "status": "operational",
  "version": "1.0.0"
}
```

---

## Your API Key

```
MKO4K06joZ9HVaG-znFkW3S_22wvUFsIevu6hyYHjEk
```

Use this in all API requests as header: `X-API-Key`

---

**Everything is ready to go!** ✅
