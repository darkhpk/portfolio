# Tur'Eco Mobile Application

[![Flutter](https://img.shields.io/badge/Flutter-3.8.1+-02569B?logo=flutter)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.0+-0175C2?logo=dart)](https://dart.dev)
[![License](https://img.shields.io/badge/License-Proprietary-red)]()

A cross-platform mobile application for the Tur'Eco eco-tourism booking platform, providing native mobile access to the Django web application.

## 🚀 Features

- **WebView Integration**: Seamless integration with Tur'Eco web platform
- **Native Navigation**: Hardware back button support with WebView history
- **Cross-Platform**: Single codebase for Android, iOS, and desktop platforms
- **Offline Handling**: Graceful handling of network connectivity
- **Custom Branding**: Branded splash screen and app icon
- **Performance Optimized**: Fast loading with minimal overhead

## 📱 Platform Support

| Platform | Minimum Version | Status |
|----------|----------------|--------|
| Android  | API 21 (5.0)  | ✅ Supported |
| iOS      | iOS 11.0      | ✅ Supported |
| Web      | Modern browsers | ✅ Supported |
| Windows  | Windows 10+   | ✅ Supported |
| macOS    | macOS 10.14+  | ✅ Supported |
| Linux    | Ubuntu 18.04+ | ✅ Supported |

## 🛠️ Tech Stack

- **Flutter SDK**: 3.8.1+
- **Dart**: 3.0+
- **WebView Flutter**: 4.0.0
- **Flutter Native Splash**: 2.4.0
- **Flutter Launcher Icons**: 0.13.1

## 📋 Prerequisites

- Flutter SDK 3.8.1 or higher
- Dart SDK 3.0 or higher
- Android Studio (for Android development)
- Xcode (for iOS development, macOS only)
- VS Code or Android Studio with Flutter/Dart plugins

## 🏁 Quick Start

### 1. Install Dependencies

```bash
flutter pub get
```

### 2. Run the App

```bash
# On Android emulator/device
flutter run -d android

# On iOS simulator/device (macOS only)
flutter run -d ios

# On web browser
flutter run -d chrome
```

### 3. Build for Release

```bash
# Android APK
flutter build apk --release

# Android App Bundle (for Play Store)
flutter build appbundle --release

# iOS (macOS only)
flutter build ios --release
```

## 📖 Documentation

### Complete Guides

- **[Flutter App Documentation](FLUTTER_APP_DOCUMENTATION.md)** - Comprehensive technical documentation
- **[Quick Start Guide](QUICK_START.md)** - Get started in 5 minutes
- **[API Reference](API_REFERENCE.md)** - Complete API documentation
- **[Deployment Guide](DEPLOYMENT.md)** - Deploy to Play Store and App Store

### Key Topics

#### Configuration

The app connects to the backend web server. Update the URL in `lib/main.dart`:

```dart
..loadRequest(
  Uri.parse('http://87.106.96.193:80'),  // Production URL
);
```

For development:
- **Android Emulator**: `http://10.0.2.2:8000`
- **iOS Simulator**: `http://localhost:8000`
- **Physical Device**: `http://YOUR_PC_IP:8000`

#### Version Management

Update version in `pubspec.yaml`:

```yaml
version: 1.0.0+1  # Format: VERSION_NAME+BUILD_NUMBER
```

## 🏗️ Project Structure

```
tureco/
├── lib/
│   └── main.dart              # App entry point & main code
├── android/                   # Android platform files
├── ios/                       # iOS platform files
├── assets/
│   └── icons/                 # App icons & splash screen
├── pubspec.yaml              # Dependencies & configuration
├── FLUTTER_APP_DOCUMENTATION.md
├── QUICK_START.md
├── API_REFERENCE.md
├── DEPLOYMENT.md
└── README.md
```

## 🔧 Development

### Hot Reload

Flutter supports hot reload for instant updates:
1. Make changes to your code
2. Press `r` in terminal or save file
3. See changes instantly in running app

### Testing

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widget_test.dart

# Check for issues
flutter analyze
```

### Common Commands

```bash
# Check Flutter installation
flutter doctor

# Clean build files
flutter clean

# Update dependencies
flutter pub upgrade

# View connected devices
flutter devices

# View logs
flutter logs
```

## 🚢 Deployment

### Android

1. Configure signing in `android/app/build.gradle.kts`
2. Create `android/key.properties` with keystore details
3. Build: `flutter build appbundle --release`
4. Upload to Google Play Console

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### iOS

1. Configure signing in Xcode
2. Update bundle identifier
3. Build: `flutter build ios --release`
4. Archive and upload to App Store Connect

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🐛 Troubleshooting

### WebView Not Loading

- Verify backend URL is accessible
- Check internet connectivity
- For emulator: Use `10.0.2.2` instead of `localhost`
- Ensure `INTERNET` permission in AndroidManifest.xml

### Build Failures

```bash
flutter clean
flutter pub get
flutter run
```

### More Help

- Check [FLUTTER_APP_DOCUMENTATION.md](FLUTTER_APP_DOCUMENTATION.md#troubleshooting)
- Run `flutter doctor -v`
- View logs with `flutter logs`

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| webview_flutter | ^4.0.0 | WebView integration |
| flutter_native_splash | ^2.4.0 | Custom splash screen |
| flutter_launcher_icons | ^0.13.1 | Custom app icons |
| cupertino_icons | ^1.0.8 | iOS-style icons |

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly on both Android and iOS
4. Submit a pull request

## 📄 License

Proprietary - All rights reserved

## 🔗 Related Projects

- **Tur'Eco Web Application** - Django backend (in `django_wp/` directory)

## 📞 Support

For issues or questions:
- Create an issue in the repository
- Contact the development team
- Check documentation files

## 🎯 Roadmap

- [ ] Push notifications support
- [ ] Offline data caching
- [ ] Deep linking support
- [ ] Biometric authentication
- [ ] Dark mode support
- [ ] Multi-language support

## 📊 App Statistics

- **App Size**: ~15 MB (Android APK)
- **Minimum API Level**: Android 21 (Lollipop)
- **Supported Architectures**: ARM64, ARMv7, x86_64

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Maintained by**: Tur'Eco Development Team

For more information, see the [complete documentation](FLUTTER_APP_DOCUMENTATION.md).
