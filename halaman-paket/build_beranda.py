"""Calon pengganti beranda (page 10088, /beranda-baru/, berkata sandi). Beranda asli (page 7840) TIDAK diubah
sampai pemilik bilang final. Urutan bagian terinspirasi ghufrantravel.com (pilihan pemilik), tetapi semua kalimat ditulis sendiri
dengan gaya Elharamain (pemilik minta kata-kata tidak sama dengan LP contoh).
Jadwal & harga diambil dari kartu Januari + Ramadhan (paket musim dingin) di pattern 9996.
Jalankan: python3 halaman-paket/build_beranda.py  → halaman-paket/halaman/beranda-baru.html"""
import json, re
from build_paket import HERE, SITE, SEMUA, PAGES, wa, blk, ref

WA_SVG = '<i class="ehb-wa"></i>'  # ikon WA lewat CSS mask, supaya isi halaman lebih ringan

UP = SITE + 'wp-content/uploads/'
BULAN = {'Jan': ('Januari', 1), 'Feb': ('Februari', 2), 'Mar': ('Maret', 3)}
rp = lambda n: 'Rp ' + f'{n:,}'.replace(',', '.')
harga = lambda c: int(re.sub(r'\D', '', re.search(r'<b>(Rp [^<]+)</b>', c).group(1)))
isi = lambda c, k: re.search(k + r'</i><span>([^<]+)</span>', c).group(1).replace('&amp;', '&')

# --- jadwal: pecah setiap kartu musim dingin jadi satu baris per tanggal berangkat ---
jadwal = []
for per, k, nama, c in SEMUA:
    if per not in ('Januari 2027', 'Ramadhan 2027'):
        continue
    tgl = isi(c, 'Berangkat')
    bln = re.search(r'(Jan|Feb|Mar) (\d{4})', tgl)
    for d in re.findall(r'\d+', tgl.split(bln.group(1))[0]):
        jadwal.append(dict(tgl=int(d), bln=bln.group(1), nama=nama, dur=isi(c, 'Durasi'), mk=isi(c, 'Maskapai'),
                           makkah=isi(c, 'Hotel Makkah'), madinah=isi(c, 'Hotel Madinah'), harga=harga(c)))
jadwal.sort(key=lambda j: (BULAN[j['bln']][1], j['tgl'], j['harga']))
pertama = jadwal[0]


def baris(j):
    bulan = BULAN[j['bln']][0]
    pesan = f"Assalamu'alaikum Elharamain Wisata, saya ingin tanya paket {j['nama']} keberangkatan {j['tgl']} {bulan} 2027."
    return f'''<div class="ehb-jr"><div class="ehb-dt"><b>{j['tgl']}</b><span>{j['bln'].upper()} 27</span></div>
      <div class="ehb-jx"><h3>Paket {j['nama']} · Makkah {j['makkah']} · Madinah {j['madinah']}</h3><p>{j['dur']} · {j['mk']}</p><p class="ehb-pr">mulai <b>{rp(j['harga'])}</b></p></div>
      <a class="ehb-btn ghost" href="{wa(pesan)}" target="_blank" rel="noopener">{WA_SVG} Tanya kursi</a></div>'''


# --- kelas paket: harga mulai = kartu termurah di halaman paket itu ---
KELAS = [('bronze', 'Harga terjangkau', 'Hotel Makkah bintang 5, cocok untuk umroh pertama.', 't1'),
         ('silver', 'Saudia Airlines', 'Anjum di Makkah dan Al-Aqeeq di Madinah, keduanya bintang 5.', 't2'),
         ('silver-12', '12 hari', 'Waktu ibadah lebih leluasa, tersedia kelas Silver dan Gold.', 't3'),
         ('platinum', 'Zamzam Tower', 'Menginap di Marwa Rotana atau Movenpick, selangkah ke Masjidil Haram.', 't4'),
         ('premium', 'Fairmont Makkah', 'Kenyamanan terbaik di Fairmont Makkah Clock Royal Tower.', 't5')]
halaman = {p['key']: p for p in PAGES}


