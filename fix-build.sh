#!/bin/bash

# Frontend Build Fix Script
echo "🔧 Fixing Frontend Build Issues..."

cd frontend

# Clean previous build
echo "🧹 Cleaning previous build..."
rm -rf dist node_modules/.vite

# Reinstall dependencies
echo "📦 Reinstalling dependencies..."
npm install

# Build with verbose output
echo "🏗️ Building with verbose output..."
npm run build

# Check build output
if [ -d "dist" ]; then
    echo "✅ Build successful!"
    echo "📁 Build contents:"
    ls -la dist/
    echo ""
    echo "🔍 Checking main JS file:"
    if [ -f "dist/assets/index-*.js" ]; then
        echo "✅ Main JS file found"
        head -5 dist/assets/index-*.js
    else
        echo "❌ Main JS file not found"
        echo "📁 Available files:"
        find dist -name "*.js" | head -5
    fi
else
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "🎯 Build fix complete!"
echo "📋 Next steps:"
echo "1. Deploy 'dist' folder to Netlify"
echo "2. Test at: https://kilimo.netlify.app"
echo "3. Check browser console for errors"
