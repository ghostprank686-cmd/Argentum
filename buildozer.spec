[app]
# (str) Title of your application
 title = Argentum - Competencias de Rap
# (str) Package name
package.name = argentum
# (str) Package domain (needed for android/ios packaging)
package.domain = com.argentum.app
# (str) Source code where main.py live
source.dir = .
# (str) Main filename
source.main = main.py
# (list) Source files to include
source.include_exts = py,json,png,jpg,jpeg,kv,atlas
# (str) Application version
version = 1.0.0
# (list) Application requirements
requirements = python3,kivy
# (str) Supported orientation (portrait, landscape, all)
orientation = portrait
# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]
# (str) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
# (str) Warn if buildozer is run as root
warn_on_root = 0

[app:android]
# (str) Android API target
android.api = 35
# (str) Minimum API supported
android.minapi = 23
# (str) Android SDK version to use
android.sdk = 35
# (str) Android NDK version
android.ndk = 27c
# (str) Android app orientation
android.orientation = portrait
# (str) Permissions
android.permissions = INTERNET
# (str) Architecture to build for
android.archs = arm64-v8a,armeabi-v7a
# (bool) Keep the app fullscreen
fullscreen = 0
