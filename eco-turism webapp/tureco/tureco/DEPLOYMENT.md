# Tur'Eco Flutter App - Deployment Guide

## Overview

This guide covers deploying the Tur'Eco Flutter mobile application to production environments including Google Play Store (Android) and Apple App Store (iOS).

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Android Deployment](#android-deployment)
3. [iOS Deployment](#ios-deployment)
4. [Post-Deployment](#post-deployment)
5. [CI/CD Setup](#cicd-setup)

---

## Pre-Deployment Checklist

### Code Preparation

- [ ] Update backend URL to production in `lib/main.dart`
- [ ] Remove all debug logs and print statements
- [ ] Test on multiple devices and screen sizes
- [ ] Verify all features work offline/online
- [ ] Update version number in `pubspec.yaml`
- [ ] Update changelog
- [ ] Run `flutter analyze` and fix all issues
- [ ] Run `flutter test` and ensure all tests pass

### Assets & Metadata

- [ ] Verify app icon (1024x1024 PNG)
- [ ] Verify splash screen
- [ ] Prepare store listing screenshots (see sizes below)
- [ ] Write store description
- [ ] Prepare privacy policy URL
- [ ] Prepare terms of service URL

### Legal & Compliance

- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] GDPR compliance verified
- [ ] Age rating determined
- [ ] Content rating questionnaire completed

---

## Android Deployment

### 1. App Signing Setup

#### Generate Upload Keystore

```bash
# Navigate to android directory
cd android/app

# Generate keystore (Windows PowerShell)
keytool -genkey -v -keystore upload-keystore.jks -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# You'll be prompted for:
# - Password (remember this!)
# - Name
# - Organization
# - City
# - State
# - Country Code
```

**IMPORTANT**: Save the password and alias securely! You'll need them forever.

#### Create key.properties

Create `android/key.properties`:

```properties
storePassword=YOUR_STORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=upload
storeFile=upload-keystore.jks
```

**⚠️ NEVER commit this file to version control!**

Add to `.gitignore`:
```
**/android/key.properties
**/android/app/upload-keystore.jks
```

#### Configure build.gradle

**File**: `android/app/build.gradle.kts`

Add before `android` block:

```kotlin
// Load keystore properties
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    // ... existing config
    
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

### 2. Update App Configuration

#### AndroidManifest.xml

**File**: `android/app/src/main/AndroidManifest.xml`

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.tureco.app">  <!-- Update package name -->
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        android:label="Tur'Eco"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:usesCleartextTraffic="false">  <!-- Set to false for HTTPS -->
        
        <!-- Rest of config -->
    </application>
</manifest>
```

#### build.gradle.kts

**File**: `android/app/build.gradle.kts`

Update:

```kotlin
android {
    namespace = "com.tureco.app"
    compileSdk = 34
    
    defaultConfig {
        applicationId = "com.tureco.app"  // Unique package name
        minSdk = 21
        targetSdk = 34
        versionCode = flutterVersionCode.toInt()
        versionName = flutterVersionName
    }
    
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

### 3. Build Release APK/AAB

#### Build App Bundle (Recommended for Play Store)

```bash
flutter build appbundle --release
```

Output: `build/app/outputs/bundle/release/app-release.aab`

#### Build APK (For direct distribution)

```bash
# Single APK
flutter build apk --release

# Split APKs by architecture (smaller size)
flutter build apk --split-per-abi --release
```

Output: `build/app/outputs/flutter-apk/app-release.apk`

#### Build with Optimization

```bash
flutter build appbundle --release \
  --obfuscate \
  --split-debug-info=build/app/outputs/symbols
```

**Flags**:
- `--obfuscate`: Obscures code
- `--split-debug-info`: Saves symbols for crash reports

### 4. Google Play Console Setup

#### Create Application

1. Go to [Google Play Console](https://play.google.com/console/)
2. Click "Create app"
3. Fill in app details:
   - App name: Tur'Eco
   - Default language: Romanian/English
   - App/Game: App
   - Free/Paid: Free

#### Store Listing

**Required Assets**:

1. **App Icon**: 512x512 PNG
2. **Feature Graphic**: 1024x500 PNG
3. **Screenshots**:
   - Phone: At least 2, up to 8 (1080x1920 or 720x1280)
   - 7" Tablet: At least 2 (1200x1920 or 900x1440)
   - 10" Tablet: At least 2 (1536x2048 or 1152x1536)

**Text Content**:
- Short description (80 chars max)
- Full description (4000 chars max)
- App category
- Contact email
- Privacy policy URL

#### Content Rating

1. Go to "Content rating"
2. Fill out questionnaire
3. Submit for rating

#### Pricing & Distribution

1. Select countries
2. Set pricing (Free)
3. Agree to content guidelines

### 5. Upload & Release

#### Internal Testing (Recommended First)

1. Go to "Internal testing"
2. Create release
3. Upload AAB file
4. Add release notes
5. Review and rollout

#### Production Release

1. Go to "Production"
2. Create release
3. Upload AAB
4. Set rollout percentage (start with 20%)
5. Add release notes
6. Review and publish

**Release Notes Template**:
```
Version 1.0.0
- Initial release
- Browse eco-tourism destinations
- Book accommodations
- Read reviews
- User account management
```

---

## iOS Deployment

### Prerequisites

- macOS with Xcode installed
- Apple Developer Account ($99/year)
- iPhone/iPad for testing

### 1. Xcode Configuration

#### Open iOS Project

```bash
cd ios
open Runner.xcworkspace
```

#### Configure App Identity

1. Select "Runner" in Xcode
2. Go to "Signing & Capabilities"
3. Select your Team
4. Update Bundle Identifier: `com.tureco.app`
5. Enable "Automatically manage signing"

#### Update Info.plist

**File**: `ios/Runner/Info.plist`

```xml
<key>CFBundleName</key>
<string>Tur'Eco</string>

<key>CFBundleDisplayName</key>
<string>Tur'Eco</string>

<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>

<key>CFBundleVersion</key>
<string>$(FLUTTER_BUILD_NUMBER)</string>

<key>CFBundleShortVersionString</key>
<string>$(FLUTTER_BUILD_NAME)</string>

<!-- For HTTP (if not using HTTPS) -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

### 2. App Store Connect Setup

#### Create App

1. Go to [App Store Connect](https://appstoreconnect.apple.com/)
2. Click "My Apps" > "+"
3. Fill in details:
   - Name: Tur'Eco
   - Primary Language: Romanian/English
   - Bundle ID: com.tureco.app
   - SKU: tureco-app

#### Prepare Metadata

**Required Assets**:

1. **App Icon**: 1024x1024 PNG (no transparency)
2. **Screenshots**:
   - 6.5" iPhone: 1284x2778 (at least 1)
   - 5.5" iPhone: 1242x2208 (at least 1)
   - iPad Pro 12.9": 2048x2732 (optional)

**Text Content**:
- Name (30 chars)
- Subtitle (30 chars)
- Description (4000 chars)
- Keywords (100 chars)
- Support URL
- Marketing URL (optional)
- Privacy Policy URL

### 3. Build & Archive

#### Build for Release

```bash
flutter build ios --release
```

#### Archive in Xcode

1. Open `ios/Runner.xcworkspace` in Xcode
2. Select "Any iOS Device" as target
3. Product > Archive
4. Wait for archive to complete

#### Upload to App Store

1. Window > Organizer
2. Select your archive
3. Click "Distribute App"
4. Select "App Store Connect"
5. Click "Upload"
6. Wait for processing (15-60 minutes)

### 4. TestFlight (Beta Testing)

1. Go to App Store Connect
2. Select your app
3. Go to "TestFlight"
4. Select build
5. Add internal testers
6. Submit for external testing (optional)

### 5. Submit for Review

1. Go to "App Store"
2. Create version (e.g., 1.0.0)
3. Fill in "What's New in This Version"
4. Add screenshots
5. Select build
6. Fill in App Review Information:
   - Contact info
   - Demo account (if login required)
   - Notes for reviewer
7. Submit for review

**Review Timeline**: Usually 24-48 hours

---

## Post-Deployment

### Monitor Release

#### Google Play Console

1. Check crash reports
2. Monitor user reviews
3. Track installation metrics
4. Check ANR (App Not Responding) rate

#### App Store Connect

1. Check crash reports
2. Monitor reviews
3. Track downloads
4. Check App Analytics

### Respond to Reviews

- Thank positive reviews
- Address negative reviews professionally
- Fix reported bugs quickly

### Update Strategy

#### Version Numbering

Use semantic versioning: `MAJOR.MINOR.PATCH+BUILD`

- **MAJOR**: Breaking changes
- **MINOR**: New features
- **PATCH**: Bug fixes
- **BUILD**: Incremental build number

Example: `1.2.3+15`

#### Update Process

1. Fix bugs or add features
2. Update version in `pubspec.yaml`
3. Test thoroughly
4. Build release
5. Upload to stores
6. Write release notes

#### Staged Rollout

**Google Play**:
1. Start with 20% rollout
2. Monitor for 24 hours
3. Increase to 50% if stable
4. Increase to 100%

**App Store**:
1. Use phased release (automatic)
2. Pause if issues detected

---

## CI/CD Setup

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.8.1'
      
      - run: flutter pub get
      
      - name: Build APK
        run: flutter build apk --release
      
      - name: Upload to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.SERVICE_ACCOUNT_JSON }}
          packageName: com.tureco.app
          releaseFiles: build/app/outputs/bundle/release/app-release.aab
          track: production

  deploy-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.8.1'
      
      - run: flutter pub get
      
      - name: Build iOS
        run: flutter build ios --release --no-codesign
      
      - name: Upload to TestFlight
        uses: apple-actions/upload-testflight-build@v1
        with:
          app-path: build/ios/iphoneos/Runner.app
          issuer-id: ${{ secrets.APPSTORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APPSTORE_API_KEY_ID }}
          api-private-key: ${{ secrets.APPSTORE_API_PRIVATE_KEY }}
```

### Fastlane Setup (Alternative)

#### Install Fastlane

```bash
# macOS
brew install fastlane

# Or with Ruby
gem install fastlane
```

#### Configure Android

`android/fastlane/Fastfile`:

```ruby
platform :android do
  desc "Deploy to Play Store"
  lane :deploy do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(
      track: 'production',
      aab: '../build/app/outputs/bundle/release/app-release.aab'
    )
  end
end
```

#### Configure iOS

`ios/fastlane/Fastfile`:

```ruby
platform :ios do
  desc "Deploy to App Store"
  lane :deploy do
    build_app(scheme: "Runner")
    upload_to_app_store(
      skip_metadata: false,
      skip_screenshots: false,
      submit_for_review: true
    )
  end
end
```

---

## Troubleshooting Deployment

### Common Android Issues

**Issue**: "Upload failed: You uploaded an APK with version code X"
- **Solution**: Increment `version` in `pubspec.yaml`

**Issue**: "You need to use a different package name"
- **Solution**: Change `applicationId` in `android/app/build.gradle.kts`

**Issue**: "App not signed properly"
- **Solution**: Verify `key.properties` and signing config

### Common iOS Issues

**Issue**: "Provisioning profile doesn't match"
- **Solution**: Regenerate provisioning profile in Xcode

**Issue**: "Missing compliance"
- **Solution**: Provide export compliance info in App Store Connect

**Issue**: "Invalid bundle"
- **Solution**: Ensure bundle ID matches everywhere

---

## Security Best Practices

1. **Never commit signing keys** to version control
2. **Use environment variables** for sensitive data
3. **Enable code obfuscation** for releases
4. **Use HTTPS** for all network requests
5. **Implement certificate pinning** for production
6. **Store secrets** in secure key storage services

---

## Useful Commands

```bash
# Check app size
flutter build apk --release --target-platform android-arm64 --analyze-size

# Generate build info
flutter build apk --release --build-name=1.0.0 --build-number=1

# Clean before building
flutter clean && flutter pub get && flutter build apk --release

# Test release build locally
flutter run --release
```

---

## Checklist for Each Release

- [ ] Code reviewed and tested
- [ ] Version number incremented
- [ ] Changelog updated
- [ ] Release notes written
- [ ] Signed release built
- [ ] Tested on physical devices
- [ ] Uploaded to stores
- [ ] Submitted for review
- [ ] Monitored for crashes post-release

---

**Last Updated**: January 2026
**Version**: 1.0.0
