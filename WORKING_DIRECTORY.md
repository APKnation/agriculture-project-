# PythonAnywhere Working Directory Configuration

## 📁 CORRECT WORKING DIRECTORIES

### Username: apknation
### Project: agriculture-project-

## 🐍 PYTHONANYWHERE STRUCTURE

```
/home/apknation/
├── agriculture-project-/          # Main project directory
│   ├── backend/                # Django backend
│   │   ├── backend/           # Django settings
│   │   ├── market/            # Django app
│   │   ├── manage.py
│   │   └── requirements.txt
│   ├── frontend/              # Vue frontend
│   │   ├── src/
│   │   ├── package.json
│   │   └── dist/
│   ├── .git/
│   └── deploy_pythonanywhere.sh
├── .virtualenvs/              # Python virtual environments
└── .ssh/                    # SSH keys
```

## 🔧 WEB APP CONFIGURATION

### Working Directory:
```
/home/apknation/agriculture-project-/backend
```

### WSGI File Path:
```
/home/apknation/agriculture-project-/pythonanywhere_wsgi.py
```

### Static Files Directory:
```
/home/apknation/agriculture-project-/backend/staticfiles
```

### Media Files Directory:
```
/home/apknation/agriculture-project-/backend/media
```

## 📋 PYTHONANYWHERE SETUP COMMANDS

### 1. Clone Repository
```bash
cd ~
git clone https://github.com/APKnation/agriculture-project-.git
cd agriculture-project-
```

### 2. Create Virtual Environment
```bash
cd ~/agriculture-project-
mkvirtualenv --python=python3.11 apknation-env
workon apknation-env
```

### 3. Install Dependencies
```bash
cd ~/agriculture-project-/backend
pip install -r requirements_pythonanywhere.txt
```

### 4. Set Up Web App
```bash
# In PythonAnywhere Web tab:
# Working directory: /home/apknation/agriculture-project-/backend
# WSGI file: /home/apknation/agriculture-project-/pythonanywhere_wsgi.py
# Virtualenv: apknation-env
```

## 🔄 DEPLOYMENT WORKFLOW

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
cd backend
python manage.py collectstatic --noinput
touch /var/www/apknation_pythonanywhere_com_wsgi.py
```

## 🌐 FINAL URLS

### Backend URLs:
- **Main**: `https://apknation.pythonanywhere.com`
- **Admin**: `https://apknation.pythonanywhere.com/admin`
- **API**: `https://apknation.pythonanywhere.com/api`
- **Health**: `https://apknation.pythonanywhere.com/health`

### Static Files URL:
- **Static**: `https://apknation.pythonanywhere.com/static/`
- **Media**: `https://apknation.pythonanywhere.com/media/`

## 🔍 TROUBLESHOOTING

### If WSGI fails:
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Test Django import
cd ~/agriculture-project-/backend
python -c "import django; print(django.get_version())"
```

### If static files not loading:
```bash
# Recollect static files
cd ~/agriculture-project-/backend
python manage.py collectstatic --noinput --clear
```

### If database issues:
```bash
# Check database settings
cd ~/agriculture-project-/backend
python manage.py check --deploy
```

## 📝 IMPORTANT NOTES

1. **Working Directory**: Always use `/home/apknation/agriculture-project-/backend`
2. **Python Path**: Both project root and backend must be in PYTHONPATH
3. **Virtual Environment**: Use `apknation-env` for isolation
4. **Static Files**: Must be collected and configured in Web tab
5. **WSGI File**: Use the provided `pythonanywhere_wsgi.py`
6. **Restart**: Use `touch /var/www/apknation_pythonanywhere_com_wsgi.py`
