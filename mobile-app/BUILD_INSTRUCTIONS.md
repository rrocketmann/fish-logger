# Fish Logger - Android App Build Instructions

## Prerequisites

1. **Install Node.js and npm:**
   ```bash
   sudo pacman -S nodejs npm
   ```

2. **Verify installation:**
   ```bash
   node --version  # Should be v18+
   npm --version   # Should be v9+
   ```

## Setup & Build

### 1. Navigate to mobile app directory:
```bash
cd /home/martin/dev/fish-logger/mobile-app/fish-logger-app
```

### 2. Install dependencies:
```bash
npm install
```

### 3. Test on your Pixel 9a (Development Mode):

**Option A: Expo Go (Fastest)**
```bash
# Install Expo Go from Google Play Store on your Pixel 9a
npx expo start

# Scan the QR code with Expo Go app
# App runs instantly - no build needed!
```

**Option B: Development Build**
```bash
# Install on phone via USB debugging
npx expo run:android
```

### 4. Build Production APK:

**Install EAS CLI:**
```bash
npm install -g eas-cli
```

**Login to Expo:**
```bash
eas login
```

**Build APK:**
```bash
# First time setup
eas build:configure

# Build the APK
eas build --platform android --profile preview
```

This will:
- Build the app in the cloud
- Generate an `.apk` file
- Download link provided when complete

**Install APK on Pixel 9a:**
1. Download the `.apk` file
2. Transfer to your phone
3. Enable "Install from unknown sources" in Android settings
4. Tap the APK file to install

## Alternative: Local Build (No Cloud)

If you want to build locally without EAS:

1. **Install Android Studio:**
   ```bash
   yay -S android-studio
   ```

2. **Set up Android SDK:**
   - Open Android Studio
   - Go to Settings → Android SDK
   - Install Android 13 (API 33) or higher
   - Add to PATH in `~/.bashrc`:
     ```bash
     export ANDROID_HOME=$HOME/Android/Sdk
     export PATH=$PATH:$ANDROID_HOME/emulator
     export PATH=$PATH:$ANDROID_HOME/platform-tools
     export PATH=$PATH:$ANDROID_HOME/tools
     export PATH=$PATH:$ANDROID_HOME/tools/bin
     ```

3. **Build APK:**
   ```bash
   npx expo prebuild
   cd android
   ./gradlew assembleRelease
   ```

4. **APK location:**
   ```
   android/app/build/outputs/apk/release/app-release.apk
   ```

## Features Included

✅ **Camera Integration** - Take photos of fish catches  
✅ **Offline Database** - SQLite storage, works without internet  
✅ **AI Identification** - Connect to server for species ID  
✅ **Submit Catches** - Form with species, location, notes  
✅ **View Database** - Browse all logged catches  
✅ **Background Sync** - Auto-uploads when network available  
✅ **Offline-First Design** - All core features work offline  

## App Configuration

Server URL is set to: `http://100.118.217.22:5000`

To change it, edit:
```
src/context/DatabaseContext.js
src/screens/IdentifyScreen.js
```

Update the `SERVER_URL` constant.

## Troubleshooting

**Metro bundler won't start:**
```bash
npx expo start -c  # Clear cache
```

**Build fails:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Camera not working:**
- Check app permissions in Android settings
- Ensure camera permission is granted

**Sync not working:**
- Check if Flask server is running on `http://100.118.217.22:5000`
- Verify phone and server are on same network
- Check firewall settings

## Quick Start Summary

```bash
# Install Node.js (if not done)
sudo pacman -S nodejs npm

# Navigate to app
cd /home/martin/dev/fish-logger/mobile-app/fish-logger-app

# Install dependencies
npm install

# Run on phone with Expo Go
npx expo start
```

That's it! Scan QR code with Expo Go app and start using Fish Logger on your Pixel 9a!
