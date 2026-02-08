#!/bin/bash

# Test Built Frontend
echo "🧪 Testing Built Frontend"

cd "$(dirname "$0")/frontend"

# Check if dist exists
if [ ! -d "dist" ]; then
    echo "❌ dist folder not found. Run 'npm run build' first."
    exit 1
fi

echo "✅ dist folder found"
echo "📁 Contents:"
ls -la dist/

echo ""
echo "🔍 Checking index.html:"
if [ -f "dist/index.html" ]; then
    echo "✅ index.html exists"
    echo "📄 Script tag:"
    grep -o 'src="[^"]*"' dist/index.html
else
    echo "❌ index.html missing"
    exit 1
fi

echo ""
echo "🔍 Checking JavaScript file:"
JS_FILE=$(find dist -name "*.js" | head -1)
if [ -f "$JS_FILE" ]; then
    echo "✅ JavaScript file found: $JS_FILE"
    echo "📏 File size: $(du -h "$JS_FILE" | cut -f1)"
    echo "🔍 First 100 characters:"
    head -c 100 "$JS_FILE"
    echo ""
else
    echo "❌ JavaScript file missing"
    exit 1
fi

echo ""
echo "🌐 Starting preview server..."
npm run preview &
PREVIEW_PID=$!

echo "⏳ Waiting 3 seconds for server to start..."
sleep 3

echo "📱 Preview server running at: http://localhost:4173"
echo ""
echo "🧪 Test Instructions:"
echo "1. Open http://localhost:4173 in your browser"
echo "2. Try to login with: apk / password123"
echo "3. Check browser console for errors"
echo "4. If login works, the build is good for Netlify"
echo ""
echo "🛑 To stop preview server: kill $PREVIEW_PID"
echo ""
echo "🔍 If you still get timeout errors:"
echo "1. Check browser network tab for failed requests"
echo "2. Verify backend is accessible: curl -X POST https://agriculture-project-9-nvhd.onrender.com/api/login/ -H 'Content-Type: application/json' -d '{\"username\":\"apk\",\"password\":\"password123\"}'"
echo "3. Check CORS headers in browser"
