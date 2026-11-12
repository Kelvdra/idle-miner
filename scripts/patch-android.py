#!/usr/bin/env python3
"""Dipanggil CI setelah `npx cap add android`.

Menambahkan konfigurasi tanda tangan release ke android/app/build.gradle
(kunci dibaca dari environment variable) dan mengisi versionCode / versionName.

Env wajib: KEYSTORE_PATH, KEYSTORE_PASSWORD, KEY_ALIAS, KEY_PASSWORD,
           VERSION_NAME, VERSION_CODE
"""
import os
import pathlib
import re
import sys

path = pathlib.Path("android/app/build.gradle")
src = path.read_text()
s = src

for var in ("KEYSTORE_PATH", "KEYSTORE_PASSWORD", "KEY_ALIAS", "KEY_PASSWORD", "VERSION_NAME", "VERSION_CODE"):
    if not os.environ.get(var):
        sys.exit(f"Env {var} belum diisi")

code = os.environ["VERSION_CODE"]
name = os.environ["VERSION_NAME"]

signing = '''    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_PATH"))
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
'''

# 1. blok signingConfigs sebelum buildTypes
s, n1 = re.subn(r"^([ \t]*)buildTypes\s*\{", lambda m: signing + m.group(0), s, count=1, flags=re.M)
# 2. pakai signingConfig di build type release
s, n2 = re.subn(r"(buildTypes\s*\{\s*release\s*\{)", r"\1\n            signingConfig signingConfigs.release", s, count=1)
# 3. versi
s, n3 = re.subn(r"versionCode\s+\d+", f"versionCode {code}", s, count=1)
s, n4 = re.subn(r'versionName\s+"[^"]*"', f'versionName "{name}"', s, count=1)

if not (n1 and n2 and n3 and n4):
    print(src)
    sys.exit(f"Gagal menambal build.gradle (buildTypes={n1}, release={n2}, versionCode={n3}, versionName={n4}). Isi file dicetak di atas.")

path.write_text(s)
print(f"OK: versionName={name} versionCode={code}, signing release aktif")
