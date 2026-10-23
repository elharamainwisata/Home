# Catatan sesi 2026-10-23 · Halaman kantor cabang

Permintaan pemilik: desain ulang halaman kota (referensi ghufrantravel.com), live di bagian kantor cabang,
paket Syawal ikut dimasukkan, dirapikan, dan **info paket serta lokasi jangan berulang**.

## Yang dikerjakan
- 6 halaman kota (9584–9589) dipindah dari Elementor ke blok `wp:html` + synced pattern 9991–9996 dan 9999.
  `_elementor_edit_mode` dikosongkan; `_elementor_data` lama tetap ada untuk rollback.
- Pattern harga 9996 dibangun ulang dari kartu harga lama (20 paket, harga tidak diubah) + 5 paket **Syawal 2027**
  (sumber: halaman /umroh-syawal/, harga quad/triple/double). Markup lebih ringkas: 54 rb → 35 rb karakter.
- Struktur akhir tanpa pengulangan: kartu "keberangkatan terdekat", jadwal terdekat, cara daftar, FAQ, kotak rekening
  di legalitas, dan CTA penutup dihapus (duplikat pattern harga/ketentuan, bagian kantor, atau CTA footer situs).
- Perapian: judul bagian rata tengah semua, latar selang-seling, di HP kartu harga jadi geser horizontal,
  layanan 2 kolom. Tinggi halaman HP turun dari ±24.400 px ke ±15.700 px.
- Pattern uji (9989) dan draft uji (9990) dipindah ke Trash.

## Temuan teknis
- Konektor WordPress.com hanya bisa menulis `_elementor_data` sebagai satu string JSON besar (harus string, array ditolak).
  Untuk halaman Elementor ±150 KB ini terlalu berisiko; jalan aman = blok `wp:html` + synced pattern.
- Upload plugin PHP lewat konektor diblokir pengaman Claude Code (dianggap membuka eksekusi kode di situs live).
- Tema LandingPress membungkus konten di `.site-content .container` (lebar terbatas) → dilepas lewat CSS `:has()` di pattern 9999.
- Aturan `.ehc a{color}` mengalahkan warna link khusus; pakai selektor `.ehc .kelas`.
- `include_fields: ["id"]` di `pages.update` membuat respons kecil (tanpa meta Elementor 180 KB).

## Menunggu pemilik
- ~~Konfirmasi nomor WA Bandung~~: 0813-2212-344 (11 digit) sudah dikonfirmasi benar oleh pemilik.
- Foto khusus kartu Syawal (sementara memakai foto kartu paket yang ada).
- ~~Akses tulis repo GitHub~~: undangan diterima, repo `elharamainwisata/Home` sudah berisi file ini.

## Lanjutan: halaman paket Bronze (8869)
- Didesain ulang dengan pola yang sama: hero, angka singkat, 5 kartu Bronze (Des, Bronze Plus Des, Jan, Ramadhan, Syawal)
  diambil dari pattern 9996, lalu pattern layanan/ketentuan/fasilitas/testimoni, dan tautan paket lain + kantor terdekat.
  FAQ lama tidak dibawa karena semua isinya mengulang bagian lain. Schema TouristTrip per keberangkatan.
- Pattern 9999 diperbaiki: urutan latar halaman kota sebelumnya ada dua bagian berurutan berwarna sama.
- **Temuan penting:** Cloudinary `v6gwkqrb` membalas HTTP 401 `cloud_name v6gwkqrb is disabled` (23 Okt 2026, ±14:20 WIB).
  Semua gambar Cloudinary di situs tidak tampil sampai akun diaktifkan lagi atau gambar dipindah ke Media WordPress.

## Lanjutan: gambar pengganti Cloudinary (23 Okt 2026, sore)
- Semua gambar Cloudinary di 6 halaman kota + Bronze diganti gambar di Media WordPress (`wp-content/uploads/2026/10/`).
  Skrip penggantian: `tools/ganti_gambar.py`.
- **Kartu paket**: foto rombongan asli tanpa teks/harga (gaya ghufrantravel). Diambil dari salinan desain Canva "web"
  (DAHYz54LrZM, stiker & harga dihapus). Bronze = Ka'bah malam, Silver = Jabal Rahmah, Platinum = Ka'bah ihram,
  Premium = Masjid Nabawi, Silver 12 Hari/Gold = Masjid Quba.
- **Hero**: `hero-jamaah-kabah.jpg` (dari foto Platinum).
- **Perlengkapan**: desain Canva "Perlengkapan" hal. 1 (wanita) & 3 (pria).
- **Hotel**: kolase 1000x520 `kolase-hotel-*.jpg` (gedung + 2 foto kamar/lobi), atas permintaan pemilik
  ("ada gambar hotel dan gambar dalamnya"). Foto dari situs resmi: Anjum, Fairmont, Marwa Rotana (Al Marwa Rayhaan),
  Movenpick Hajar & Anwar Al Madinah. Sisanya dari halaman fasilitas hotel brosur Canva Januari/Desember/Ramadhan.
  Pembuat kolase: `tools/kolase_hotel.py`.
- **Belum**: galeri "Momen bersama jamaah" dari Google Drive. Folder DOKUMENTASI hanya berisi video, folder "media" berisi
  materi iklan, file DSC besar gagal diunduh lewat konektor. Perlu nama folder foto dokumentasi dari pemilik.
  Galeri saat ini tetap memakai 11 foto lama dari Media WordPress (masih tampil).

## Paket Desember 2026 habis (23 Okt 2026)
- Tab Desember dihapus dari pattern 9996 (tinggal Januari, Ramadhan, Syawal; Januari jadi tab awal). Judul: "Januari – Syawal 2027".
- Halaman Bronze: 2 kartu Desember dihapus (tinggal Januari, Ramadhan, Syawal) + schema TouristTrip ikut.
- Slider hotel (9995): Prestige & Peninsula Worth dihapus karena hanya dipakai paket Desember.
- priceRange schema 6 halaman kota: Rp 37.500.000 – Rp 71.000.000 (diganti per blok lewat page-sections.replace).
- Deskripsi SEO (Rank Math) 6 kota + judul/deskripsi Bronze diganti ke "Januari–Syawal 2027 mulai Rp 37,5 juta".
