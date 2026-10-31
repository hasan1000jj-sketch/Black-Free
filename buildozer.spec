[app]
title = X Black
package.name = xblack
package.domain = org.xblack
source.dir = .
source.include_exts = py,kv,png,jpg,json,txt
version = 1.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 35
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
