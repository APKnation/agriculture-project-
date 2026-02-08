# 🔧 Render Deployment Troubleshooting Guide

## ❌ Error: "subprocess-exited-with-error"

This error occurs during the build process when pip fails to install dependencies.

### 🚀 Quick Fix Solutions

#### Solution 1: Use Minimal Requirements (Recommended)
1. Replace `requirements.txt` with `requirements-minimal.txt`
2. Update render.yaml to use minimal requirements:

```yaml
buildCommand: "python -m pip install --upgrade pip && pip install -r requirements-minimal.txt"
```

#### Solution 2: Use Simple Configuration
1. Use `render-simple.yaml` instead of `render.yaml`
2. This uses Django's built-in server instead of Gunicorn
3. Removes Redis dependency that might cause issues

#### Solution 3: Manual Build Commands
Update render.yaml build command:

```yaml
buildCommand: |
  python -m pip install --upgrade pip
  pip install Django==5.2.10
  pip install gunicorn==21.2.0
  pip install whitenoise==6.6.0
  pip install dj-database-url==2.1.0
  pip install djangorestframework==3.15.2
  pip install djangorestframework-simplejwt==5.3.0
  pip install django-filter==24.3
  pip install django-cors-headers==4.4.0
  pip install Pillow==10.2.0
  pip install requests==2.31.0
```

### 🔍 Common Causes

#### 1. Package Version Conflicts
- Django and DRF version mismatches
- Cryptography version conflicts
- Redis/django-redis compatibility issues

#### 2. Build Environment Issues
- Python version mismatch
- Missing build dependencies
- Network timeouts during pip install

#### 3. Platform-Specific Issues
- Linux-specific packages failing
- Binary packages not available
- Compilation errors

### 🛠️ Step-by-Step Fix

#### Step 1: Try Minimal Requirements
```bash
# In your project root
cp backend/requirements-minimal.txt backend/requirements.txt
git add backend/requirements.txt
git commit -m "Use minimal requirements for deployment"
git push
```

#### Step 2: Use Simple Render Config
```bash
cp render-simple.yaml render.yaml
git add render.yaml
git commit -m "Use simple render configuration"
git push
```

#### Step 3: Check Build Logs
1. Go to your Render dashboard
2. Click on the failing service
3. Check the "Build Logs" tab
4. Look for specific package installation errors

#### Step 4: Test Locally
```bash
# Test the build process locally
docker run --rm -v $(pwd):/app python:3.11 bash -c "
  cd /app/backend
  python -m pip install --upgrade pip
  pip install -r requirements.txt
"
```

### 📋 Alternative Deployment Strategies

#### Strategy A: Manual Dependencies
Remove complex packages and install only what's essential:

```txt
Django==5.2.10
gunicorn==21.2.0
whitenoise==6.6.0
djangorestframework==3.15.2
Pillow==10.2.0
```

#### Strategy B: Use Docker
Create a Dockerfile for more control:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:$PORT"]
```

#### Strategy C: Step-by-Step Deployment
1. Deploy backend first with minimal setup
2. Add database connection
3. Add frontend separately
4. Connect services

### 🆘 Emergency Fix

If nothing works, try this emergency render.yaml:

```yaml
services:
  - type: web
    name: agriculture-backend
    env: python
    plan: free
    buildCommand: "pip install Django==5.2.10 djangorestframework==3.15.2"
    startCommand: "python manage.py runserver 0.0.0.0:$PORT"
    envVars:
      - key: DEBUG
        value: "False"
      - key: SECRET_KEY
        generateValue: true
```

### 📞 Getting Help

1. **Check Render Status**: [status.render.com](https://status.render.com)
2. **Render Docs**: [render.com/docs](https://render.com/docs)
3. **Community**: [Render Community](https://community.render.com)

### ✅ Success Indicators

When deployment succeeds, you should see:
- ✅ Build completes without errors
- ✅ Service status: "Live"
- ✅ Health checks passing
- ✅ Application accessible at URL

---

## 🎯 Try This First

1. Copy `requirements-minimal.txt` over `requirements.txt`
2. Use `render-simple.yaml` configuration
3. Push to GitHub and check build logs

This should resolve the subprocess error in 90% of cases!
