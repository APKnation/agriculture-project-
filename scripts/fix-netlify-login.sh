#!/bin/bash

# Fix Netlify Login Page Issue
echo "🔧 Fix Netlify Login Page White Screen"

cd "$(dirname "$0")/../frontend"

echo "🧹 Clean build..."
rm -rf dist
rm -rf node_modules/.vite
rm -rf node_modules/.cache

echo "🗑️ Clear caches..."
npm cache clean --force

echo "📦 Reinstall dependencies..."
npm install

echo "🔍 Check Vue installation..."
if npm list vue | grep -q "vue@"; then
    echo "✅ Vue installed correctly"
else
    echo "❌ Vue installation issue"
    exit 1
fi

echo "🏗️ Build with Vue module fix..."
npm run build

# Check build
if [ ! -d "dist" ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Check built files
echo "🔍 Checking dist/index.html..."
if [ -f "dist/index.html" ]; then
    echo "✅ index.html found"
    echo "📄 Script tag:"
    grep -o 'src="[^"]*"' dist/index.html
else
    echo "❌ index.html missing"
    exit 1
fi

echo ""
echo "🔍 Checking JavaScript file..."
JS_FILE=$(find dist -name "*.js" | head -1)
if [ -f "$JS_FILE" ]; then
    echo "✅ JavaScript file found: $JS_FILE"
    echo "📏 File size: $(du -h "$JS_FILE" | cut -f1)"
else
    echo "❌ JavaScript file missing"
    exit 1
fi

echo ""
echo "🔍 Checking for Vue module issues..."
if grep -q "Failed to resolve module specifier" "$JS_FILE" 2>/dev/null; then
    echo "❌ Vue module resolution issues found"
    echo "🔧 This is causing the white page on Netlify"
    exit 1
else
    echo "✅ No Vue module resolution issues"
fi

echo ""
echo "🌐 Starting preview server..."
npm run preview &
PREVIEW_PID=$!

echo "⏳ Waiting 3 seconds..."
sleep 3

echo "📱 Preview server running at: http://localhost:4173"
echo ""
echo "🧪 Test Instructions:"
echo "1. Open http://localhost:4173"
echo "2. Should redirect to login page (if not authenticated)"
echo "3. Should see login form, not white page"
echo "4. Check browser console for Vue errors"
echo "5. Test login with: apk / password123"
echo ""
echo "🔍 What should happen:"
echo "1. Visit / → redirect to /dashboard"
echo "2. Router guard checks authentication"
echo "3. No token → redirect to /login"
echo "4. Login page loads"
echo ""
echo "🛑 To stop preview: kill $PREVIEW_PID"

# Wait for testing
echo "⏳ Running preview for 2 minutes..."
sleep 120

kill $PREVIEW_PID 2>/dev/null

echo ""
echo "🎯 Fix complete!"
echo "📋 If login page loads locally:"
echo "1. Deploy 'dist' folder to Netlify"
echo "2. Clear Netlify cache"
echo "3. Test at: https://kilimo.netlify.app"
echo "4. Should show login page, not white page"
