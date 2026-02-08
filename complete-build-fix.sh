#!/bin/bash

# Complete Netlify Build Fix Script
echo "🔧 Complete Netlify Build Fix..."

# Navigate to project root
cd "$(dirname "$0")"

# Clean everything
echo "🧹 Cleaning all build artifacts..."
rm -rf frontend/dist
rm -rf frontend/node_modules/.vite
rm -rf frontend/node_modules/.cache

# Navigate to frontend
cd frontend

# Clear npm cache
echo "🗑️ Clearing npm cache..."
npm cache clean --force

# Remove node_modules and reinstall
echo "📦 Removing and reinstalling dependencies..."
rm -rf node_modules
npm install

# Verify Vue installation
echo "🔍 Verifying Vue installation..."
if npm list vue | grep -q "vue@"; then
    echo "✅ Vue is installed correctly"
else
    echo "❌ Vue installation issue found"
    exit 1
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
        head -10 dist/index.html
    else
        echo "❌ index.html not found"
        exit 1
    fi
    echo ""
    echo "🔍 Checking JS files:"
    find dist -name "*.js" | head -5
    echo ""
    echo "🔍 Checking main JS file content:"
    MAIN_JS=$(find dist -name "index-*.js" | head -1)
    if [ -f "$MAIN_JS" ]; then
        echo "✅ Main JS file found: $MAIN_JS"
        echo "📄 First 5 lines:"
        head -5 "$MAIN_JS"
    else
        echo "⚠️ No index-*.js file found, checking other JS files:"
        find dist -name "*.js" | while read file; do
            echo "📄 $file (first 3 lines):"
            head -3 "$file"
            echo ""
        done
    fi
else
    echo "❌ Build failed!"
    echo "🔍 Checking build logs..."
    npm run build 2>&1 | tail -20
    exit 1
fi

echo ""
echo "🎯 Build fix complete!"
echo ""
echo "📋 Next steps for Netlify:"
echo "1. Commit and push these changes"
echo "2. Wait for Netlify auto-rebuild"
echo "3. Test at: https://kilimo.netlify.app"
echo "4. Check browser console for errors"
echo ""
echo "🔧 If still failing:"
echo "1. Manual deploy: Drag 'frontend/dist' to Netlify"
echo "2. Check Netlify build logs"
echo "3. Verify netlify.toml is in project root"
