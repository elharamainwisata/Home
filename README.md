# Elharamain Wisata · Halaman Kantor Cabang

Sumber halaman kantor cabang di **elharamainwisata.com** (WordPress.com Atomic, blog ID `257762850`).
Desain mengacu ke ghufrantravel.com, warna brand `#004AAD` / `#1684CF` / emas `#DBC033`, font Poppins + Mulish.

## Halaman yang dikelola

| Kota | Page ID | URL | WA cabang |
|---|---|---|---|
| Bekasi (pusat) | 9584 | /travel-umroh-bekasi/ | 6281287292422 |
| Jakarta | 9585 | /travel-umroh-jakarta/ | 6281214178056 |
| Depok | 9586 | /travel-umroh-depok/ | 6285179988198 |
| Tangerang | 9587 | /travel-umroh-tangerang/ | 6285693883208 |
| Bogor | 9588 | /travel-umroh-bogor/ | 6282260126394 |
| Bandung | 9589 | /travel-umroh-bandung/ | 628132212344 (11 digit, sudah dikonfirmasi pemilik) |

## Halaman paket

Semua halaman dibuat oleh `python3 halaman-paket/build_paket.py`, yang menulis `halaman-paket/halaman/<kunci>.html`.

| Paket | Page ID | URL | Kartu yang diambil dari pattern 9996 |
|---|---|---|---|
| Bronze | 8869 | /umroh-bronze/ | tag `bronze` |
| Silver | 8896 | /paket-umroh-silver/ | tag `silver` selain 12 Hari (termasuk I'tikaf 17 Hari) |
| 12 Hari | 8910 | /umroh-silver-12-hari/ | Silver 12 Hari + Gold 12 Hari |
| Platinum | 8908 | /umroh-platinum/ | tag `platinum` |
| Premium | 8909 | /umroh-premium/ | tag `premium` |
| Syawal | 9935 | /umroh-syawal/ | semua kartu tab Syawal |
| Musim Dingin | 9581 | /paket-umroh-musim-dingin/ | semua kartu Januari + Ramadhan, dikelompokkan per periode |

- **Harga**: setelah mengubah pattern 9996, jalankan ulang `build_paket.py`, lalu pasang ulang isi halaman paket yang berubah.
- **Pattern 10076 "Paket: kartu & rotator WA"** (`halaman-paket/pattern/10076-kartu-rotator.html`): CSS kartu + script rotator WhatsApp.
  - Rotator berisi 7 nomor kantor; nomor ganti di `ROTATOR` di `build_paket.py`, lalu update pattern 10076.
  - Semua link WA ke nomor pusat dialihkan ke satu nomor CS. Nomor itu tetap per pengunjung (localStorage).
  - Jangan pakai `&&` di script inline: wptexturize mengubahnya jadi `&#038;&#038;` dan script rusak.
- **Tidak ada bagian "Paket lain & kantor"**: menu paket ada di header dan daftar kantor ada di footer (permintaan pemilik).
- **Backup sebelum diganti** ada di `backup/2026-10-23_<id>_*`. Rollback Elementor: `_elementor_edit_mode` = `builder`.
  Syawal (9935) dulunya blok khusus (itinerary, FAQ): `backup/2026-10-23_9935_syawal_rendered_sebelum.html` + revisi WordPress.

## Cara kerja

Sejak 23 Okt 2026 keenam halaman **tidak lagi memakai Elementor**. Isinya blok WordPress (`wp:html`) ditambah
**synced pattern** yang dipakai bersama. Edit satu pattern, keenam halaman ikut berubah.

| Pattern | ID | File |
|---|---|---|
| Lebar penuh & perapian (CSS) | 9999 | `halaman-kota/pattern/9999-lebar-penuh-perapian.html` |
| Gaya utama (CSS + font) | 9991 | `halaman-kota/pattern/9991-gaya.html` |
| Layanan eksklusif | 9992 | `halaman-kota/pattern/9992-layanan.html` |
| **Paket & harga** (tab Des / Jan / Ramadhan / Syawal) | 9996 | `halaman-kota/pattern/9996-paket-harga.html` |
| Fasilitas & ketentuan (termasuk DP & rekening) | 9993 | `halaman-kota/pattern/9993-fasilitas-ketentuan.html` |
| Perlengkapan, hotel, dokumentasi | 9995 | `halaman-kota/pattern/9995-perlengkapan-hotel-dokumentasi.html` |
| Testimoni (shortcode Trustindex) | 9994 | `halaman-kota/pattern/9994-testimoni.html` |

Urutan tiap halaman: hero → angka singkat → **kantor** (alamat, telepon, peta, rute, area layanan) → layanan →
**paket & harga** → ketentuan → legalitas → fasilitas → testimoni → kantor lain.
Aturan pemilik: **info paket dan lokasi tidak boleh berulang**. Paket hanya di pattern 9996, lokasi hanya di bagian kantor.

Bagian khusus kota dibuat oleh `halaman-kota/build_kota.py` (data kantor dari repo `khaeruddienfatih/web`):

```
python3 halaman-kota/build_kota.py   # menulis halaman-kota/halaman/<kota>.html
```

Isi file `halaman/<kota>.html` itulah yang dipasang ke halaman WordPress (Code Editor, REST, atau konektor WordPress.com).
Script WA cabang di tiap halaman mengalihkan link nomor pusat ke nomor cabang dan mengunci rotasi Click to Chat.

## Mengubah harga

Edit `halaman-kota/pattern/9996-paket-harga.html`, lalu ganti isi synced pattern 9996
(wp-admin → Tampilan/Editor → Pola, atau konektor `synced-patterns.update`). Semua kota langsung ikut.

## Rollback ke versi Elementor lama

Data Elementor lama **tidak dihapus**. Untuk kembali, ubah meta `_elementor_edit_mode` halaman menjadi `builder`
(atau buka halaman di Elementor lalu Simpan). Backup Bekasi sebelum perubahan: `backup/2026-10-23_9584_bekasi_elementor_sebelum.json`.

## Gambar

Sejak Cloudinary `v6gwkqrb` dinonaktifkan (23 Okt 2026), semua gambar halaman ini ada di Media WordPress
(`wp-content/uploads/2026/10/`): `foto-paket-*` (kartu paket), `hero-jamaah-kabah`, `perlengkapan-*-2026`,
`kolase-hotel-*` (slider hotel: gedung + kamar), `fasilitas-bus-1`. Sumber: Canva, Google Drive dan situs resmi hotel.
Lihat `tools/ganti_gambar.py` dan `tools/kolase_hotel.py`.

## Alat bantu

- `tools/screenshot.js`: screenshot desktop/HP lewat Chrome (`npm i puppeteer-core`, lalu `node tools/screenshot.js <url> <prefix> <lebar> <1=mobile>`).
- `tools/cek_update.py`: cocokkan respons update WordPress dengan file lokal.
