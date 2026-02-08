#!/bin/bash

# Manual Netlify Deployment Script
echo "🚀 Manual Netlify Deployment"

# Navigate to project root
cd "$(dirname "$0")"

# Build frontend
echo "🏗️ Building frontend..."
cd frontend
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo ""
echo "📁 Build contents:"
ls -la dist/
echo ""
echo "🎯 Ready for manual deployment!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://app.netlify.com/"
echo "2. Drag the 'frontend/dist' folder to the deploy area"
echo "3. Wait for deployment to complete"
echo "4. Test at: https://kilimo.netlify.app"
echo ""
echo "🔍 Fixed Issues:"
echo "✅ Relative asset paths (./assets/ instead of /assets/)"
echo "✅ Proper Vue module resolution"
echo "✅ Correct build configuration"
echo "✅ SPA routing support"
echo ""
echo "📱 Expected Results:"
echo "- No Vue module errors"
echo "- Application loads properly"
echo "- All features functional"
echo "- Login works with deployed backend"
