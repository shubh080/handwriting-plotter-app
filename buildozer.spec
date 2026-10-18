[app]

# (str) Title of your application
title = Plotter Controller

# (str) Package name
package.name = plottercontroller

# (str) Package domain (needed for android packaging)
package.domain = org.plotter

# (str) Main application file (points directly to your app.py)
source.main_filename = app.py

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Version of your application
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (int) Fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (list) Features
android.features = android.hardware.usb.host

# (bool) Use private data storage
android.private_storage = True

# (int) Target Android API
android.api = 31
android.minapi = 21

# Automatically accept Android SDK licenses
android.accept_sdk_license = True

[buildozer]

# (int) Log level
log_level = 2

# (int) Display warning if run as root
warn_on_root = 0
