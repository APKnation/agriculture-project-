# Agriculture Management System - Deployment Guide

## 🚀 Render Deployment Instructions

### 📋 Prerequisites
- Render account (free tier available)
- GitHub repository with the project code
- All code committed and pushed to GitHub

### 🗂️ Project Structure
```
agriculture/
├── backend/
│   ├── backend/
│   │   ├── settings.py (development)
│   │   └── settings_production.py (production)
│   ├── requirements.txt
│   ├── Procfile
│   └── manage.py
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── render.yaml
└── build-deploy.sh
```

### 🔧 Key Files Created/Updated

#### 1. `backend/requirements.txt`
- Added production dependencies: `gunicorn`, `whitenoise`, `dj-database-url`
- All existing dependencies maintained

#### 2. `backend/backend/settings_production.py`
- Environment-based configuration
- PostgreSQL database support
- Redis caching support
- Security settings for production
- CORS configuration for production domains

#### 3. `backend/Procfile`
- Updated to use production settings
- Gunicorn WSGI server configuration

#### 4. `render.yaml`
- Complete Render service configuration
- Backend Django service
- PostgreSQL database
- Redis cache
- Frontend Vue.js static site

#### 5. `frontend/src/axios.js`
- Environment-aware API URL configuration
- Development proxy support
- Production API URL support

#### 6. `frontend/vite.config.js`
- Production build configuration
- Development proxy maintained

### 🎯 Deployment Steps

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

#### Step 2: Create Render Services
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Select "New" → "Blueprint" 
4. Choose your repository
5. Render will automatically detect the `render.yaml` file

#### Step 3: Environment Variables
Render will automatically set these from `render.yaml`:
- `SECRET_KEY` (auto-generated)
- `DATABASE_URL` (from PostgreSQL service)
- `REDIS_URL` (from Redis service)
- `DEBUG` = "False"
- `ALLOWED_HOSTS` = "your-backend-url.onrender.com"
- `FRONTEND_URL` = "your-frontend-url.onrender.com"

#### Step 4: Manual Environment Variables (if needed)
Add these in Render dashboard:
- `VITE_API_URL` = "https://your-backend-url.onrender.com/api"

### 🔍 Verification Checklist

#### Backend Service
- [ ] Service status: "Ready"
- [ ] Database migrations completed
- [ ] Static files collected
- [ ] API endpoints accessible

#### Frontend Service
- [ ] Build successful
- [ ] Static files served
- [ ] API calls working

#### Database
- [ ] PostgreSQL instance running
- [ ] Connection established
- [ ] Data migrations applied

#### Redis Cache
- [ ] Redis instance running
- [ ] Django cache configured

### 🛠️ Local Testing

Before deploying, test locally:
```bash
# Run the build script
./build-deploy.sh

# Test production settings
cd backend
python manage.py runserver --settings backend.settings_production
```

### 📊 Monitoring

#### Render Dashboard
- Service logs
- Metrics and performance
- Error tracking

#### Django Admin
Access: `https://your-backend-url.onrender.com/admin`
- User management
- Content management
- System monitoring

### 🔧 Troubleshooting

#### Common Issues

1. **Build Failed**
   - Check `requirements.txt` for correct versions
   - Verify all dependencies are installable

2. **Database Connection Error**
   - Ensure `DATABASE_URL` is correctly set
   - Check PostgreSQL service status

3. **Static Files Not Loading**
   - Verify `STATIC_ROOT` is set correctly
   - Check `whitenoise` middleware configuration

4. **CORS Errors**
   - Verify `FRONTEND_URL` is correct
   - Check CORS configuration in production settings

5. **API Calls Failing**
   - Verify `VITE_API_URL` in frontend
   - Check backend service status

#### Debug Commands
```bash
# Check backend logs (in Render dashboard)
# Test API endpoints
curl https://your-backend-url.onrender.com/api/login/

# Check frontend build
cd frontend && npm run build
```

### 🔄 CI/CD Pipeline

The `render.yaml` creates an automatic pipeline:
1. Push to GitHub → Auto-build
2. Build successful → Auto-deploy
3. Health checks → Service monitoring

### 📈 Scaling

#### Free Tier Limits
- Backend: 512MB RAM, shared CPU
- Database: 256MB RAM, 90-day limit
- Redis: 256MB RAM

#### Upgrading
1. Go to service settings in Render
2. Change plan type
3. Adjust resources as needed

### 🔒 Security

#### Production Settings
- `DEBUG = False`
- Secure headers enabled
- HTTPS enforced
- Environment variables for secrets

#### Best Practices
- Regular updates to dependencies
- Monitor security advisories
- Backup database regularly
- Use strong passwords

### 📞 Support

#### Render Documentation
- [Render Docs](https://render.com/docs)
- [Django on Render](https://render.com/docs/deploy-django)
- [Vue.js on Render](https://render.com/docs/deploy-vue)

#### Project-Specific
- Check this README for updates
- Review deployment logs
- Monitor service health

---

## 🎉 You're Ready to Deploy!

Your Agriculture Management System is now configured for production deployment on Render with:
- ✅ Production-ready Django backend
- ✅ Optimized Vue.js frontend
- ✅ PostgreSQL database
- ✅ Redis caching
- ✅ Automatic CI/CD
- ✅ Security best practices
- ✅ Monitoring and logging

Deploy now and watch your farm management system come to life! 🌾
