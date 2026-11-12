# Tambang Emas Idle

Game idle tambang offline (HTML5, tanpa framework). Bisa dimainkan di browser, di-install sebagai PWA, atau dibuild jadi aplikasi Android (APK + AAB untuk Play Store).

## Struktur

```
www/                      <- seluruh game (statis)
assets/                   <- ikon & splash screen sumber (untuk Android)
scripts/
  make-keystore.sh        <- bikin kunci penandatangan (sekali saja)
  patch-android.py        <- dipakai CI: pasang signing + versi
capacitor.config.json     <- pembungkus Android (appId, nama app)
.github/workflows/
  release.yml             <- tag v* -> Release berisi .zip web, .apk, .aab (bertanda tangan)
  pages.yml               <- tag v* -> deploy ke GitHub Pages (opsional)
```

## Langkah 1: ganti ID aplikasi

Buka `capacitor.config.json` dan ubah `appId` (sekarang `app.tambangemas.idle`) menjadi ID unik milikmu, misalnya `com.namamu.tambangemas`. **ID ini tidak bisa diubah lagi setelah diunggah ke Play Store.** Play Store menolak ID berawalan `com.example`.

## Langkah 2: buat kunci penandatangan (sekali seumur aplikasi)

Butuh JDK di komputermu.

```bash
bash scripts/make-keystore.sh
```

Skrip membuat `release.keystore` dan `keystore.b64`. Lalu di GitHub: **Settings → Secrets and variables → Actions → New repository secret**, buat 4 secret:

| Secret | Isi |
|---|---|
| `KEYSTORE_BASE64` | isi file `keystore.b64` |
| `KEYSTORE_PASSWORD` | password yang kamu buat |
| `KEY_ALIAS` | `tambangemas` (atau alias yang kamu pilih) |
| `KEY_PASSWORD` | sama dengan `KEYSTORE_PASSWORD` |

Simpan `release.keystore` + password di tempat aman. Jangan di-commit (sudah di `.gitignore`).

## Langkah 3: rilis lewat git tag

```bash
git add .
git commit -m "versi pertama"
git push origin main

git tag v1.0.0
git push origin v1.0.0
```

Di tab **Actions** akan jalan:

| Workflow | Hasil |
|---|---|
| Release | Release `v1.0.0` berisi `.zip` web, `tambang-emas-idle-v1.0.0.apk` (untuk install langsung), dan `tambang-emas-idle-v1.0.0.aab` (untuk Play Store) |
| Deploy Pages | Game online di `https://USERNAME.github.io/NAMA-REPO/` (opsional) |

Nomor versi diambil dari tag: `v1.2.3` jadi versionName `1.2.3` dan versionCode `10203`. versionCode harus selalu naik untuk setiap unggahan ke Play Store, jadi setiap rilis baru cukup pakai tag yang lebih besar. Tag boleh non-semver (mis. `v1.0-beta`), tapi versionCode lalu diambil dari nomor run Actions.

### Pengaturan GitHub satu kali

1. **Settings → Actions → General → Workflow permissions**: pilih *Read and write permissions*.
2. Pages (opsional): **Settings → Pages → Source = GitHub Actions**, lalu di **Settings → Environments → github-pages** izinkan tag `v*`. Tidak mau Pages? Hapus `pages.yml`.

## Langkah 4: unggah ke Google Play

1. Daftar akun [Play Console](https://play.google.com/console) (biaya sekali bayar US$25, butuh verifikasi identitas).
2. Buat aplikasi baru, isi data toko (deskripsi, screenshot, ikon 512×512 ada di `www/icon-512.png`), kebijakan privasi, kuesioner rating konten, dan Data safety. Game ini tidak mengumpulkan data apa pun dan tidak butuh internet.
3. Unggah file **`.aab`** dari halaman Release ke jalur Internal testing atau Production. Aktifkan *Play App Signing* saat diminta.
4. Akun pribadi baru biasanya wajib menjalankan closed testing dengan sejumlah penguji selama beberapa minggu sebelum boleh rilis produksi. Cek syarat terbaru di Play Console.

Syarat target SDK: sejak 31 Agustus 2026 aplikasi baru dan update harus menargetkan Android 16 (API 36). Capacitor 8 sudah menargetkan API 36.

## Install APK langsung (tanpa Play Store)

Unduh `.apk` dari halaman Release, kirim ke HP, lalu buka. Android akan meminta izin "install dari sumber tidak dikenal".

## Menjalankan lokal

Buka `www/index.html` di browser, atau `npm start`.

## Catatan

- Progres game tersimpan otomatis di penyimpanan lokal perangkat; uninstall aplikasi menghapusnya.
- Build Android memakai Node 22 dan JDK 21 (persyaratan Capacitor 8). Workflow ini belum pernah dijalankan di GitHub. Kalau ada langkah yang gagal, salin lognya dan saya bantu perbaiki.
