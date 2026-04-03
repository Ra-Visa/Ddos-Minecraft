[app]
# ឈ្មោះ App ពេលដំឡើងលើទូរសព្ទ
title = Ddos Minecraft

# ឈ្មោះកញ្ចប់ App (Package)
package.name = ddos-Minecraft
package.domain = com.cyber.ghost

# ប្រភពកូដ (ទីតាំងដែលដាក់ main.py)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# ជំនាន់ App
version = 1.0.0

# --- គ្រឿងផ្សំ (Requirements) ---
# សំខាន់បំផុត៖ ត្រូវមាន requests ដើម្បីឆែក Key ក្នុង Firebase
requirements = python3, kivy==2.3.0, requests, urllib3, charset-normalizer, idna

# ការកំណត់អេក្រង់ (Orientation)
orientation = portrait

# --- Android Specific ---
# អាសយដ្ឋាន Permissions
android.permissions = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE

# កំណត់កម្រិត Android (API 33 គឺសម្រាប់ Android 13 ឡើង)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# រូបតំណាង App (Icon) - បើបងមានរូប icon.png ក្នុង Folder
# icon.filename = %(source.dir)s/data/icon.png

# បិទអេក្រង់ខ្មៅពេលបើក App ដំបូង (Presplash)
android.presplash_color = #0A0A0A

# --- Buildozer Settings ---
log_level = 2
warn_on_root = 1

[buildozer]
bin_dir = ./bin
