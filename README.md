# OSIS Space 2.0

Proyek pengganti lengkap untuk Flask + PostgreSQL + Vercel. Tidak ada database lokal, pendaftaran publik, atau kredensial plaintext dalam source aplikasi.

## Penting untuk database lama
Schema mengikuti tabel edisi sebelumnya. schema.sql hanya CREATE IF NOT EXISTS dan INSERT pengaturan ON CONFLICT DO NOTHING. Tidak ada DROP, TRUNCATE, atau reset akun. Cadangkan database sebelum penggantian. Akun lama dan hash PBKDF2 tetap dipakai. Excel kredensial baru HANYA berlaku jika database kosong dan diaktivasi dengan seed baru. Tidak berlaku pada database lama.

## Deploy
1. Upload isi ZIP ke root repo PRIVATE, bukan file ZIP atau folder pembungkus. Pastikan folder templates dan public ikut masuk.
2. Neon/PostgreSQL: jalankan schema.sql pada database yang dipakai DATABASE_URL. Untuk database lama, cek kesesuaian kolom dan buat backup terlebih dahulu.
3. Vercel: import repo, preset Flask, root directory root repo. Jangan gunakan npm build, Next.js, atau output directory dist.
4. Environment production: DATABASE_URL (connection string dengan TLS sesuai provider), SECRET_KEY (acak dan rahasia, minimal 32 karakter), SETUP_TOKEN (acak dan rahasia untuk aktivasi pertama).
5. Deploy. / harus menampilkan halaman. /api/health harus mengirim ok:true. /api/session membutuhkan schema dan environment.
6. Database kosong: masukkan token setup lalu login menggunakan kredensial rebuild yang dibagikan secara pribadi. Semua akun wajib ganti password.
7. Setelah aktivasi, hapus SETUP_TOKEN dan redeploy. Jangan mengganti SECRET_KEY pada setiap deployment.
8. Jika database lama sudah berisi akun, tidak ada aktivasi dan tidak ada perubahan password otomatis.

Vercel melayani public/static/app.css sebagai /static/app.css dan public/static/app.js sebagai /static/app.js. Flask juga punya route static untuk development lokal. Semua CSS/JS eksternal agar sesuai CSP. /api/health tidak mengecek database.

## Lokal
Python 3.12. pip install -r requirements.txt. Atur environment di shell atau runner; .env tidak dimuat otomatis. python app.py. Buka http://127.0.0.1:8000.
python -m unittest discover -s tests -v untuk pengujian core tanpa database.

## Fitur
Dashboard, daftar anggota dengan pencarian, susunan divisi, 21 modul (5 umum + 16 divisi), tambah/edit/hapus catatan sesuai izin, filter divisi, PDF, impor Excel dengan preview dan konfirmasi, CSV keuangan, tambah akun, reset password, ganti password, pengaturan sekolah, tema gelap dan layout mobile.

## Hak akses
Pembina/Ketua: semua. Wakil: agenda/proker/pengumuman dan membaca semua divisi. Sekretaris: agenda/pengumuman/surat/PDF. Bendahara: keuangan. Ketua divisi: modul divisi sendiri dan agenda/proker divisi sendiri. Anggota: tambah catatan modul sendiri dan edit/hapus catatan miliknya. Keuangan dapat dibaca semua akun seperti versi lama. UKS hanya persediaan, bukan rekam kesehatan pribadi.

## Batasan
Belum audit keamanan produksi atau verifikasi deployment live. Batas request 3 MB; frontend membatasi PDF sekitar 2,8 MB untuk metadata. PDF tersimpan BYTEA PostgreSQL, tidak dipindai antivirus. Maksimal 2000 baris impor, decompressed Excel 30 MB. Daftar catatan maksimal 2000 terbaru per modul; dashboard memberi peringatan bila terpotong; ekspor CSV keuangan mencakup semua. Tidak ada pagination lanjutan, hapus/edit profil akun, email reset, atau otomasi backup. Rate limit login IP+username bukan proteksi bot menyeluruh. Credential Excel jangan di-upload ke GitHub atau dikirim ke grup. Jangan publikasikan data siswa tanpa izin.

## Status pengujian
Lihat TEST-REPORT.txt. Pengujian core dan sintaks bukan bukti seluruh integrasi Flask/PostgreSQL berjalan. Jalankan acceptance checklist setelah deploy.

## Acceptance checklist
- /, /static/app.css, /static/app.js, /api/health tidak 404.
- Login salah ditolak; login benar berhasil; password sementara wajib diganti.
- Data tersimpan setelah logout/redeploy.
- Anggota tidak dapat mengedit catatan anggota lain atau menulis divisi lain.
- Ketua divisi tidak bisa memindahkan proker ke divisi lain.
- PDF diunduh hanya akun berwenang.
- Excel invalid tidak disimpan; duplicate exact dilewati.
- Reset password membatalkan sesi lama.
- Uji desktop/mobile dan mode gelap.

Dokumentasi: https://vercel.com/docs/frameworks/backend/flask
https://vercel.com/docs/functions/runtimes/python
