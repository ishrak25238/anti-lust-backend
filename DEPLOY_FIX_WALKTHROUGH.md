# Build Error Fix Walkthrough

## Issue
The build failed on Render with `KeyError: '__version__'` during `pip install`.
This was caused by **Python 3.13** being used by default, which has compatibility issues with some older Python packages (likely `python-multipart` or `python-jose` build backends).

## Fixes Applied

### 1. Enforced Python 3.11.9
Created `runtime.txt` in the **root directory** of the repository.
```text
python-3.11.9
```
This tells Render to use Python 3.11 instead of the default 3.13.

### 2. Upgraded Dependencies
Updated `backend/requirements.txt` to use a newer version of `python-multipart`.
```diff
-python-multipart==0.0.6
+python-multipart==0.0.9
```
This ensures better compatibility with modern build environments.

### 3. Added Root Configuration
Created `render.yaml` in the **root directory** to correctly configure the service if you are deploying from the repository root.
```yaml
services:
  - type: web
    name: anti-lust-guardian-api
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.9
```

## Next Steps for You
1. **Push these changes to GitHub**:
   ```bash
   git add .
   git commit -m "Fix build error: Force Python 3.11 and upgrade deps"
   git push
   ```
2. **Trigger a Manual Deploy** (if not automatic) in the Render Dashboard.
3. **Verify**: Check the logs. The build should now use Python 3.11 and succeed.

> [!NOTE]
> If the build still fails, check your Render Service Settings > Environment Variables and ensure `PYTHON_VERSION` is NOT set to `3.13`. If it is, delete it or set it to `3.11.9`.
