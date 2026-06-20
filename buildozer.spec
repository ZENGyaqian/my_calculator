[app]

# (str) Title of your application
title = 我的计算器

# (str) Package name
package.name = mycalculator

# (str) Package domain (used for the APK ID, e.g. org.example.myapp)
package.domain = com.test

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) Requirements (libraries your app uses)
requirements = python3,kivy

# (str) Application version
version = 0.1

# (int) Android API level (target SDK)
android.api = 31

# (int) Minimum Android API level
android.minapi = 21

# (list) Android architectures to build for
android.archs = arm64-v8a

# (bool) Enable/disable buildozer's own debug mode
# log_level = 2

# (list) Permissions your app needs
android.permissions = INTERNET

# (str) Presplash image (optional)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon image (optional)
# icon.filename = %(source.dir)s/data/icon.png

# (bool) Allow Android to resize the app when keyboard appears
android.allow_resize = True

# (str) Android NDK version (use a stable one)
android.ndk = 25c

# (list) Android Gradle dependencies (if needed)
# android.gradle_dependencies =

# (str) Android SDK path (if you want to specify manually, leave empty for auto-download)
# android.sdk_path =

# (str) Android NDK path (leave empty for auto-download)
# android.ndk_path =