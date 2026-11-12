#!/usr/bin/env bash
# Membuat keystore untuk menandatangani aplikasi. JALANKAN SEKALI SAJA di komputermu.
# Butuh JDK (perintah keytool). Hasil: release.keystore + keystore.b64
set -euo pipefail

ALIAS="${1:-tambangemas}"

if [ -f release.keystore ]; then
  echo "release.keystore sudah ada. Hapus dulu kalau memang mau membuat ulang." >&2
  exit 1
fi

echo "Alias kunci: $ALIAS"
echo "Kamu akan diminta membuat password (catat!) dan mengisi nama/organisasi."
echo

keytool -genkeypair -v \
  -storetype PKCS12 \
  -keystore release.keystore \
  -alias "$ALIAS" \
  -keyalg RSA -keysize 2048 -validity 10000

# base64 satu baris (Linux: -w0, macOS: tanpa -w)
if base64 --help 2>&1 | grep -q -- '-w'; then
  base64 -w0 release.keystore > keystore.b64
else
  base64 -i release.keystore | tr -d '\n' > keystore.b64
fi

cat <<EOF

Selesai. Sekarang buat 4 secret di GitHub
(Settings > Secrets and variables > Actions > New repository secret):

  KEYSTORE_BASE64    = isi file keystore.b64
  KEYSTORE_PASSWORD  = password yang barusan kamu buat
  KEY_ALIAS          = $ALIAS
  KEY_PASSWORD       = sama dengan KEYSTORE_PASSWORD (format PKCS12)

PENTING:
  - Simpan release.keystore dan passwordnya di tempat aman (password manager / cloud pribadi).
  - JANGAN commit file ini ke repo (sudah ada di .gitignore).
  - Kalau hilang dan kamu tidak memakai Play App Signing, aplikasi tidak bisa diupdate lagi.
EOF
