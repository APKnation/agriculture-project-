#!/bin/bash

# Force Render Redeploy Script
echo "🔄 Forcing Render redeploy to apply CORS fixes..."

# Check if we can trigger a redeploy via API (if available)
RENDER_SERVICE_ID="agriculture-backend"
RENDER_WEBHOOK="https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys"

echo "📋 Current situation:"
echo "❌ Backend still showing old CORS behavior"
echo "❌ Health endpoint returns 404 (not deployed yet)"
echo "❌ OPTIONS request missing CORS headers"
echo ""

echo "🔧 Solutions:"
echo "1. Manual redeploy in Render dashboard:"
echo "   - Go to https://dashboard.render.com"
echo "   - Find agriculture-backend service"
echo "   - Click 'Manual Deploy' or 'Restart'"
echo ""
echo "2. Push a small change to trigger redeploy:"
echo "   - This script will create a small change"
echo "   - Commit and push to trigger new build"
echo ""

# Create a small change to trigger redeploy
echo "📝 Creating trigger change..."
TIMESTAMP=$(date +%s)
echo "// Auto-generated redeploy trigger $TIMESTAMP" >> backend/backend/redeploy_trigger.py

# Add the trigger file
git add backend/backend/redeploy_trigger.py
git commit -m "Trigger redeploy for CORS fixes - $TIMESTAMP"
git push

echo ""
echo "✅ Redeploy trigger pushed!"
echo "⏳ Wait 2-3 minutes for deployment"
echo "🔍 Then test:"
echo "   curl https://agriculture-project-9-nvhd.onrender.com/health/"
echo "   curl -X OPTIONS https://agriculture-project-9-nvhd.onrender.com/api/login/ -H 'Origin: https://kilimo.netlify.app'"
echo ""
echo "🎯 Expected after redeploy:"
echo "✅ Health check: 200 OK with JSON response"
echo "✅ CORS headers: Access-Control-Allow-Origin present"
echo "✅ Login works on Netlify"
