# Tur'Eco Flutter Mobile Application Documentation

## Overview

The Tur'Eco Flutter mobile application is a cross-platform mobile wrapper that provides native mobile access to the Tur'Eco web application. It uses WebView technology to display the Django web application within a native mobile interface for both Android and iOS devices.

## Table of Contents

1. [Architecture](#architecture)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Configuration](#configuration)
6. [Building & Deployment](#building--deployment)
7. [Development Guide](#development-guide)
8. [Troubleshooting](#troubleshooting)

## Architecture

### Technology Stack

- **Framework**: Flutter 3.8.1+
- **Language**: Dart
- **Primary Package**: `webview_flutter` ^4.0.0
- **Additional Packages**:
  - `flutter_native_splash` ^2.4.0 - Custom splash screen
  - `flutter_launcher_icons` ^0.13.1 - Custom app icons
  - `cupertino_icons` ^1.0.8 - iOS style icons

### Application Architecture

```
┌─────────────────────────────────────┐
│     TurecoApp (MaterialApp)         │
│  - Entry point                      │
│  - App configuration                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   WebAppScreen (StatefulWidget)     │
│  - Main screen container            │
│  - WebView management               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    WebViewController                │
│  - URL loading                      │
│  - Navigation handling              │
│  - JavaScript support               │
└─────────────────────────────────────┘
```

## Features

### 1. **WebView Integration**
- Full JavaScript support enabled
- Seamless web application loading
- Native navigation behavior
- Loading state management

### 2. **Navigation Handling**
- **Hardware Back Button**: Navigates through WebView history
- **Pop Scope Management**: Prevents accidental app closure
- **Browser-like Navigation**: Back button works within web pages first

### 3. **User Experience**
- **Loading Indicator**: Shows progress while pages load
- **Custom Splash Screen**: Branded launch screen
- **Custom App Icon**: Tur'Eco branded launcher icon
- **No Debug Banner**: Clean production-ready interface

### 4. **Cross-Platform Support**
- Android (API 21+)
- iOS
- Windows (desktop)
- macOS (desktop)
- Linux (desktop)
- Web browser

## Project Structure

```
tureco/
├── android/                    # Android-specific configuration
│   ├── app/
│   │   ├── build.gradle.kts   # Android build configuration
│   │   └── src/               # Android native code
│   └── build.gradle.kts       # Project-level gradle config
├── ios/                        # iOS-specific configuration
│   ├── Runner/
│   └── Runner.xcodeproj/
├── lib/                        # Main Dart application code
│   └── main.dart              # Application entry point
├── assets/                     # Static assets
│   └── icons/
│       ├── tureco_icon.png    # App launcher icon
│       └── tureco_splash.png  # Splash screen image
├── web/                        # Web platform files
├── windows/                    # Windows desktop files
├── linux/                      # Linux desktop files
├── macos/                      # macOS desktop files
├── pubspec.yaml               # Dependencies & configuration
├── analysis_options.yaml      # Dart linter configuration
└── README.md                  # Basic project information
```

## Setup & Installation

### Prerequisites

1. **Flutter SDK**: Version 3.8.1 or higher
   ```bash
   flutter --version
   ```

2. **Development Tools**:
   - For Android: Android Studio + Android SDK
   - For iOS: Xcode (macOS only)
   - For all platforms: VS Code or Android Studio

### Installation Steps

1. **Clone the Repository**
   ```bash
   cd tureco/tureco
   ```

2. **Install Dependencies**
   ```bash
   flutter pub get
   ```

3. **Generate App Icons** (if assets are ready)
   ```bash
   flutter pub run flutter_launcher_icons
   ```

4. **Generate Splash Screen**
   ```bash
   flutter pub run flutter_native_splash:create
   ```

5. **Verify Installation**
   ```bash
   flutter doctor
   ```

## Configuration

### 1. Backend URL Configuration

**File**: `lib/main.dart`

```dart
..loadRequest(
  Uri.parse('http://87.106.96.193:80'),  // Production URL
);
```

**Development Options**:
- **Android Emulator**: `http://10.0.2.2:8000` (localhost on host)
- **iOS Simulator**: `http://localhost:8000` or `http://127.0.0.1:8000`
- **Physical Device**: `http://YOUR_PC_IP:8000` (e.g., `http://192.168.1.100:8000`)
- **Production**: `http://87.106.96.193:80`

### 2. App Metadata

**File**: `pubspec.yaml`

```yaml
name: tureco
description: "Tur'Eco - Eco-Tourism Booking Platform"
version: 1.0.0+1  # version+buildNumber
```

### 3. Splash Screen Customization

**File**: `pubspec.yaml`

```yaml
flutter_native_splash:
  color: "#FFFFFF"                          # Background color
  image: assets/icons/tureco_splash.png     # Splash image
  android_12:
    color: "#FFFFFF"
    image: assets/icons/tureco_splash.png
```

### 4. App Icon Configuration

**File**: `pubspec.yaml`

```yaml
flutter_launcher_icons:
  android: true
  ios: true
  image_path: "assets/icons/tureco_icon.png"
  min_sdk_android: 21
```

### 5. Android Permissions

**File**: `android/app/src/main/AndroidManifest.xml`

Required permissions for WebView:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

## Building & Deployment

### Development Build

**Android**:
```bash
flutter run -d android
```

**iOS** (macOS only):
```bash
flutter run -d ios
```

**Chrome** (for testing):
```bash
flutter run -d chrome
```

### Production Build

#### Android APK
```bash
# Debug APK
flutter build apk

# Release APK
flutter build apk --release

# Split APKs by ABI (smaller size)
flutter build apk --split-per-abi --release
```

Output: `build/app/outputs/flutter-apk/app-release.apk`

#### Android App Bundle (for Google Play)
```bash
flutter build appbundle --release
```

Output: `build/app/outputs/bundle/release/app-release.aab`

#### iOS (macOS only)
```bash
flutter build ios --release

# For App Store
flutter build ipa --release
```

Output: `build/ios/ipa/tureco.ipa`

### Version Bumping

Update version in `pubspec.yaml`:
```yaml
version: 1.0.1+2  # Format: MAJOR.MINOR.PATCH+BUILD_NUMBER
```

- **Version Name**: 1.0.1 (user-facing)
- **Build Number**: 2 (internal tracking)

## Development Guide

### Main Application Flow

#### 1. Application Entry Point

```dart
void main() {
  runApp(const TurecoApp());
}
```

#### 2. App Widget

```dart
class TurecoApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,  // Hide debug banner
      title: "Tur'Eco",
      home: WebAppScreen(),
    );
  }
}
```

#### 3. WebView Screen

**Initialization**:
```dart
@override
void initState() {
  super.initState();
  
  _controller = WebViewController()
    ..setJavaScriptMode(JavaScriptMode.unrestricted)
    ..setNavigationDelegate(
      NavigationDelegate(
        onPageStarted: (url) => setState(() => _isLoading = true),
        onPageFinished: (url) => setState(() => _isLoading = false),
      ),
    )
    ..loadRequest(Uri.parse('YOUR_URL'));
}
```

**Navigation Handling**:
```dart
PopScope(
  canPop: false,
  onPopInvokedWithResult: (didPop, result) async {
    if (didPop) return;
    
    // Try WebView back navigation first
    if (await _controller.canGoBack()) {
      _controller.goBack();
      return;
    }
    
    // Check if widget is still mounted
    if (!mounted) return;
    
    // Allow app to close
    Navigator.of(context).maybePop();
  },
  // ... child widgets
)
```

### Key Components

#### Loading State
```dart
bool _isLoading = true;

// In UI
if (_isLoading) const Center(child: CircularProgressIndicator())
```

#### WebView Widget
```dart
WebViewWidget(controller: _controller)
```

### Adding New Features

#### Example: Add Pull-to-Refresh

1. Add dependency to `pubspec.yaml`:
```yaml
dependencies:
  flutter:
    sdk: flutter
  webview_flutter: ^4.0.0
```

2. Wrap WebView with refresh indicator:
```dart
RefreshIndicator(
  onRefresh: () async {
    await _controller.reload();
  },
  child: WebViewWidget(controller: _controller),
)
```

#### Example: Add Custom JavaScript Bridge

```dart
_controller
  ..setJavaScriptMode(JavaScriptMode.unrestricted)
  ..addJavaScriptChannel(
    'FlutterChannel',
    onMessageReceived: (JavaScriptMessage message) {
      print('Message from JS: ${message.message}');
    },
  );
```

In web app:
```javascript
FlutterChannel.postMessage('Hello from web!');
```

### Testing

#### Unit Tests
```bash
flutter test
```

#### Widget Tests
Create tests in `test/widget_test.dart`

#### Integration Tests
```bash
flutter drive --target=test_driver/app.dart
```

## Troubleshooting

### Common Issues

#### 1. WebView Not Loading

**Symptom**: Blank screen or ERR_CONNECTION_REFUSED

**Solutions**:
- Check network connectivity
- Verify backend URL is accessible
- For emulator: Use `10.0.2.2` instead of `localhost`
- For physical device: Ensure device and PC are on same network
- Check Android permissions in `AndroidManifest.xml`

#### 2. Back Button Not Working

**Symptom**: App closes instead of navigating back

**Solution**: Verify `PopScope` implementation in `main.dart`

#### 3. Build Failures

**Android Gradle Issues**:
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter build apk
```

**iOS Build Issues**:
```bash
cd ios
pod deintegrate
pod install
cd ..
flutter clean
flutter build ios
```

#### 4. Performance Issues

**Solutions**:
- Enable hardware acceleration (Android)
- Optimize web app assets
- Implement caching in WebView
- Use release builds for testing performance

#### 5. Splash Screen Not Showing

**Solution**:
```bash
flutter pub run flutter_native_splash:create
```

Verify assets exist in `assets/icons/`

#### 6. JavaScript Not Working

**Solution**: Ensure JavaScript mode is set:
```dart
..setJavaScriptMode(JavaScriptMode.unrestricted)
```

### Debug Commands

**Check Flutter Doctor**:
```bash
flutter doctor -v
```

**View Logs**:
```bash
# Android
flutter logs

# Or use adb
adb logcat | grep flutter
```

**Clear Cache**:
```bash
flutter clean
flutter pub cache repair
```

### Network Debugging

**Check if URL is accessible**:
```bash
# Windows PowerShell
Test-NetConnection -ComputerName 87.106.96.193 -Port 80

# Or use browser
curl http://87.106.96.193:80
```

## Environment-Specific Configuration

### Development
```dart
const String API_URL = 'http://10.0.2.2:8000';  // Android Emulator
```

### Staging
```dart
const String API_URL = 'http://staging.tureco.com';
```

### Production
```dart
const String API_URL = 'http://87.106.96.193:80';
```

**Best Practice**: Use environment variables or build flavors:

```dart
const String API_URL = String.fromEnvironment(
  'API_URL',
  defaultValue: 'http://87.106.96.193:80',
);
```

Build with:
```bash
flutter build apk --dart-define=API_URL=http://production.url
```

## Performance Optimization

### 1. WebView Optimization
```dart
_controller
  ..setBackgroundColor(Colors.white)
  ..enableZoom(false);
```

### 2. Image Optimization
- Use optimized splash screen images
- Keep app icon under 1MB
- Use PNG format for transparency

### 3. Build Optimization
```bash
# Enable R8 shrinking (Android)
flutter build apk --release --obfuscate --split-debug-info=build/app/outputs/symbols

# Enable optimization flags
flutter build apk --release --shrink --tree-shake-icons
```

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **SSL Pinning**: Consider implementing for enhanced security
3. **JavaScript Channels**: Validate all messages from WebView
4. **Permissions**: Request only necessary permissions
5. **Code Obfuscation**: Use `--obfuscate` flag for release builds

## Maintenance

### Regular Updates

1. **Flutter SDK**: Keep updated
   ```bash
   flutter upgrade
   ```

2. **Dependencies**: Update regularly
   ```bash
   flutter pub upgrade
   ```

3. **Security Patches**: Monitor dependency advisories
   ```bash
   flutter pub outdated
   ```

### Version Control

- Tag releases: `git tag v1.0.0`
- Keep changelog updated
- Document breaking changes

## Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [WebView Flutter Plugin](https://pub.dev/packages/webview_flutter)
- [Flutter Cookbook](https://docs.flutter.dev/cookbook)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)

## Support

For issues or questions:
- Create an issue in the project repository
- Contact the development team
- Check existing documentation and issues

---

**Last Updated**: January 2026
**Version**: 1.0.0
**Author**: Tur'Eco Development Team