def kelas(key, badge, desc, t):
    p = halaman[key]
    murah = min(harga(c) for per, k, n, c in SEMUA if p['pilih'](k, n))
    return f'''<div class="ehb-tier {t}"><div class="ehb-th"><span>{badge}</span><h3>Umroh {p['nama']}</h3><i>★★★★★</i></div>
      <div class="ehb-tb"><small>mulai</small><b>{rp(murah)}</b><small>per orang · kamar berempat</small><p>{desc}</p>
      <a class="ehb-btn pri" href="{SITE}{p['slug']}/">Lihat detail paket</a></div></div>'''


IC = {  # ikon garis sederhana (stroke)
    'tameng': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    'dok': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/>',
    'dompet': '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>',
    'orang': '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3 3-5 6-5s6 2 6 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 15c3 0 5 2 5 5"/>',
    'kalender': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    'tukar': '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
    'pesawat': '<path d="M10.5 3.5 13 10h5.5a2 2 0 0 1 0 4H13l-2.5 6.5H8.5L10 14H6l-1.5 2H3l1-4-1-4h1.5L6 10h4L8.5 3.5z"/>',
    'bulan': '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/>',
    'masjid': '<path d="M4 21h16M6 21v-7a6 6 0 0 1 12 0v7M12 8V3M10 21v-4h4v4"/>',
    'buku': '<path d="M4 5c3-1 6-1 8 1 2-2 5-2 8-1v14c-3-1-6-1-8 1-2-2-5-2-8-1z"/><path d="M12 6v14"/>',
    'hati': '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    'bintang': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    'peta': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
}
ikon = lambda n: f'<span class="ehb-ic"><svg viewBox="0 0 24 24">{IC[n]}</svg></span>'
kartu = lambda i, judul, teks, extra='': f'<div class="ehb-card">{ikon(i)}<h3>{judul}</h3><p>{teks}</p>{extra}</div>'

# hanya program yang ada di brosur PDF (pemilik: "paket yang ada di pdf saja")
LAYANAN = [('pesawat', 'Umroh Januari 2027', 'Bronze sampai Premium, keberangkatan 3 sampai 31 Januari 2027 bersama Saudia Airlines.', 'paket-umroh-musim-dingin/'),
           ('bulan', 'Umroh Ramadhan 2027', 'Bronze, Platinum, dan Premium, keberangkatan 8 sampai 21 Februari 2027.', 'paket-umroh-musim-dingin/'),
           ('masjid', "I'tikaf Ramadhan 17 Hari", "Sepuluh malam terakhir Ramadhan di Tanah Suci, keberangkatan 28 Februari 2027.", 'paket-umroh-silver/'),
           ('kalender', 'Umroh Syawal 2027', 'Lima pilihan paket setelah Idul Fitri, keberangkatan 8 sampai 22 Maret 2027.', 'umroh-syawal/')]

# Paket Haji Plus 1448 H (estimasi keberangkatan 2027), sumber: halaman https://elharamainwisata.com/haji/
HAJI = [('Silver', '', '12.000', '13.500', '15.000', '22–23 hari', 'Anjum ★5', 'Concorde ★4', 'Saudia / Qatar / Emirates'),
        ('Gold', '', '15.500', '17.000', '18.500', '22–23 hari', 'Marwa Rotana ★5', 'Al-Aqeeq ★5', 'Saudia / Qatar / Emirates'),
        ('Gold Arbain', 'Paling diminati', '17.000', '18.500', '20.000', '27–28 hari', 'Marwa Rotana ★5', 'Al-Aqeeq ★5', 'Saudia / Qatar / Emirates'),
        ('Platinum', '', '20.000', '22.000', '24.000', '22–23 hari', 'Fairmont ★5', 'Movenpick ★5', 'Saudia / Garuda Indonesia')]


def haji(nama, badge, quad, triple, double, durasi, makkah, madinah, maskapai):
    pesan = f"Assalamu'alaikum Elharamain Wisata, saya ingin tanya Paket Haji Plus {nama}."
    tag = f'<span class="ehb-badge">{badge}</span>' if badge else ''
    return f'''<div class="ehb-card ehb-hj">{tag}<h3>Haji Plus {nama}</h3><small>mulai</small><b>{quad} USD</b><small>kamar quad · triple {triple} · double {double} USD</small>
      <ul><li><span>Durasi</span>{durasi}</li><li><span>Hotel Makkah</span>{makkah}</li><li><span>Hotel Madinah</span>{madinah}</li><li><span>Maskapai</span>{maskapai}</li></ul>
      <a class="ehb-btn pri" href="{wa(pesan)}" target="_blank" rel="noopener">{WA_SVG} Tanya paket</a></div>'''


