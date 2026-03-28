# Fish Logger - Mobile App Setup Guide

## Option 1: Quick Setup with Expo Go (Recommended)

### Prerequisites
Install Node.js on your development machine:
```bash
sudo pacman -S nodejs npm
```

### Create the App
```bash
cd /home/martin/dev/fish-logger
npx create-expo-app@latest fish-logger-mobile --template blank
cd fish-logger-mobile
npm install expo-camera expo-file-system expo-sqlite @react-native-async-storage/async-storage axios
```

### Run on Your Pixel 9a
1. Install **Expo Go** from Google Play Store on your Pixel 9a
2. Make sure phone and computer are on same WiFi
3. Start development server:
   ```bash
   npx expo start
   ```
4. Scan the QR code with Expo Go app
5. App runs instantly on your phone!

---

## Option 2: Build APK (Full Offline App)

### Build APK with EAS:
```bash
npm install -g eas-cli
eas build --platform android --profile preview
```

This creates an `.apk` file you can install directly on your Pixel 9a.

---

## Mobile App Features

### Offline-First Architecture
- **Local Storage**: SQLite database on phone
- **Camera Access**: Take photos directly in app
- **AI Identification**: (Requires model conversion to TensorFlow Lite)
- **Background Sync**: Uploads when network available

### Server Connection
The app syncs with your Flask server at: `http://100.118.217.22:5000`

API Endpoints (already implemented):
- `POST /api/submit` - Submit catch data
- `GET /api/database` - Download full database
- `GET /export/json` - Export database

---

## Starter Code

I can create the full React Native app structure for you with:
- Camera screen for taking fish photos
- Offline database with SQLite
- Identify screen (AI integration)
- Submit screen with forms
- Database view screen
- Automatic background sync

Just run the Node.js installation and I'll generate all the code!

---

## Alternative: PWA (Progressive Web App)

If you want something simpler:
1. Open `http://100.118.217.22:5000` in Chrome on your Pixel
2. Tap menu → "Add to Home Screen"
3. Works offline with service workers (I can add this feature)
4. No app store needed
5. Can access camera through browser

Would you like me to add PWA support to the existing Flask app instead?
