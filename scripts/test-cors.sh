#!/bin/bash

# Test CORS Headers
echo "🧪 Testing CORS Headers"

echo "🔍 Testing OPTIONS preflight request..."
curl -v -X OPTIONS https://agriculture-project-9-nvhd.onrender.com/api/login/ \
  -H "Origin: http://localhost:4173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  2>&1 | grep -E "(Access-Control|HTTP|< |>)"

echo ""
echo "🔍 Testing actual POST request..."
curl -v -X POST https://agriculture-project-9-nvhd.onrender.com/api/login/ \
  -H "Origin: http://localhost:4173" \
  -H "Content-Type: application/json" \
  -d '{"username":"apk","password":"password123"}' \
  2>&1 | grep -E "(Access-Control|HTTP|< |>)"

echo ""
echo "📋 Expected CORS Headers:"
echo "✅ Access-Control-Allow-Origin: http://localhost:4173"
echo "✅ Access-Control-Allow-Methods: POST, OPTIONS"
echo "✅ Access-Control-Allow-Headers: Content-Type, Authorization"

echo ""
echo "⏳ If CORS headers are missing:"
echo "1. Backend needs to redeploy with new settings"
echo "2. Wait 2-3 minutes for Render deployment"
echo "3. Test again"

echo ""
echo "🚀 If CORS headers are present:"
echo "1. Frontend should work now"
echo "2. Test at http://localhost:4173"
echo "3. Login should succeed"
