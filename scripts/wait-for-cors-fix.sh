#!/bin/bash

# CORS Fix Wait Script
echo "⏳ CORS Fix Deployment Status"

echo "🔄 Backend is redeploying with CORS fixes..."
echo "⏱️  This typically takes 2-3 minutes on Render"
echo ""

# Check deployment status
echo "🔍 Checking if CORS headers are updated..."
for i in {1..12}; do
    echo "📅 Attempt $i/12..."
    
    # Test CORS headers
    CORS_HEADERS=$(curl -s -X OPTIONS https://agriculture-project-9-nvhd.onrender.com/api/login/ \
        -H "Origin: http://localhost:4173" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -I | grep -i "access-control-allow-origin" || echo "missing")
    
    if [[ "$CORS_HEADERS" != *"missing"* ]]; then
        echo "✅ CORS headers are now present!"
        echo "📋 Headers found:"
        echo "$CORS_HEADERS"
        echo ""
        echo "🚀 Frontend should work now!"
        echo "📱 Test at: http://localhost:4173"
        echo "🔑 Login with: apk / password123"
        exit 0
    fi
    
    echo "⏳ Waiting 15 seconds..."
    sleep 15
done

echo ""
echo "❌ CORS headers still missing after 3 minutes"
echo "🔧 Possible solutions:"
echo "1. Check Render dashboard for deployment status"
echo "2. Manual redeploy on Render"
echo "3. Check backend logs for errors"
echo ""
echo "📞 In the meantime, you can:"
echo "1. Test the built frontend on Netlify (deploy dist/ folder)"
echo "2. Use the production Netlify URL (no CORS issues there)"
echo "3. Wait a bit longer for backend deployment"
