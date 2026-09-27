```ini
[app]

# (str) Title of your application
title = Argentum - Competencia de Rap

# (str) Package name
package.name = argentum

# (str) Package domain
package.domain = com.argentum.app

# (str) Source code where main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

# (str) Application version
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0


# ------------------------------------------------------------------
# Android
# ------------------------------------------------------------------

# (bool) Accept Android SDK license
android.accept_sdk_license = True

# (str) Android API target
android.api = 35

# (str) Minimum API supported
android.minapi = 23

# (str) Android SDK version
android.sdk = 35

# (str) Android NDK version
android.ndk = 27c

# (str) Android orientation
android.orientation = portrait

# (list) Android permissions
android.permissions = INTERNET

# (list) Architectures
android.archs = arm64-v8a,armeabi-v7a


# ------------------------------------------------------------------
# Buildozer
# ------------------------------------------------------------------

# (int) Log level
log_level = 2

# (bool) Warn if buildozer is run as root
warn_on_root = 0
```
