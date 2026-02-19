# Flutter App API Reference

## Main Components

### TurecoApp
**Type**: `StatelessWidget`  
**Purpose**: Root application widget

```dart
class TurecoApp extends StatelessWidget {
  const TurecoApp({super.key});
  
  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Tur'Eco",
      home: WebAppScreen(),
    );
  }
}
```

**Properties**:
- `debugShowCheckedModeBanner`: `false` - Hides debug banner in top-right corner
- `title`: `"Tur'Eco"` - App title used by OS
- `home`: `WebAppScreen()` - Initial route/screen

---

### WebAppScreen
**Type**: `StatefulWidget`  
**Purpose**: Main screen containing WebView

```dart
class WebAppScreen extends StatefulWidget {
  const WebAppScreen({super.key});
  
  @override
  State<WebAppScreen> createState() => _WebAppScreenState();
}
```

---

### _WebAppScreenState
**Type**: `State<WebAppScreen>`  
**Purpose**: Manages WebView state and logic

#### Properties

```dart
late final WebViewController _controller;
bool _isLoading = true;
```

- **`_controller`**: WebViewController instance for managing WebView
- **`_isLoading`**: Loading state indicator

#### Methods

##### initState()
**Purpose**: Initialize WebView controller and configuration

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
    ..loadRequest(Uri.parse('http://87.106.96.193:80'));
}
```

**Configuration**:
- JavaScript enabled (unrestricted mode)
- Navigation delegate for loading states
- Initial URL load

##### build()
**Purpose**: Build widget tree with WebView and navigation handling

```dart
@override
Widget build(BuildContext context) {
  return PopScope(
    canPop: false,
    onPopInvokedWithResult: (didPop, result) async {
      if (didPop) return;
      
      if (await _controller.canGoBack()) {
        _controller.goBack();
        return;
      }
      
      if (!mounted) return;
      Navigator.of(context).maybePop();
    },
    child: Scaffold(
      body: Stack(
        children: [
          Positioned.fill(child: WebViewWidget(controller: _controller)),
          if (_isLoading) const Center(child: CircularProgressIndicator()),
        ],
      ),
    ),
  );
}
```

**Widget Tree**:
```
PopScope
  └── Scaffold
      └── Stack
          ├── WebViewWidget (full screen)
          └── CircularProgressIndicator (when loading)
```

---

## WebViewController API

### Configuration Methods

#### setJavaScriptMode()
**Purpose**: Enable/disable JavaScript execution

```dart
_controller.setJavaScriptMode(JavaScriptMode.unrestricted)
```

**Options**:
- `JavaScriptMode.unrestricted` - JavaScript fully enabled
- `JavaScriptMode.disabled` - JavaScript disabled

#### setNavigationDelegate()
**Purpose**: Handle navigation events

```dart
_controller.setNavigationDelegate(
  NavigationDelegate(
    onPageStarted: (String url) {
      // Called when page starts loading
    },
    onPageFinished: (String url) {
      // Called when page finishes loading
    },
    onWebResourceError: (WebResourceError error) {
      // Called on loading errors
    },
    onNavigationRequest: (NavigationRequest request) {
      // Called before navigation
      // Return NavigationDecision.prevent to block
      // Return NavigationDecision.navigate to allow
    },
  ),
)
```

#### loadRequest()
**Purpose**: Load URL in WebView

```dart
_controller.loadRequest(Uri.parse('https://example.com'))
```

### Navigation Methods

#### goBack()
**Purpose**: Navigate to previous page in history

```dart
await _controller.goBack()
```

#### goForward()
**Purpose**: Navigate to next page in history

```dart
await _controller.goForward()
```

#### reload()
**Purpose**: Reload current page

```dart
await _controller.reload()
```

#### canGoBack()
**Purpose**: Check if back navigation is possible

```dart
bool canGoBack = await _controller.canGoBack()
```

**Returns**: `bool` - `true` if WebView can go back

#### canGoForward()
**Purpose**: Check if forward navigation is possible

```dart
bool canGoForward = await _controller.canGoForward()
```

**Returns**: `bool` - `true` if WebView can go forward

### Content Methods

#### runJavaScript()
**Purpose**: Execute JavaScript in WebView

```dart
await _controller.runJavaScript('alert("Hello from Flutter!")')
```

#### runJavaScriptReturningResult()
**Purpose**: Execute JavaScript and get return value

```dart
final result = await _controller.runJavaScriptReturningResult(
  'document.title'
);
```

**Returns**: `Future<Object>` - JavaScript return value

#### addJavaScriptChannel()
**Purpose**: Create bridge for JavaScript to call Flutter

```dart
_controller.addJavaScriptChannel(
  'FlutterChannel',
  onMessageReceived: (JavaScriptMessage message) {
    print('From JS: ${message.message}');
  },
)
```

**JavaScript Side**:
```javascript
FlutterChannel.postMessage('Hello Flutter!');
```

---

## PopScope Widget

**Purpose**: Handle back button/gesture navigation

```dart
PopScope(
  canPop: false,  // Prevents immediate pop
  onPopInvokedWithResult: (bool didPop, dynamic result) async {
    // Custom navigation logic
  },
  child: Widget(),
)
```

**Parameters**:
- `canPop`: `bool` - If `false`, prevents automatic pop
- `onPopInvokedWithResult`: Callback for handling pop attempts
  - `didPop`: `bool` - Whether pop already happened
  - `result`: Dynamic result from pop (if any)

**Use Case**: Handle Android back button to navigate WebView history before closing app

---

## NavigationDelegate Callbacks

### onPageStarted
**Called**: When page starts loading

```dart
onPageStarted: (String url) {
  print('Started loading: $url');
  setState(() => _isLoading = true);
}
```

### onPageFinished
**Called**: When page completes loading

```dart
onPageFinished: (String url) {
  print('Finished loading: $url');
  setState(() => _isLoading = false);
}
```

### onWebResourceError
**Called**: When loading error occurs

```dart
onWebResourceError: (WebResourceError error) {
  print('Error: ${error.description}');
  print('Error code: ${error.errorCode}');
}
```

**WebResourceError Properties**:
- `errorCode`: `int` - Error code
- `description`: `String` - Error description
- `errorType`: `WebResourceErrorType?` - Error type enum

### onNavigationRequest
**Called**: Before navigation occurs

```dart
onNavigationRequest: (NavigationRequest request) {
  if (request.url.startsWith('https://blocked.com')) {
    return NavigationDecision.prevent;
  }
  return NavigationDecision.navigate;
}
```

**Returns**: `NavigationDecision`
- `NavigationDecision.navigate` - Allow navigation
- `NavigationDecision.prevent` - Block navigation

---

## Extension Examples

### 1. Add Cookie Management

```dart
import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';
import 'package:webview_flutter_android/webview_flutter_android.dart';