USTADZ = [('12-5', 'Ust. Ahmad Shobirin, Lc., MA'), ('11-5', 'Ust. Dr. Muhammad Tahir, Lc., MA'),
          ('10-9', 'Ust. Didi Wibawa, Lc., MA'), ('9-9', 'Ust. Furqon Abdurrohman, Lc., MA'),
          ('8-8', 'Ust. Ahmad Husain, Lc., M.Pd'), ('7-5', 'Ust. Idrus Abidin, Lc., MA'),
          ('13-5', 'Ust. Zulfahmi Yusuf, S.Pd.I'), ('6-5', 'Ust. Ade Abu Yusuf, Lc.')]

FOTO = [('umroh-syawal-gold-12-hari', "Pelataran Ka'bah · Maret 2026", 'big'), ('umroh-syawal-silver', 'Payung Masjid Nabawi · Maret 2026', ''),
        ('umroh-syawal-silver-12-hari', 'Masjid Quba · Maret 2026', ''), ('umroh-syawal-bronze', "Ka'bah malam hari · Maret 2026", ''),
        ('umroh-syawal-platinum', "Keluarga jamaah di depan Ka'bah · Maret 2026", '')]

ALUR = [('chat', 'Konsultasi', 'Hubungi tim kami lewat WhatsApp atau kunjungi kantor Elharamain Wisata terdekat.'),
        ('kalender', 'Booking seat', 'Tentukan paket dan tanggal, bayar DP Rp 6.000.000, lalu serahkan dokumen ke admin.'),
        ('buku', 'Manasik', 'Ikuti manasik di hotel berbintang sekaligus terima perlengkapan umroh.'),
        ('pesawat', 'Berangkat', 'Rombongan berkumpul di VIP Lounge Umroh Soekarno-Hatta.'),
        ('masjid', 'Beribadah', 'Umroh hingga 3 kali dengan Audio Hajj, dilengkapi tahajjud bersama dan kajian.'),
        ('hati', 'Kembali ke tanah air', 'Jamaah pulang membawa zamzam 5 liter, album foto, sertifikat, dan oleh-oleh.')]


