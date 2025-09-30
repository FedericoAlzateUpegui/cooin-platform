#!/bin/bash

# Cooin iOS App - iPhone Installation Script
# Run this script on a Mac with Xcode installed

echo "🚀 Building Cooin iOS App for iPhone..."
echo "======================================"

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    echo "❌ Error: Xcode is not installed or xcodebuild is not in PATH"
    echo "Please install Xcode from the App Store"
    exit 1
fi

# Navigate to project directory
cd "$(dirname "$0")"

# Check if project exists
if [ ! -f "Cooin.xcodeproj/project.pbxproj" ]; then
    echo "❌ Error: Cooin.xcodeproj not found"
    echo "Make sure you're running this script from the correct directory"
    exit 1
fi

echo "✅ Found Xcode project"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
xcodebuild clean -project Cooin.xcodeproj -scheme Cooin

# Build for device (you'll need to set your development team)
echo "🔨 Building for iPhone..."
echo "⚠️  IMPORTANT: You need to:"
echo "   1. Open Cooin.xcodeproj in Xcode"
echo "   2. Set your Apple Developer Team in project settings"
echo "   3. Change bundle identifier to something unique"
echo "   4. Connect your iPhone and select it as target"
echo "   5. Press Cmd+R to build and install"

echo ""
echo "📋 Quick Setup Checklist:"
echo "========================"
echo "□ Mac with Xcode 13+ installed"
echo "□ iPhone with iOS 14+ (connected via USB)"
echo "□ Apple ID signed into Xcode"
echo "□ Backend running at http://192.168.40.34:8000"
echo "□ iPhone and computer on same network"

echo ""
echo "🎯 Next Steps:"
echo "1. Open Xcode: open Cooin.xcodeproj"
echo "2. Select your iPhone as target device"
echo "3. Press Cmd+R to build and install"
echo "4. Trust developer certificate on iPhone (Settings → General → VPN & Device Management)"

echo ""
echo "📱 Testing the App:"
echo "- Register a new account or login"
echo "- Explore dashboard and analytics"
echo "- Test loan matching features"
echo "- Try document upload with camera"

echo ""
echo "🔧 Troubleshooting:"
echo "- If build fails: Check bundle identifier is unique"
echo "- If can't connect to backend: Verify IP address and network"
echo "- If camera doesn't work: Check permissions in Settings"

echo ""
echo "✨ Ready to install! Open the project in Xcode and build."