// In initState
if (_controller.platform is AndroidWebViewController) {
  final androidController = _controller.platform as AndroidWebViewController;
  androidController.setMediaPlaybackRequiresUserGesture(false);
}
```

### 2. Add Download Handler

```dart
_controller.setDownloadHandler((String url) async {
  // Handle downloads
  print('Downloading: $url');
});
```

### 3. Add Custom User Agent

```dart
_controller.setUserAgent('TurecoApp/1.0');
```

### 4. Add Custom Headers

```dart
_controller.loadRequest(
  Uri.parse('https://example.com'),
  headers: {'Authorization': 'Bearer token123'},
);
```

### 5. Add Error Page

```dart
onWebResourceError: (WebResourceError error) {
  _controller.loadHtmlString('''
    <html>
      <body>
        <h1>Error Loading Page</h1>
        <p>${error.description}</p>
      </body>
    </html>
  ''');
}
```

---

## Constants & Configuration

### Backend URLs

```dart
// Production
const String PRODUCTION_URL = 'http://87.106.96.193:80';

// Development
const String DEV_URL_ANDROID_EMULATOR = 'http://10.0.2.2:8000';
const String DEV_URL_IOS_SIMULATOR = 'http://localhost:8000';
const String DEV_URL_PHYSICAL_DEVICE = 'http://192.168.1.X:8000';
```

### JavaScript Modes

```dart
enum JavaScriptMode {
  disabled,      // JavaScript completely disabled
  unrestricted,  // JavaScript fully enabled
}
```

### Navigation Decisions

```dart
enum NavigationDecision {
  navigate,  // Allow the navigation
  prevent,   // Block the navigation
}
```

---

## Common Patterns

### Pattern: Refresh WebView

```dart
IconButton(
  icon: Icon(Icons.refresh),
  onPressed: () => _controller.reload(),
)
```

### Pattern: Go Back

```dart
IconButton(
  icon: Icon(Icons.arrow_back),
  onPressed: () async {
    if (await _controller.canGoBack()) {
      _controller.goBack();
    }
  },
)
```

### Pattern: Share Current URL

```dart
IconButton(
  icon: Icon(Icons.share),
  onPressed: () async {
    final url = await _controller.currentUrl();
    // Use share package to share URL
  },
)
```

### Pattern: Check Network Status

```dart
import 'package:connectivity_plus/connectivity_plus.dart';

Connectivity().onConnectivityChanged.listen((ConnectivityResult result) {
  if (result == ConnectivityResult.none) {
    // Show offline message
  } else {
    _controller.reload();
  }
});
```

---

## Testing Helpers

### Mock WebViewController

```dart
class MockWebViewController extends Mock implements WebViewController {}
```

### Test Navigation

```dart
testWidgets('Back button navigates WebView', (WidgetTester tester) async {
  final controller = MockWebViewController();
  when(controller.canGoBack()).thenAnswer((_) async => true);
  
  await tester.pumpWidget(WebAppScreen());
  await tester.tap(find.byType(BackButton));
  
  verify(controller.goBack()).called(1);
});
```

---

## Performance Tips

1. **Enable Caching**:
```dart
_controller.enableZoom(false);  // Disable zoom for better performance
```

2. **Optimize Loading**:
```dart
onPageStarted: (url) {
  // Cancel pending loads if needed
}
```

3. **Memory Management**:
```dart
@override
void dispose() {
  // WebViewController is automatically disposed
  super.dispose();
}
```

---

**Version**: 1.0.0  
**Last Updated**: January 2026