hero = f'''<div class="ehc ehb"><section class="ehb-hero">
  <div class="ehc-wrap ehb-hero-in">
    <div class="ehb-hero-tx">
      <span class="ehb-pill">PT Dhiyaa El Haramain El Mubarakah · PPIU &amp; PIHK resmi</span>
      <h1>Umroh dan Haji Plus yang <em>Nyaman dan Berkesan</em></h1>
      <p>Hotel bintang 5, penerbangan langsung, kereta cepat Haramain, dan bimbingan ibadah sesuai sunnah bersama asatidz lulusan Timur Tengah. Elharamain Wisata hadir di Bekasi, Jakarta, Depok, Tangerang, Bogor, dan Bandung.</p>
      <div class="ehc-ctas">
        <a class="ehb-btn wa" href="{wa("Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi paket umroh.")}" target="_blank" rel="noopener">{WA_SVG} Konsultasi Gratis</a>
        <a class="ehb-btn glass" href="#jadwal">Cek jadwal keberangkatan</a>
      </div>
    </div>
    <div class="ehb-next">
      <small>Berangkat paling dekat</small>
      <b>{pertama['tgl']} {BULAN[pertama['bln']][0]} 2027</b>
      <span>{pertama['dur']} · {pertama['mk']} · Paket {pertama['nama']}</span>
      <p>mulai <strong>{rp(pertama['harga'])}</strong></p>
      <span>per orang · kamar berempat</span>
      <a class="ehb-btn wa" href="{wa(f"Assalamu'alaikum Elharamain Wisata, saya ingin daftar paket {pertama['nama']} keberangkatan {pertama['tgl']} {BULAN[pertama['bln']][0]} 2027.")}" target="_blank" rel="noopener">Daftar keberangkatan ini →</a>
    </div>
  </div>
  <div class="ehc-wrap"><div class="ehb-stat">
    <div><b>6.800+</b><span>ulasan Google bintang 5</span></div>
    <div><b>6 kantor</b><span>Bekasi, Jakarta, Depok, Tangerang, Bogor, Bandung</span></div>
    <div><b>Akreditasi A</b><span>Komite Akreditasi Nasional</span></div>
    <div><b>IATA</b><span>Kode 15333220</span></div>
  </div></div>
</section>
<section class="ehb-sec ehb-pt0 ehb-up">
  <div class="ehc-wrap"><div class="ehb-g4">
    {kartu('tameng', 'Berizin resmi Kemenag', 'Penyelenggara umroh (PPIU No. 63/2020) dan haji khusus (PIHK No. 846/2020).')}
    {kartu('dok', 'Rincian harga lengkap', 'Harga kamar quad, triple, dan double tercantum di tiap paket beserta fasilitasnya.')}
    {kartu('dompet', 'Booking seat Rp 6 juta', 'Cukup DP Rp 6.000.000 per jamaah, sisanya dilunasi H-35 sebelum keberangkatan.')}
    {kartu('orang', 'Pembimbing sepanjang perjalanan', 'Asatidz dan mutawwif mendampingi jamaah sejak manasik hingga kembali ke tanah air.')}
  </div></div>
</section>
<section class="ehb-sec ehb-dark" id="jadwal">
  <div class="ehc-wrap">
    <span class="ehb-kick">Jadwal 2027</span>
    <h2>Pilih tanggal keberangkatan Anda</h2>
    <p class="ehb-lead">Harga per jamaah untuk kamar berempat, sesuai brosur resmi Elharamain Wisata.</p>
    {"".join(baris(j) for j in jadwal[:6])}
    <a class="ehb-btn ghost" href="{SITE}paket-umroh-musim-dingin/" style="margin-top:8px">Lihat seluruh jadwal ({len(jadwal)} tanggal)</a>
  </div>
</section>
<section class="ehb-sec" id="legalitas">
  <div class="ehc-wrap">
    <span class="ehb-kick">Legalitas</span>
    <h2>Legalitas Elharamain Wisata</h2>
    <p class="ehb-lead">Elharamain Wisata adalah penyelenggara ibadah umroh dan haji khusus yang terdaftar di Kementerian Agama RI.</p>
    <div class="ehb-legal">
      <div><small>Badan usaha</small><b>PT Dhiyaa El Haramain El Mubarakah</b></div>
      <div><small>Izin PPIU (umroh)</small><b>SK Kemenag No. 63 Tahun 2020</b></div>
      <div><small>Izin PIHK (haji khusus)</small><b>SK Kemenag No. 846 Tahun 2020</b></div>
      <div><small>Keanggotaan</small><b>HIMPUH No. 131/2017 · IATA 15333220</b></div>
      <div><small>Akreditasi</small><b>A, Komite Akreditasi Nasional (KAN)</b></div>
      <div><small>Kantor</small><b>Bekasi (pusat) · Jakarta · Depok · Tangerang · Bogor · Bandung</b></div>
    </div>
    <p class="ehb-note">Pembayaran hanya sah ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah: Bank Mandiri 156.001.150.115.4 atau Bank BSI 710.857.755.4.</p>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="kelas">
  <div class="ehc-wrap">
    <span class="ehb-kick">Paket umroh</span>
    <h2>Pilih kelas paket sesuai kebutuhan</h2>
    <p class="ehb-lead">Setiap kelas sudah termasuk tiket, visa, asuransi, hotel bintang 5, makan 3x sehari, manasik, pembimbing, dan mutawwif. Bedanya ada pada hotel, durasi, dan maskapai.</p>
    <div class="ehb-tiers">{"".join(kelas(*k) for k in KELAS)}</div>
  </div>
</section></div>'''

