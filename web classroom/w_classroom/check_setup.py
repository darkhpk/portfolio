"""
Startup diagnostics for the classroom app
Run this to check for common configuration issues
"""

import sys
import os

print("=" * 60)
print("DJANGO CLASSROOM - STARTUP DIAGNOSTICS")
print("=" * 60)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check installed packages
print("\n📦 Checking required packages...")
required_packages = {
    'django': 'Django',
    'channels': 'Channels',
    'daphne': 'Daphne',
}

missing = []
for module, name in required_packages.items():
    try:
        __import__(module)
        print(f"  ✓ {name} is installed")
    except ImportError:
        print(f"  ✗ {name} is NOT installed")
        missing.append(name)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("   Run: pip install -r requirements.txt")
else:
    print("\n✓ All required packages are installed")

# Check settings module
print("\n⚙️  Checking Django settings...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'w_classroom.settings')

try:
    import django
    django.setup()
    print("  ✓ Django settings loaded successfully")
    
    from django.conf import settings
    print(f"  ✓ ASGI_APPLICATION: {settings.ASGI_APPLICATION}")
    print(f"  ✓ Channel layers backend: {settings.CHANNEL_LAYERS['default']['BACKEND']}")
    
except Exception as e:
    print(f"  ✗ Error loading Django: {e}")
    sys.exit(1)

# Check migrations
print("\n🗄️  Checking migrations...")
from django.core.management import call_command
from io import StringIO
import sys

buffer = StringIO()
try:
    call_command('showmigrations', '--plan', stdout=buffer, no_color=True)
    output = buffer.getvalue()
    if '[X]' in output or output.strip():
        print("  ✓ Migrations appear to be applied")
    else:
        print("  ⚠️  No migrations found - you may need to run:")
        print("     python manage.py makemigrations")
        print("     python manage.py migrate")
except Exception as e:
    print(f"  ⚠️  Could not check migrations: {e}")

# Check routing
print("\n🌐 Checking WebSocket routing...")
try:
    from classroom.routing import websocket_urlpatterns
    print(f"  ✓ WebSocket URL patterns loaded ({len(websocket_urlpatterns)} routes)")
except Exception as e:
    print(f"  ✗ Error loading routing: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)
print("\nIf everything looks good, start the server with:")
print("  python manage.py runserver")
print("\nThen visit: http://localhost:8000")
print("=" * 60)
