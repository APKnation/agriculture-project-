#!/bin/bash

# CORS Fix and Test Script
echo "🔧 CORS Fix and Test for Netlify + Render"

BACKEND_URL="https://agriculture-project-9-nvhd.onrender.com"
FRONTEND_URL="https://kilimo.netlify.app"

echo "🌍 Testing CORS from $FRONTEND_URL to $BACKEND_URL"

echo ""
echo "🧪 Test 1: OPTIONS preflight request"
curl -X OPTIONS "$BACKEND_URL/api/login/" \
  -H "Origin: $FRONTEND_URL" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

echo ""
echo "🧪 Test 2: POST request with Origin header"
curl -X POST "$BACKEND_URL/api/login/" \
  -H "Origin: $FRONTEND_URL" \
  -H "Content-Type: application/json" \
  -d '{"username":"apk","password":"password123"}' \
  -v

echo ""
echo "🔍 Checking current backend CORS headers..."
echo "Response should include:"
echo "✅ Access-Control-Allow-Origin: $FRONTEND_URL"
echo "✅ Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS"
echo "✅ Access-Control-Allow-Headers: Content-Type, Authorization"

echo ""
echo "🛠️ If CORS errors persist:"
echo "1. Backend needs to redeploy with new CORS settings"
echo "2. Check render.yaml environment variables"
echo "3. Verify CORS middleware is loaded"
echo "4. Ensure production settings are used"

echo ""
echo "📋 Backend CORS Configuration:"
echo "✅ CORS_ALLOWED_ORIGINS includes Netlify domain"
echo "✅ CORS_ALLOW_ALL_ORIGINS = True (temporary)"
echo "✅ CORS middleware in MIDDLEWARE"
echo "✅ Production settings enabled"

echo ""
echo "⏳ Wait for backend redeploy..."
echo "After pushing render.yaml changes:"
echo "1. Go to Render dashboard"
echo "2. Check deployment status"
echo "3. Wait for 'Deploy succeeded'"
echo "4. Test login again"

echo ""
echo "🎯 Expected Result:"
echo "✅ Login should work without CORS errors"
echo "✅ No 'Access-Control-Allow-Origin missing' errors"
echo "✅ Authentication successful"