tengah = f'''<div class="ehc ehb"><section class="ehb-sec ehb-dark">
  <div class="ehc-wrap">
    <span class="ehb-kick">Kenapa Elharamain Wisata</span>
    <h2>Kenapa memilih Elharamain Wisata?</h2>
    <div class="ehb-g3">
      {kartu('tameng', 'Terdaftar dan terakreditasi', 'Izin PPIU dan PIHK dari Kemenag, anggota HIMPUH dan IATA, serta terakreditasi A oleh KAN.')}
      {kartu('bintang', 'Fasilitas eksklusif', 'Hotel bintang 5, VIP Lounge Umroh, kereta cepat Haramain, perlengkapan eksklusif, hingga kuliner khas Arab Saudi.')}
      {kartu('dompet', 'Satu nama rekening', 'Setoran hanya diterima di Bank Mandiri dan BSI atas nama PT Dhiyaa El Haramain El Mubarakah.')}
      {kartu('kalender', 'Tahapan pembayaran ringan', 'Mulai dengan DP Rp 6.000.000, pelunasan paling lambat 35 hari sebelum keberangkatan.')}
      {kartu('tukar', 'Bisa reschedule', 'Jadwal atau program dapat dipindah bila dikabarkan paling lambat 40 hari sebelum berangkat.')}
      {kartu('chat', 'Konsultasi gratis', 'Tim kami siap menjawab lewat WhatsApp maupun di 6 kantor Elharamain Wisata.')}
    </div>
  </div>
</section>
<section class="ehb-sec" id="dokumentasi">
  <div class="ehc-wrap">
    <span class="ehb-kick">Dokumentasi</span>
    <h2>Dokumentasi jamaah Elharamain Wisata</h2>
    <p class="ehb-lead">Rombongan umroh Syawal Elharamain Wisata di Makkah dan Madinah, Maret 2026.</p>
    <div class="ehb-mos">{"".join(f'<figure class="{k}"><img loading="lazy" src="{UP}2026/10/{f}-1024x640.jpg" alt="Jamaah Elharamain Wisata, {t}"><figcaption>{t}</figcaption></figure>' for f, t, k in FOTO)}</div>
  </div>
</section>
<section class="ehb-sec ehb-soft" id="layanan">
  <div class="ehc-wrap">
    <span class="ehb-kick">Program 2027</span>
    <h2>Program umroh &amp; Haji Plus Elharamain Wisata</h2>
    <div class="ehb-tabs"><input type="radio" name="ehb-prog" id="ehp-u" checked><input type="radio" name="ehb-prog" id="ehp-h">
    <div class="tl"><label for="ehp-u">Paket Umroh</label><label for="ehp-h">Paket Haji Plus</label></div>
    <div class="ehb-g4 pn pu">{"".join(kartu(i, j, t, f'<a class="ehb-more" href="{SITE}{u}">Selengkapnya →</a>') for i, j, t, u in LAYANAN)}</div>
    <div class="pn ph"><div class="ehb-g4">{"".join(haji(*h) for h in HAJI)}</div>
    <p class="ehb-note">Setoran awal nomor porsi 4.000 USD untuk semua paket. Biaya adalah estimasi keberangkatan 2027 dan diinformasikan kembali 1 tahun sebelum berangkat (estimasi kenaikan 4–5% per tahun). <a href="{SITE}haji/">Lihat detail Haji Plus →</a></p></div></div>
  </div>
</section>
<section class="ehb-sec" id="pembimbing">
  <div class="ehc-wrap">
    <span class="ehb-kick">Lulusan terbaik Timur Tengah</span>
    <h2>Pembimbing ibadah umroh &amp; haji</h2>
    <p class="ehb-lead">Ibadah dibimbing langsung oleh asatidz yang mendampingi jamaah dari manasik sampai pulang ke tanah air.</p>
    <div class="ehb-ust">{"".join(f'<figure><img loading="lazy" src="{UP}2025/03/{f}.jpg" alt="{n}, pembimbing ibadah Elharamain Wisata"><figcaption>{n}</figcaption></figure>' for f, n in USTADZ)}</div>
  </div>
</section>
<section class="ehb-sec ehb-dark" id="alur">
  <div class="ehc-wrap">
    <span class="ehb-kick">Cara mendaftar</span>
    <h2>Langkah umroh bersama Elharamain Wisata</h2>
    <div class="ehb-g3">{"".join(f'<div class="ehb-card"><span class="ehb-no">0{n}</span>{ikon(i)}<h3>{j}</h3><p>{t}</p></div>' for n, (i, j, t) in enumerate(ALUR, 1))}</div>
  </div>
</section></div>
<style>
.ehb-tabs>input{{position:absolute;opacity:0;pointer-events:none}}
.ehb-tabs .tl{{display:flex;gap:8px;flex-wrap:wrap;margin:24px 0}}
.ehb-tabs .tl label{{border:1px solid var(--ln);background:#fff;color:var(--mu);border-radius:999px;padding:10px 20px;font:700 14px Poppins,sans-serif;cursor:pointer}}
#ehp-u:checked~.tl label[for=ehp-u],#ehp-h:checked~.tl label[for=ehp-h]{{background:var(--bl);border-color:var(--bl);color:#fff}}
.ehb-tabs .pn{{display:none}}
#ehp-u:checked~.pu,#ehp-h:checked~.ph{{display:grid}}
#ehp-h:checked~.ph{{display:block}}
.ehb-hj{{position:relative}}
.ehb-hj b{{display:block;font:700 24px Poppins,sans-serif;color:var(--nv)}}
.ehb-hj small{{font-size:12px;color:var(--mu)}}
.ehb-hj ul{{list-style:none;margin:14px 0 16px;padding:0;display:grid;gap:6px;font-size:13.5px}}
.ehb-hj li{{display:flex;justify-content:space-between;gap:10px;color:var(--nv)}}
.ehb-hj li span{{color:var(--mu)}}
.ehb-hj .ehb-btn{{margin-top:auto;font-size:14px;padding:11px}}
.ehb-badge{{position:absolute;top:-10px;right:16px;background:var(--gd);color:var(--nv);font:700 11px Poppins,sans-serif;padding:4px 10px;border-radius:999px}}
</style>'''

