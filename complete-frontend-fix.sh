#!/bin/bash

# Complete Frontend Fix Script
echo "🔧 Complete Frontend Fix for Netlify"

# Navigate to project root
cd "$(dirname "$0")"

# Clean everything
echo "🧹 Cleaning all build artifacts and cache..."
cd frontend
rm -rf dist
rm -rf node_modules/.vite
rm -rf node_modules/.cache

# Clear npm cache completely
echo "🗑️ Clearing npm cache..."
npm cache clean --force

# Remove and reinstall dependencies
echo "📦 Removing and reinstalling all dependencies..."
rm -rf node_modules
npm install

# Verify critical dependencies
echo "🔍 Verifying Vue installation..."
if npm list vue | grep -q "vue@"; then
    echo "✅ Vue installed correctly"
else
    echo "❌ Vue installation issue - installing manually"
    npm install vue@latest
fi

echo "🔍 Verifying Vite installation..."
if npm list vite | grep -q "vite@"; then
    echo "✅ Vite installed correctly"
else
    echo "❌ Vite installation issue - installing manually"
    npm install vite@latest
fi

# Build with verbose output
echo "🏗️ Building with verbose output..."
npm run build -- --verbose

# Check build output
if [ -d "dist" ]; then
    echo "✅ Build successful!"
    echo "📁 Build contents:"
    ls -la dist/
    echo ""
    echo "🔍 Checking index.html:"
    if [ -f "dist/index.html" ]; then
        echo "✅ index.html found"
        echo "📄 Script tag:"
        grep -o 'src="[^"]*"' dist/index.html | head -3
    else
        echo "❌ index.html not found"
        exit 1
    fi
    echo ""
    echo "🔍 Checking JS files:"
    find dist -name "*.js" | head -5
    echo ""
    echo "🔍 Checking main JS file:"
    MAIN_JS=$(find dist -name "index-*.js" | head -1)
    if [ -f "$MAIN_JS" ]; then
        echo "✅ Main JS file found: $MAIN_JS"
        echo "📄 File size: $(du -h "$MAIN_JS" | cut -f1)"
    else
        echo "⚠️ No index-*.js file found, checking other JS files:"
        find dist -name "*.js" | while read file; do
            echo "📄 $file ($(du -h "$file" | cut -f1))"
        done
    fi
    
    echo ""
    echo "🔍 Testing local preview..."
    echo "📱 Starting preview server..."
    npm run preview &
    PREVIEW_PID=$!
    
    echo "⏳ Waiting 3 seconds for preview server..."
    sleep 3
    
    echo "🌐 Preview should be available at: http://localhost:4173"
    echo "📋 Test steps:"
    echo "1. Open http://localhost:4173 in browser"
    echo "2. Check console for Vue errors"
    echo "3. Verify application loads"
    echo ""
    echo "🛑 To stop preview server: kill $PREVIEW_PID"
    
else
    echo "❌ Build failed!"
    echo "🔍 Checking build logs..."
    npm run build 2>&1 | tail -20
    exit 1
fi

echo ""
echo "🎯 Frontend fix complete!"
echo ""
echo "📋 Next steps for Netlify:"
echo "1. If local preview works, deploy 'dist' folder to Netlify"
echo "2. Go to https://app.netlify.com/"
echo "3. Drag 'frontend/dist' folder to deploy area"
echo "4. Test at: https://kilimo.netlify.app"
echo ""
echo "🔍 If local preview shows Vue errors:"
echo "1. Check browser console for specific errors"
echo "2. Verify all imports in source files"
echo "3. Check for missing dependencies"
