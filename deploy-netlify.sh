#!/bin/bash

# Netlify Deployment Script for Agriculture Frontend
echo "🚀 Starting Netlify Deployment..."

# Navigate to frontend directory
cd frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build for production
echo "🏗️  Building for production..."
npm run build

# Check if build was successful
if [ -d "dist" ]; then
    echo "✅ Build successful!"
    echo "📁 Build output: $(ls -la dist/ | head -10)"
else
    echo "❌ Build failed!"
    exit 1
fi

# Test the build locally (optional)
echo "🧪 Running local server test..."
npx vite preview --port 3000 &
PREVIEW_PID=$!

echo "🌐 Preview server running at: http://localhost:3000"
echo "📝 Press Ctrl+C to stop preview server and continue deployment"

# Wait for user to test
wait $PREVIEW_PID

echo "🎯 Ready for Netlify deployment!"
echo "📋 Next steps:"
echo "   1. Login to Netlify: https://app.netlify.com/"
echo "   2. Drag 'dist' folder to Netlify deploy area"
echo "   3. Or connect GitHub repository for auto-deploys"
echo ""
echo "🔗 Your site will be available at: https://your-site.netlify.app"
