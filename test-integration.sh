#!/bin/bash

# Integration Test Script for Agriculture Management System
echo "🧪 Testing Frontend-Backend Integration"
echo "======================================"

BACKEND_URL="https://agriculture-project-9-nvhd.onrender.com"
FRONTEND_URL="https://kilimo.netlify.app"

echo "🔗 Backend URL: $BACKEND_URL"
echo "🌐 Frontend URL: $FRONTEND_URL"
echo ""

# Test 1: Backend Health Check
echo "1. Testing Backend Health..."
echo "GET $BACKEND_URL/api/"
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" "$BACKEND_URL/api/")
HTTP_CODE="${HEALTH_RESPONSE: -3}"
if [ "$HTTP_CODE" = "401" ]; then
    echo "✅ Backend responding correctly (401 - Protected API)"
else
    echo "❌ Backend health check failed (HTTP $HTTP_CODE)"
fi
echo ""

# Test 2: Login Endpoint
echo "2. Testing Login Endpoint..."
echo "POST $BACKEND_URL/api/login/"
LOGIN_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/login/" \
  -H "Content-Type: application/json" \
  -d '{"username": "apk", "password": "password123"}')
if echo "$LOGIN_RESPONSE" | grep -q "token"; then
    echo "✅ Login endpoint working"
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    echo "🔑 Token received: ${TOKEN:0:20}..."
else
    echo "❌ Login endpoint failed"
    echo "Response: $LOGIN_RESPONSE"
fi
echo ""

# Test 3: CORS Headers
echo "3. Testing CORS Headers..."
CORS_RESPONSE=$(curl -s -I -X OPTIONS "$BACKEND_URL/api/login/" \
  -H "Origin: $FRONTEND_URL" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type")
if echo "$CORS_RESPONSE" | grep -q "access-control-allow-origin"; then
    echo "✅ CORS headers present"
else
    echo "⚠️  CORS headers not found (may need backend update)"
fi
echo ""

# Test 4: Frontend Accessibility
echo "4. Testing Frontend Accessibility..."
FRONTEND_RESPONSE=$(curl -s -w "%{http_code}" "$FRONTEND_URL/")
FRONTEND_HTTP_CODE="${FRONTEND_RESPONSE: -3}"
if [ "$FRONTEND_HTTP_CODE" = "200" ]; then
    echo "✅ Frontend accessible"
else
    echo "❌ Frontend not accessible (HTTP $FRONTEND_HTTP_CODE)"
fi
echo ""

# Test 5: API with Authentication
if [ ! -z "$TOKEN" ]; then
    echo "5. Testing Authenticated API Call..."
    API_RESPONSE=$(curl -s -X GET "$BACKEND_URL/api/crops/" \
      -H "Authorization: Bearer $TOKEN")
    if echo "$API_RESPONSE" | grep -q "\["; then
        echo "✅ Authenticated API working"
        CROP_COUNT=$(echo "$API_RESPONSE" | grep -o '\[.*\]' | grep -o '{' | wc -l)
        echo "📊 Found $CROP_COUNT crops in database"
    else
        echo "❌ Authenticated API failed"
        echo "Response: $API_RESPONSE"
    fi
else
    echo "⚠️  Skipping authenticated test (no token)"
fi

echo ""
echo "======================================"
echo "🎯 Integration Test Complete"
echo ""
echo "📋 Manual Testing Steps:"
echo "1. Open $FRONTEND_URL in browser"
echo "2. Try to login with: apk / password123"
echo "3. Check browser console for errors"
echo "4. Verify dashboard loads after login"
echo "5. Test crop management features"
echo ""
echo "🔧 If issues occur:"
echo "- Check browser console (F12)"
echo "- Check network tab for failed requests"
echo "- Clear browser cache and retry"
echo "- Verify backend logs on Render dashboard"