# FAQ sengaja tidak ada di home (permintaan pemilik)
akhir = f'''<style>
.ehb{{--nv:#10213d;--bl:#004AAD;--bl2:#1684CF;--gd:#DBC033;--ln:#e3e9f3;--mu:#55627a;--soft:#f4f7fc}}
.ehb .ehb-sec{{padding:72px 0;background:#fff}}
.ehb .ehb-soft{{background:var(--soft)}}
.ehb .ehb-dark{{background:var(--bl);color:#fff}}
.ehb .ehb-pt0{{padding-top:0}}
.ehb .ehb-up .ehb-g4{{margin-top:-28px;position:relative}}
.ehb .ehb-up .ehb-card{{box-shadow:0 10px 28px rgba(16,33,61,.08)}}
.ehb h2{{font:700 clamp(26px,3.4vw,38px)/1.18 Poppins,sans-serif;margin:0 0 10px;color:var(--nv);letter-spacing:-.01em}}
.ehb .ehb-dark h2,.ehb .ehb-dark h3{{color:#fff}}
.ehb .ehb-kick{{display:block;font:700 12px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--bl);margin-bottom:8px}}
.ehb .ehb-dark .ehb-kick{{color:var(--gd)}}
.ehb .ehb-lead{{color:var(--mu);margin:0 0 28px;max-width:680px}}
.ehb .ehb-dark .ehb-lead,.ehb .ehb-dark p{{color:rgba(255,255,255,.85)}}
.ehb .ehb-note{{font-size:13px;color:var(--mu);margin:16px 0 0;max-width:760px}}
.ehb-btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:13px 20px;border-radius:12px;font:600 15px Poppins,sans-serif;text-decoration:none!important;border:1px solid transparent;transition:transform .15s}}
.ehb-btn:hover{{transform:translateY(-1px)}}
.ehb-wa{{width:18px;height:18px;flex:none;background:currentColor;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z'/%3E%3C/svg%3E") center/contain no-repeat}}
.ehb-btn.wa{{background:#25D366;color:#fff!important}}
.ehb-btn.pri{{background:var(--bl);color:#fff!important}}
.ehb-btn.glass{{background:rgba(255,255,255,.1);color:#fff!important;border-color:rgba(255,255,255,.45)}}
.ehb-btn.ghost{{background:#fff;color:var(--bl)!important;border-color:#fff}}
.ehb-hero{{position:relative;color:#fff;padding:84px 0 40px;background:linear-gradient(100deg,rgba(16,33,61,.96) 0%,rgba(16,33,61,.85) 45%,rgba(0,74,173,.45) 100%),url({UP}2026/10/hero-jamaah-kabah.jpg) center/cover;}}
.ehb-hero-in{{display:flex;gap:40px;align-items:flex-end;justify-content:space-between}}
.ehb-hero-tx{{max-width:680px}}
.ehb-pill{{display:inline-block;border:1px solid rgba(255,255,255,.45);border-radius:999px;padding:7px 14px;font:700 11px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-bottom:20px}}
.ehb-hero h1{{font:700 clamp(36px,5.4vw,62px)/1.06 Poppins,sans-serif;color:#fff;margin:0 0 18px;letter-spacing:-.02em}}
.ehb-hero h1 em{{font-style:normal;color:var(--gd)}}
.ehb-hero p{{color:rgba(255,255,255,.85);font-size:17px;margin:0 0 26px}}
.ehb-next{{flex:none;width:300px;background:rgba(0,74,173,.88);border:1px solid rgba(255,255,255,.2);border-radius:18px;padding:22px;backdrop-filter:blur(6px)}}
.ehb-next small{{display:block;font:700 11px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--gd)}}
.ehb-next b{{display:block;font:700 26px Poppins,sans-serif;margin:6px 0 2px}}
.ehb-next span{{display:block;font-size:13px;color:rgba(255,255,255,.7)}}
.ehb-next p{{margin:14px 0 0;font-size:14px}}
.ehb-next strong{{font:700 26px Poppins,sans-serif;color:var(--gd)}}
.ehb-next .ehb-btn{{width:100%;margin-top:16px}}
.ehb-stat{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:44px;border:1px solid rgba(255,255,255,.22);border-radius:16px;overflow:hidden}}
.ehb-stat div{{padding:16px 20px;border-right:1px solid rgba(255,255,255,.22)}}
.ehb-stat div:last-child{{border-right:0}}
.ehb-stat b{{display:block;font:700 26px Poppins,sans-serif}}
.ehb-stat span{{font-size:13px;color:rgba(255,255,255,.75)}}
.ehb-g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.ehb-g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}}
.ehb-card{{background:#fff;border:1px solid var(--ln);border-radius:16px;padding:22px;display:flex;flex-direction:column}}
.ehb-dark .ehb-card{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.2)}}
.ehb-card h3{{font:700 17px/1.35 Poppins,sans-serif;margin:0 0 6px}}
.ehb-card h3{{color:var(--nv)}}
.ehb-card p{{margin:0;font-size:14.5px;color:var(--mu)}}
.ehb-ic{{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;background:#e8eef9;color:var(--bl);margin-bottom:14px}}
.ehb-dark .ehb-ic{{background:rgba(219,192,51,.2);color:var(--gd)}}
.ehb-ic svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}}
.ehb-no{{font:700 13px Poppins,sans-serif;color:var(--gd);margin-bottom:8px}}
.ehb-more{{margin-top:auto;padding-top:14px;font:600 14px Poppins,sans-serif;color:var(--bl)!important;text-decoration:none!important}}
.ehb-jr{{display:flex;align-items:center;gap:20px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:16px;padding:16px 18px;margin-bottom:10px}}
.ehb-dt{{flex:none;width:66px;height:66px;border-radius:12px;background:var(--gd);color:var(--nv);display:grid;place-items:center;align-content:center;line-height:1}}
.ehb-dt b{{font:800 26px Poppins,sans-serif}}
.ehb-dt span{{font:700 10.5px Poppins,sans-serif;letter-spacing:.08em;margin-top:4px}}
.ehb-jx{{flex:1;min-width:0}}
.ehb-jx h3{{font:600 15.5px/1.4 Poppins,sans-serif;margin:0 0 2px;color:#fff}}
.ehb-jx p{{margin:0;font-size:13px}}
.ehb-pr b{{font:700 19px Poppins,sans-serif;color:var(--gd)}}
.ehb-jr .ehb-btn{{flex:none;font-size:14px;padding:10px 14px}}
.ehb-legal{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.ehb-legal div{{border:1px solid var(--ln);border-radius:12px;padding:12px 14px;background:var(--soft)}}
.ehb-legal small{{display:block;font-size:12px;color:var(--mu)}}
.ehb-legal b{{font:600 15px Poppins,sans-serif;color:var(--nv)}}
.ehb-tiers{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}
.ehb-tier{{background:#fff;border:1px solid var(--ln);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.ehb-th{{padding:16px;color:#fff}}
.ehb-th span{{display:inline-block;background:rgba(255,255,255,.2);border-radius:999px;padding:3px 10px;font:700 10.5px Poppins,sans-serif;letter-spacing:.05em;text-transform:uppercase}}
.ehb-th h3{{font:700 19px/1.25 Poppins,sans-serif;margin:10px 0 2px;color:#fff}}
.ehb-th i{{font-style:normal;font-size:12px;letter-spacing:2px;color:#ffe48a}}
.t1 .ehb-th{{background:linear-gradient(135deg,#7a4a22,#b98150)}}.t2 .ehb-th{{background:linear-gradient(135deg,#4f5d70,#95a3b5)}}
.t3 .ehb-th{{background:linear-gradient(135deg,#8c6812,#d0a534)}}.t4 .ehb-th{{background:linear-gradient(135deg,#004AAD,#1684CF)}}
.t5 .ehb-th{{background:linear-gradient(135deg,#8e1b1b,#c0504d)}}
.ehb-tb{{padding:16px;display:flex;flex-direction:column;flex:1}}
.ehb-tb small{{font-size:12px;color:var(--mu)}}
.ehb-tb b{{font:700 22px Poppins,sans-serif;color:var(--nv);white-space:nowrap}}
.ehb-tb p{{font-size:13.5px;color:var(--mu);margin:10px 0 16px}}
.ehb-tb .ehb-btn{{margin-top:auto;font-size:14px;padding:11px}}
.ehb-mos{{display:grid;grid-template-columns:2fr 1fr 1fr;grid-auto-rows:220px;gap:10px}}
.ehb-mos figure{{position:relative;margin:0;border-radius:16px;overflow:hidden}}
.ehb-mos .big{{grid-row:span 2}}
.ehb-mos img{{width:100%;height:100%;object-fit:cover;display:block}}
.ehb-mos figcaption{{position:absolute;left:0;right:0;bottom:0;padding:24px 12px 10px;font-size:12.5px;color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.6))}}
.ehb-ust{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.ehb-ust figure{{margin:0;background:#fff;border:1px solid var(--ln);border-radius:14px;overflow:hidden;text-align:center}}
.ehb-ust img{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}}
.ehb-ust figcaption{{padding:12px 10px;font:600 14px Poppins,sans-serif;color:var(--nv)}}
@media (max-width:1060px){{.ehb-tiers{{grid-template-columns:repeat(3,1fr)}}.ehb-g4{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:900px){{.ehb-hero-in{{flex-direction:column;align-items:stretch}}.ehb-next{{width:auto}}.ehb-stat{{grid-template-columns:repeat(2,1fr)}}.ehb-stat div:nth-child(2){{border-right:0}}.ehb-stat div:nth-child(-n+2){{border-bottom:1px solid rgba(255,255,255,.22)}}.ehb-g3,.ehb-legal{{grid-template-columns:1fr 1fr}}.ehb-ust{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:640px){{.ehb .ehb-sec{{padding:52px 0}}.ehb-hero{{padding:48px 0 32px}}.ehb-g4,.ehb-g3,.ehb-legal,.ehb-tiers{{grid-template-columns:1fr}}.ehb-jr{{flex-wrap:wrap}}.ehb-jr .ehb-btn{{width:100%}}.ehb-mos{{grid-template-columns:1fr 1fr;grid-auto-rows:140px}}.ehb-mos .big{{grid-column:span 2;grid-row:span 1;height:220px}}.ehb-hero .ehc-ctas .ehb-btn{{width:100%}}}}
</style>'''

assert '&&' not in hero + tengah + akhir
page = '\n\n'.join([ref('gaya'), ref('lebar'), ref('paket'), blk(hero), blk(tengah), ref('testimoni'), blk(akhir)])
open(HERE + 'halaman/beranda-baru.html', 'w').write(page)
print('beranda-baru', len(page), 'jadwal', len(jadwal), 'pertama', pertama['tgl'], pertama['bln'], pertama['nama'])
