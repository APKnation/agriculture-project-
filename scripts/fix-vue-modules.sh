#!/bin/bash

# Complete Vue Module Resolution Fix
echo "🔧 Complete Vue Module Resolution Fix"

cd "$(dirname "$0")/../frontend"

echo "🧹 Deep clean..."
rm -rf dist
rm -rf node_modules
rm -rf .vite
rm -rf .cache

echo "🗑️ Clear all caches..."
npm cache clean --force
rm -rf ~/.npm/_cacache
rm -rf ~/.cache

echo "📦 Fresh install..."
npm install --verbose

echo "🔍 Verifying Vue installation..."
npm list vue
npm list @vitejs/plugin-vue

echo "🏗️ Building with ES module format..."
npm run build

# Check build
if [ ! -d "dist" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo "📁 Build contents:"
ls -la dist/

echo ""
echo "🔍 Checking built files..."
echo "📄 index.html script tag:"
grep -o 'src="[^"]*"' dist/index.html

echo ""
echo "📄 JavaScript files:"
find dist -name "*.js" -exec basename {} \;

echo ""
echo "📏 Bundle sizes:"
find dist -name "*.js" -exec du -h {} \;

echo ""
echo "🌐 Starting preview server..."
npm run preview &
PREVIEW_PID=$!

echo "⏳ Waiting 3 seconds..."
sleep 3

echo "📱 Preview running at: http://localhost:4173"
echo ""
echo "🧪 Test Instructions:"
echo "1. Open http://localhost:4173"
echo "2. Open browser console (F12)"
echo "3. Look for: 'Failed to resolve module specifier vue'"
echo "4. Should see NO Vue errors"
echo "5. Application should load properly"
echo ""
echo "🛑 To stop: kill $PREVIEW_PID"

# Wait for testing
echo "⏳ Running preview for 2 minutes..."
sleep 120

kill $PREVIEW_PID 2>/dev/null

echo ""
echo "🎯 Vue module fix complete!"
echo "📋 If no Vue errors in console:"
echo "1. Deploy 'dist' to Netlify"
echo "2. Test at: https://kilimo.netlify.app"
echo "3. Should work perfectly"
