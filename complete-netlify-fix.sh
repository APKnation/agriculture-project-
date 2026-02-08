#!/bin/bash

# Complete Netlify Fix Script
echo "🔧 Complete Netlify Fix - Vue Module Resolution"

cd "$(dirname "$0")"

# Navigate to frontend
cd frontend

echo "🧹 Cleaning everything..."
rm -rf dist
rm -rf node_modules/.vite
rm -rf node_modules/.cache

echo "🗑️ Clearing npm cache..."
npm cache clean --force

echo "📦 Reinstalling dependencies..."
rm -rf node_modules
npm install

echo "🔍 Verifying Vue installation..."
if npm list vue | grep -q "vue@"; then
    echo "✅ Vue installed correctly"
else
    echo "❌ Vue installation issue"
    exit 1
fi

echo "🏗️ Building with clean configuration..."
npm run build

# Check if build was successful
if [ ! -d "dist" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo "📁 Build contents:"
ls -la dist/

echo ""
echo "🔍 Checking built index.html..."
if [ -f "dist/index.html" ]; then
    echo "✅ index.html found"
    echo "📄 Script tag:"
    grep -o 'src="[^"]*"' dist/index.html
    echo "📄 Icon tag:"
    grep -o 'href="[^"]*"' dist/index.html | head -1
else
    echo "❌ index.html not found"
    exit 1
fi

echo ""
echo "🔍 Checking JavaScript files:"
JS_FILES=$(find dist -name "*.js")
if [ -n "$JS_FILES" ]; then
    echo "✅ JavaScript files found:"
    echo "$JS_FILES"
    echo ""
    echo "📏 Main JS file size:"
    MAIN_JS=$(find dist -name "index*.js" | head -1)
    if [ -f "$MAIN_JS" ]; then
        echo "$(du -h "$MAIN_JS" | cut -f1)"
    fi
else
    echo "❌ No JavaScript files found"
    exit 1
fi

echo ""
echo "🔍 Checking for Vue module references..."
if grep -q "Failed to resolve module specifier" dist/assets/index.js 2>/dev/null; then
    echo "❌ Vue module resolution issues found"
    exit 1
else
    echo "✅ No Vue module resolution issues"
fi

echo ""
echo "🌐 Starting preview server for testing..."
npm run preview &
PREVIEW_PID=$!

echo "⏳ Waiting 3 seconds for server..."
sleep 3

echo "📱 Preview server running at: http://localhost:4173"
echo ""
echo "🧪 Test Instructions:"
echo "1. Open http://localhost:4173 in browser"
echo "2. Check console for Vue errors"
echo "3. Should see no 'Failed to resolve module specifier' errors"
echo "4. Should see no 404 errors for vite.svg"
echo "5. Application should load properly"
echo ""
echo "🛑 To stop preview: kill $PREVIEW_PID"
echo ""
echo "🚀 If local preview works:"
echo "1. Deploy 'dist' folder to Netlify"
echo "2. Test at: https://kilimo.netlify.app"
echo "3. Should work without Vue module errors"

# Wait a bit for user to test
echo "⏳ Preview server will run for 2 minutes..."
sleep 120

# Stop preview server
kill $PREVIEW_PID 2>/dev/null

echo ""
echo "🎯 Fix complete!"
echo "📋 Ready for Netlify deployment"
echo "📁 Deploy 'frontend/dist' folder to Netlify"
