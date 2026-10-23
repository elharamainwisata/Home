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
