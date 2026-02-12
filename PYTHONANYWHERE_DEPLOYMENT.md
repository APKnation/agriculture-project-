# PythonAnywhere Deployment Guide

## 🐍 PYTHONANYWHERE SETUP

### 1. Account Setup
- Username: **apknation**
- Plan: Free tier (or paid for better performance)
- Web app: Manual configuration

### 2. Initial Setup Commands

```bash
# In PythonAnywhere Bash console
cd ~
git clone https://github.com/APKnation/agriculture-project-.git
cd agriculture-project-
```

### 3. Web App Configuration

#### Web Tab Settings:
- **Python version**: 3.11
- **Working directory**: `/home/apknation/agriculture-project-/backend`
- **WSGI file**: `/home/apknation/agriculture-project-/pythonanywhere_wsgi.py`
- **Virtualenv**: Create new virtualenv

#### Virtualenv Setup:
```bash
cd ~/agriculture-project-
mkvirtualenv --python=python3.11 venv
workon venv
cd backend
pip install -r requirements.txt
```

### 4. Environment Variables

In Web tab → Variables:
```
DJANGO_SETTINGS_MODULE=backend.settings_production
SECRET_KEY=your-very-secret-key-here
DEBUG=False
```

### 5. Database Setup

```bash
cd ~/agriculture-project-/backend
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6. Static Files Configuration

#### In Web tab → Static files:
- **URL**: `/static/`
- **Directory**: `/home/apknation/agriculture-project-/backend/staticfiles`

#### In Web tab → Media files:
- **URL**: `/media/`
- **Directory**: `/home/apknation/agriculture-project-/backend/media`

### 7. URL Configuration

Your app will be available at:
- **Main**: `https://apknation.pythonanywhere.com`
- **Admin**: `https://apknation.pythonanywhere.com/admin`
- **API**: `https://apknation.pythonanywhere.com/api`

## 🔄 AUTO-DEPLOYMENT SETUP

### GitHub Webhook

1. **GitHub Repo** → Settings → Webhooks
2. **Payload URL**: `https://apknation.pythonanywhere.com/api/v1/user/apknation/webhooks/github/`
3. **Content type**: `application/json`
4. **Secret**: Create random string
5. **Events**: "Just" → "pushes"

### Webhook Handler (Optional)

Create webhook handler in Django to receive GitHub events:
```python
# Add to backend/backend/urls.py
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import subprocess
import json

@csrf_exempt
@require_http_methods(["POST"])
def github_webhook(request):
    try:
        # Verify webhook secret if needed
        # Pull latest changes
        subprocess.run(['git', 'pull', 'origin', 'main'], 
                     cwd='/home/apknation/agriculture-project-')
        # Restart web app
        subprocess.run(['touch', '/var/www/apknation_pythonanywhere_com_wsgi.py'])
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, 500)
```

## 🌐 NETLIFY FRONTEND

### Build Settings
```
Base directory: frontend
Build command: npm run build
Publish directory: frontend/dist
```

### Environment Variables
```
VITE_API_URL=https://apknation.pythonanywhere.com/api/
```

### Auto-deploy
- Connect to GitHub repository
- Enable continuous deployment
- Deploy on push to main branch

## 📋 FINAL CHECKLIST

### ✅ PythonAnywhere
- [ ] Web app created with Python 3.11
- [ ] WSGI file configured
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Static files collected
- [ ] Environment variables set
- [ ] Superuser created

### ✅ Netlify
- [ ] Repository connected
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Auto-deploy enabled

### ✅ Integration
- [ ] Frontend connects to backend
- [ ] CORS configured
- [ ] Authentication works
- [ ] API endpoints accessible

## 🚀 DEPLOYMENT COMMANDS

### Manual Deploy:
```bash
cd ~/agriculture-project-
chmod +x deploy_pythonanywhere.sh
./deploy_pythonanywhere.sh
```

### Quick Update:
```bash
cd ~/agriculture-project-
git pull origin main
cd backend && python manage.py collectstatic --noinput
touch /var/www/apknation_pythonanywhere_com_wsgi.py
```

## 🌐 FINAL URLS

- **Backend**: `https://apknation.pythonanywhere.com`
- **Frontend**: `https://your-app-name.netlify.app`
- **Admin**: `https://apknation.pythonanywhere.com/admin`
- **API**: `https://apknation.pythonanywhere.com/api`
