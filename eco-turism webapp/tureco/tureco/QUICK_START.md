# Tur'Eco Flutter App - Quick Start Guide

## Prerequisites Checklist

- [ ] Flutter SDK 3.8.1+ installed
- [ ] Android Studio (for Android development)
- [ ] Xcode (for iOS development - macOS only)
- [ ] Git installed
- [ ] Text editor (VS Code recommended)

## Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
cd tureco/tureco
flutter pub get
```

### 2. Check Your Setup
```bash
flutter doctor
```
Fix any issues shown with ❌

### 3. Run the App

**On Android Emulator:**
```bash
flutter run -d android
```

**On iOS Simulator (macOS only):**
```bash
flutter run -d ios
```

**On Physical Device:**
1. Enable USB debugging on your device
2. Connect via USB
3. Run: `flutter devices` to verify connection
4. Run: `flutter run`

## Common Commands

### Development
```bash
# Run app in debug mode
flutter run

# Run with hot reload enabled (default)
flutter run

# Run on specific device
flutter run -d <device-id>

# View available devices
flutter devices
```

### Building
```bash
# Build Android APK
flutter build apk --release

# Build for Google Play Store
flutter build appbundle --release

# Build iOS (macOS only)
flutter build ios --release
```

### Maintenance
```bash
# Clean build files
flutter clean

# Get dependencies
flutter pub get

# Update dependencies
flutter pub upgrade

# Check for issues
flutter doctor
```

## Configuration Quick Reference

### Change Backend URL
**File**: `lib/main.dart` (around line 45)

```dart
..loadRequest(
  Uri.parse('YOUR_URL_HERE'),
);
```

**Common URLs:**
- Production: `http://87.106.96.193:80`
- Local (Android Emulator): `http://10.0.2.2:8000`
- Local (iOS Simulator): `http://localhost:8000`
- Local (Physical Device): `http://YOUR_PC_IP:8000`

### Update App Version
**File**: `pubspec.yaml`

```yaml
version: 1.0.0+1  # Format: VERSION_NAME+BUILD_NUMBER
```

## Troubleshooting Quick Fixes

### App Won't Build
```bash
flutter clean
flutter pub get
flutter run
```

### WebView Shows Blank Screen
1. Check internet connection
2. Verify backend URL is accessible
3. Check Android permissions in `android/app/src/main/AndroidManifest.xml`

### "No devices found"
```bash
# For Android
adb devices

# Restart adb
adb kill-server
adb start-server
```

### Gradle Build Failed (Android)
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter run
```

## Project Structure Overview

```
lib/
  └── main.dart          # App entry point & main code

android/                 # Android-specific files
ios/                     # iOS-specific files
pubspec.yaml            # Dependencies & config
assets/icons/           # App icons & splash screen
```

## Key Files to Know

| File | Purpose |
|------|---------|
| `lib/main.dart` | Main app code & WebView setup |
| `pubspec.yaml` | Dependencies & app metadata |
| `android/app/build.gradle` | Android build config |
| `android/app/src/main/AndroidManifest.xml` | Android permissions |
| `ios/Runner/Info.plist` | iOS configuration |

## Development Workflow

1. Make changes to code
2. Save file (hot reload happens automatically)
3. Test changes in running app
4. If hot reload doesn't work: Press `R` in terminal or restart app

## Build for Release Checklist

- [ ] Update version number in `pubspec.yaml`
- [ ] Test on multiple devices
- [ ] Verify backend URL points to production
- [ ] Remove debug logs
- [ ] Run `flutter clean`
- [ ] Build release: `flutter build apk --release`
- [ ] Test the release APK on device

## Getting Help

- Check logs: `flutter logs`
- Verbose doctor: `flutter doctor -v`
- Full documentation: See `FLUTTER_APP_DOCUMENTATION.md`

---

**Quick Tip**: Use `flutter run` with hot reload for development - changes appear instantly without rebuilding!
