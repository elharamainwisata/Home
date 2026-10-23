"""Calon pengganti beranda (page 10088, /beranda-baru/, berkata sandi). Beranda asli (page 7840) TIDAK diubah
sampai pemilik bilang final. Struktur mengikuti ghufrantravel.com (pilihan pemilik): jadwal terdekat, legalitas,
kelas paket, alasan percaya, dokumentasi, layanan lain, alur, testimoni, FAQ.
Jadwal & harga diambil dari kartu Januari + Ramadhan (paket musim dingin) di pattern 9996.
Jalankan: python3 halaman-paket/build_beranda.py  → halaman-paket/halaman/beranda-baru.html"""
import json, re
from build_paket import HERE, SITE, SEMUA, PAGES, wa, blk, ref

WA_SVG = '<i class="ehh-wa"></i>'  # ikon WA lewat CSS mask, supaya isi halaman lebih ringan

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
    return f'''<div class="ehh-jr"><div class="ehh-dt"><b>{j['tgl']}</b><span>{j['bln'].upper()} 27</span></div>
      <div class="ehh-jx"><h3>Paket {j['nama']} · Makkah {j['makkah']} · Madinah {j['madinah']}</h3><p>{j['dur']} · {j['mk']}</p><p class="ehh-pr">mulai <b>{rp(j['harga'])}</b></p></div>
      <a class="ehh-btn ghost" href="{wa(pesan)}" target="_blank" rel="noopener">{WA_SVG} Tanya tanggal ini</a></div>'''


# --- kelas paket: harga mulai = kartu termurah di halaman paket itu ---
KELAS = [('bronze', 'Paling hemat', 'Hotel bintang 5 dengan pendampingan yang sama lengkap.', 't1'),
         ('silver', 'Direct Saudia', 'Hotel Anjum dekat Masjidil Haram, Al-Aqeeq di Madinah.', 't2'),
         ('silver-12', 'Lebih lama', 'Silver & Gold 12 hari, ibadah tanpa terburu-buru.', 't3'),
         ('platinum', 'Zamzam Tower', 'Marwa Rotana / Movenpick tepat di depan Masjidil Haram.', 't4'),
         ('premium', 'Kelas tertinggi', 'Fairmont Makkah Clock Royal Tower bintang 5.', 't5')]
halaman = {p['key']: p for p in PAGES}


def kelas(key, badge, desc, t):
    p = halaman[key]
    murah = min(harga(c) for per, k, n, c in SEMUA if p['pilih'](k, n))
    return f'''<div class="ehh-tier {t}"><div class="ehh-th"><span>{badge}</span><h3>Umroh {p['nama']}</h3><i>★★★★★</i></div>
      <div class="ehh-tb"><small>mulai</small><b>{rp(murah)}</b><small>per orang · kamar berempat</small><p>{desc}</p>
      <a class="ehh-btn pri" href="{SITE}{p['slug']}/">Lihat jadwal &amp; hotel</a></div></div>'''


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
    'peta': '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/>',
}
ikon = lambda n: f'<span class="ehh-ic"><svg viewBox="0 0 24 24">{IC[n]}</svg></span>'
kartu = lambda i, judul, teks, extra='': f'<div class="ehh-card">{ikon(i)}<h3>{judul}</h3><p>{teks}</p>{extra}</div>'

LAYANAN = [('pesawat', 'Umroh Musim Dingin', 'Keberangkatan Januari dan Ramadhan 2027, dari Bronze sampai Premium.', 'paket-umroh-musim-dingin/'),
           ('bulan', "Umroh Ramadhan & I'tikaf", "Umroh di bulan Ramadhan, termasuk I'tikaf 17 hari di sepuluh malam terakhir.", 'paket-umroh-silver/'),
           ('kalender', 'Umroh Syawal', 'Berangkat Maret 2027 setelah Lebaran, dengan Riyadh Air, Saudia, atau Garuda.', 'umroh-syawal/'),
           ('peta', 'Umroh Plus Turki', 'Umroh digabung perjalanan wisata ke Turki.', 'umroh-plus-turki/'),
           ('peta', 'Umroh Plus Dubai', 'Umroh digabung perjalanan wisata ke Dubai.', 'umroh-plus-dubai/'),
           ('peta', 'Umroh Plus Mesir', 'Umroh digabung perjalanan wisata ke Mesir.', 'umroh-plus-mesir/'),
           ('peta', 'Umroh Plus Aqsa', 'Umroh plus kunjungan ke Masjidil Aqsa.', 'umroh-plus-aqsa/'),
           ('masjid', 'Haji Plus', 'Haji khusus resmi melalui PIHK Elharamain (SK Kemenag No. 846/2020).', 'haji/')]

USTADZ = [('12-5', 'Ust. Ahmad Shobirin, Lc., MA'), ('11-5', 'Ust. Dr. Muhammad Tahir, Lc., MA'),
          ('10-9', 'Ust. Didi Wibawa, Lc., MA'), ('9-9', 'Ust. Furqon Abdurrohman, Lc., MA'),
          ('8-8', 'Ust. Ahmad Husain, Lc., M.Pd'), ('7-5', 'Ust. Idrus Abidin, Lc., MA'),
          ('13-5', 'Ust. Zulfahmi Yusuf, S.Pd.I'), ('6-5', 'Ust. Ade Abu Yusuf, Lc.')]

FOTO = [('umroh-syawal-gold-12-hari', "Pelataran Ka'bah · Maret 2026", 'big'), ('umroh-syawal-silver', 'Payung Masjid Nabawi · Maret 2026', ''),
        ('umroh-syawal-silver-12-hari', 'Masjid Quba · Maret 2026', ''), ('umroh-syawal-bronze', "Ka'bah malam hari · Maret 2026", ''),
        ('umroh-syawal-platinum', "Keluarga jamaah di depan Ka'bah · Maret 2026", '')]

ALUR = [('chat', 'Konsultasi', 'Ceritakan rencana Anda lewat WhatsApp atau datang ke kantor terdekat.'),
        ('kalender', 'Amankan kursi', 'Pilih paket dan tanggal, DP Rp 6.000.000 per orang, lalu lengkapi dokumen bersama tim admin.'),
        ('buku', 'Manasik', 'Manasik di hotel berbintang dan pembagian perlengkapan sebelum berangkat.'),
        ('pesawat', 'Berangkat', 'Berkumpul di VIP Lounge Umroh Soekarno-Hatta bersama pembimbing.'),
        ('masjid', 'Beribadah', 'Umroh hingga 3x dengan Audio Hajj, tahajjud bersama, dan kajian di Tanah Suci.'),
        ('hati', 'Pulang', 'Air zamzam 5 liter, album foto, sertifikat umroh, dan oleh-oleh.')]

FAQ = [('Apakah Elharamain Wisata resmi?', 'Ya. PT Dhiyaa El Haramain El Mubarakah memiliki izin PPIU SK Kemenag No. 63 Tahun 2020 dan PIHK No. 846 Tahun 2020, anggota HIMPUH dan IATA, serta terakreditasi A oleh KAN.'),
       ('Apa saja yang sudah termasuk dalam harga paket?', 'Tiket pesawat PP, visa dan asuransi, hotel bintang 5 sesuai paket dengan makan 3x sehari, perlengkapan umroh, manasik, VIP Lounge, bus, pembimbing dan mutawwif, umroh hingga 3x, city tour Thaif, bagasi 35 kg, air zamzam 5 liter, album foto, dan sertifikat.'),
       ('Apa yang belum termasuk?', 'Pembuatan paspor, suntik meningitis dan polio, keperluan pribadi, kelebihan bagasi, serta penyesuaian biaya bila ada kebijakan baru dari kedua negara.'),
       ('Berapa DP dan kapan pelunasan?', 'DP Rp 6.000.000 per jamaah untuk booking kursi. Pelunasan paling lambat 35 hari sebelum keberangkatan, hanya ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah.'),
       ('Harga yang tertulis untuk kamar apa?', 'Harga mulai adalah kamar berempat (quad). Harga kamar bertiga dan berdua tertulis di setiap paket.')]

hero = f'''<div class="ehc ehh"><section class="ehh-hero">
  <div class="ehc-wrap ehh-hero-in">
    <div class="ehh-hero-tx">
      <span class="ehh-pill">Travel umroh &amp; haji resmi · PPIU Kemenag</span>
      <h1>Umroh yang <em>nyaman dan berkesan</em>, dari manasik sampai pulang.</h1>
      <p>Elharamain Wisata menemani setiap langkah ibadah Anda: manasik sebelum berangkat, pembimbing lulusan Timur Tengah yang mendampingi di Tanah Suci, dan harga yang ditulis terbuka sejak awal.</p>
      <div class="ehc-ctas">
        <a class="ehh-btn wa" href="{wa("Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi paket umroh.")}" target="_blank" rel="noopener">{WA_SVG} Konsultasi via WhatsApp</a>
        <a class="ehh-btn glass" href="#jadwal">Lihat jadwal</a>
      </div>
    </div>
    <div class="ehh-next">
      <small>Keberangkatan terdekat</small>
      <b>{pertama['tgl']} {BULAN[pertama['bln']][0]} 2027</b>
      <span>{pertama['dur']} · {pertama['mk']} · Paket {pertama['nama']}</span>
      <p>mulai <strong>{rp(pertama['harga'])}</strong></p>
      <span>per orang · kamar berempat</span>
      <a class="ehh-btn wa" href="{wa(f"Assalamu'alaikum Elharamain Wisata, saya ingin daftar paket {pertama['nama']} keberangkatan {pertama['tgl']} {BULAN[pertama['bln']][0]} 2027.")}" target="_blank" rel="noopener">Pilih tanggal ini →</a>
    </div>
  </div>
  <div class="ehc-wrap"><div class="ehh-stat">
    <div><b>6.800+</b><span>ulasan Google bintang 5</span></div>
    <div><b>6 kantor</b><span>Bekasi, Jakarta, Depok, Tangerang, Bogor, Bandung</span></div>
    <div><b>Akreditasi A</b><span>Komite Akreditasi Nasional</span></div>
    <div><b>IATA</b><span>Kode 15333220</span></div>
  </div></div>
</section>
<section class="ehh-sec ehh-pt0 ehh-up">
  <div class="ehc-wrap"><div class="ehh-g4">
    {kartu('tameng', 'Izin resmi, bisa dicek', 'Izin PPIU SK Kemenag No. 63/2020 dan PIHK No. 846/2020 atas nama PT Dhiyaa El Haramain El Mubarakah.')}
    {kartu('dok', 'Harga ditulis terbuka', 'Harga kamar berempat, bertiga, dan berdua tertulis di setiap paket, lengkap dengan yang termasuk dan belum.')}
    {kartu('dompet', 'DP Rp 6.000.000/orang', 'Kunci kursi dengan DP, pelunasan paling lambat 35 hari sebelum berangkat.')}
    {kartu('orang', 'Didampingi penuh', 'Manasik, pembimbing ibadah, dan mutawwif menemani dari berangkat sampai pulang.')}
  </div></div>
</section>
<section class="ehh-sec ehh-dark" id="jadwal">
  <div class="ehc-wrap">
    <span class="ehh-kick">Keberangkatan terdekat</span>
    <h2>Jadwal umroh yang bisa Anda pilih</h2>
    <p class="ehh-lead">Langsung dari daftar harga resmi kami. Harga per orang, kamar berempat.</p>
    {"".join(baris(j) for j in jadwal[:6])}
    <a class="ehh-btn ghost" href="{SITE}paket-umroh-musim-dingin/" style="margin-top:8px">Semua jadwal keberangkatan ({len(jadwal)} tanggal)</a>
  </div>
</section>
<section class="ehh-sec" id="legalitas">
  <div class="ehc-wrap">
    <span class="ehh-kick">Legalitas</span>
    <h2>Resmi, terdaftar, dan bisa Anda datangi</h2>
    <p class="ehh-lead">Sebelum memilih travel, cek izinnya. Ini data kami, silakan verifikasi.</p>
    <div class="ehh-legal">
      <div><small>Badan usaha</small><b>PT Dhiyaa El Haramain El Mubarakah</b></div>
      <div><small>Izin PPIU (umroh)</small><b>SK Kemenag No. 63 Tahun 2020</b></div>
      <div><small>Izin PIHK (haji khusus)</small><b>SK Kemenag No. 846 Tahun 2020</b></div>
      <div><small>Keanggotaan</small><b>HIMPUH No. 131/2017 · IATA 15333220</b></div>
      <div><small>Akreditasi</small><b>A, Komite Akreditasi Nasional (KAN)</b></div>
      <div><small>Kantor</small><b>Bekasi (pusat) · Jakarta · Depok · Tangerang · Bogor · Bandung</b></div>
    </div>
    <p class="ehh-note">Pembayaran hanya sah ke rekening atas nama PT Dhiyaa El Haramain El Mubarakah: Bank Mandiri 156.001.150.115.4 atau Bank BSI 710.857.755.4.</p>
  </div>
</section>
<section class="ehh-sec ehh-soft" id="kelas">
  <div class="ehc-wrap">
    <span class="ehh-kick">Pilihan kelas</span>
    <h2>Lima pilihan kelas hotel, satu standar pendampingan</h2>
    <p class="ehh-lead">Semua kelas mendapat fasilitas inti yang sama: tiket, visa, asuransi, hotel bintang 5, makan 3x sehari, pembimbing, mutawwif, dan manasik.</p>
    <div class="ehh-tiers">{"".join(kelas(*k) for k in KELAS)}</div>
  </div>
</section></div>'''

tengah = f'''<div class="ehc ehh"><section class="ehh-sec ehh-dark">
  <div class="ehc-wrap">
    <span class="ehh-kick">Sebelum Anda membayar</span>
    <h2>Menitipkan ibadah itu soal percaya.<br>Ini yang bisa Anda pegang.</h2>
    <div class="ehh-g3">
      {kartu('tameng', 'Izin yang bisa dicek sendiri', 'PPIU SK Kemenag No. 63/2020 dan PIHK No. 846/2020 atas nama PT Dhiyaa El Haramain El Mubarakah, terakreditasi A oleh KAN.')}
      {kartu('dok', 'Semua tertulis sebelum membayar', 'Rincian yang termasuk dan belum termasuk, ketentuan pembayaran, dan pembatalan dijelaskan sebelum Anda daftar.')}
      {kartu('dompet', 'Rekening resmi atas nama perusahaan', 'Pembayaran hanya ke Bank Mandiri atau BSI atas nama PT Dhiyaa El Haramain El Mubarakah, bukan rekening pribadi.')}
      {kartu('kalender', 'Jadwal bayar yang jelas', 'DP Rp 6.000.000 per orang untuk kunci kursi, pelunasan paling lambat 35 hari sebelum berangkat.')}
      {kartu('tukar', 'Kalau rencana berubah', 'Pindah tanggal atau program bisa dilakukan paling lambat 40 hari sebelum keberangkatan.')}
      {kartu('chat', 'Tanya dulu, tanpa tekanan', 'Konsultasi gratis lewat WhatsApp atau datang langsung ke salah satu dari 6 kantor kami.')}
    </div>
  </div>
</section>
<section class="ehh-sec" id="dokumentasi">
  <div class="ehc-wrap">
    <span class="ehh-kick">Dokumentasi asli kami</span>
    <h2>Momen jamaah di Tanah Suci</h2>
    <p class="ehh-lead">Foto dari perjalanan jamaah Elharamain Wisata sendiri, bukan foto stok.</p>
    <div class="ehh-mos">{"".join(f'<figure class="{k}"><img loading="lazy" src="{UP}2026/10/{f}-1024x640.jpg" alt="Jamaah Elharamain Wisata, {t}"><figcaption>{t}</figcaption></figure>' for f, t, k in FOTO)}</div>
  </div>
</section>
<section class="ehh-sec ehh-soft" id="layanan">
  <div class="ehc-wrap">
    <span class="ehh-kick">Layanan kami</span>
    <h2>Satu pintu untuk perjalanan ibadah Anda</h2>
    <div class="ehh-g4">{"".join(kartu(i, j, t, f'<a class="ehh-more" href="{SITE}{u}">Lihat selengkapnya →</a>') for i, j, t, u in LAYANAN)}</div>
  </div>
</section>
<section class="ehh-sec" id="pembimbing">
  <div class="ehc-wrap">
    <span class="ehh-kick">Lulusan terbaik Timur Tengah</span>
    <h2>Pembimbing ibadah umroh &amp; haji</h2>
    <p class="ehh-lead">Ibadah dibimbing langsung oleh asatidz yang mendampingi jamaah dari manasik sampai pulang ke tanah air.</p>
    <div class="ehh-ust">{"".join(f'<figure><img loading="lazy" src="{UP}2025/03/{f}.jpg" alt="{n}, pembimbing ibadah Elharamain Wisata"><figcaption>{n}</figcaption></figure>' for f, n in USTADZ)}</div>
  </div>
</section>
<section class="ehh-sec ehh-dark" id="alur">
  <div class="ehc-wrap">
    <span class="ehh-kick">Perjalanan bersama kami</span>
    <h2>Dari chat pertama sampai kembali ke rumah</h2>
    <div class="ehh-g3">{"".join(f'<div class="ehh-card"><span class="ehh-no">0{n}</span>{ikon(i)}<h3>{j}</h3><p>{t}</p></div>' for n, (i, j, t) in enumerate(ALUR, 1))}</div>
  </div>
</section></div>'''

akhir = f'''<div class="ehc ehh"><section class="ehh-sec ehh-soft" id="faq">
  <div class="ehc-wrap">
    <span class="ehh-kick">Pertanyaan umum</span>
    <h2>Yang biasanya ditanyakan sebelum berangkat</h2>
    <div class="ehh-faq">{"".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
  </div>
</section></div>
<style>
.ehh{{--nv:#10213d;--bl:#004AAD;--bl2:#1684CF;--gd:#DBC033;--ln:#e3e9f3;--mu:#55627a;--soft:#f4f7fc}}
.ehh .ehh-sec{{padding:72px 0;background:#fff}}
.ehh .ehh-soft{{background:var(--soft)}}
.ehh .ehh-dark{{background:var(--bl);color:#fff}}
.ehh .ehh-pt0{{padding-top:0}}
.ehh .ehh-up .ehh-g4{{margin-top:-28px;position:relative}}
.ehh .ehh-up .ehh-card{{box-shadow:0 10px 28px rgba(16,33,61,.08)}}
.ehh h2{{font:700 clamp(26px,3.4vw,38px)/1.18 Poppins,sans-serif;margin:0 0 10px;color:var(--nv);letter-spacing:-.01em}}
.ehh .ehh-dark h2,.ehh .ehh-dark h3{{color:#fff}}
.ehh .ehh-kick{{display:block;font:700 12px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--bl);margin-bottom:8px}}
.ehh .ehh-dark .ehh-kick{{color:var(--gd)}}
.ehh .ehh-lead{{color:var(--mu);margin:0 0 28px;max-width:680px}}
.ehh .ehh-dark .ehh-lead,.ehh .ehh-dark p{{color:rgba(255,255,255,.85)}}
.ehh .ehh-note{{font-size:13px;color:var(--mu);margin:16px 0 0;max-width:760px}}
.ehh-btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:13px 20px;border-radius:12px;font:600 15px Poppins,sans-serif;text-decoration:none!important;border:1px solid transparent;transition:transform .15s}}
.ehh-btn:hover{{transform:translateY(-1px)}}
.ehh-wa{{width:18px;height:18px;flex:none;background:currentColor;-webkit-mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z'/%3E%3C/svg%3E") center/contain no-repeat;mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z'/%3E%3C/svg%3E") center/contain no-repeat}}
.ehh-btn.wa{{background:#25D366;color:#fff!important}}
.ehh-btn.pri{{background:var(--bl);color:#fff!important}}
.ehh-btn.glass{{background:rgba(255,255,255,.1);color:#fff!important;border-color:rgba(255,255,255,.45)}}
.ehh-btn.ghost{{background:#fff;color:var(--bl)!important;border-color:#fff}}
.ehh-hero{{position:relative;color:#fff;padding:84px 0 40px;background:linear-gradient(100deg,rgba(16,33,61,.96) 0%,rgba(16,33,61,.85) 45%,rgba(0,74,173,.45) 100%),url({UP}2026/10/hero-jamaah-kabah.jpg) center/cover;}}
.ehh-hero-in{{display:flex;gap:40px;align-items:flex-end;justify-content:space-between}}
.ehh-hero-tx{{max-width:680px}}
.ehh-pill{{display:inline-block;border:1px solid rgba(255,255,255,.45);border-radius:999px;padding:7px 14px;font:700 11px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-bottom:20px}}
.ehh-hero h1{{font:700 clamp(36px,5.4vw,62px)/1.06 Poppins,sans-serif;color:#fff;margin:0 0 18px;letter-spacing:-.02em}}
.ehh-hero h1 em{{font-style:normal;color:var(--gd)}}
.ehh-hero p{{color:rgba(255,255,255,.85);font-size:17px;margin:0 0 26px}}
.ehh-next{{flex:none;width:300px;background:rgba(0,74,173,.88);border:1px solid rgba(255,255,255,.2);border-radius:18px;padding:22px;backdrop-filter:blur(6px)}}
.ehh-next small{{display:block;font:700 11px Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--gd)}}
.ehh-next b{{display:block;font:700 26px Poppins,sans-serif;margin:6px 0 2px}}
.ehh-next span{{display:block;font-size:13px;color:rgba(255,255,255,.7)}}
.ehh-next p{{margin:14px 0 0;font-size:14px}}
.ehh-next strong{{font:700 26px Poppins,sans-serif;color:var(--gd)}}
.ehh-next .ehh-btn{{width:100%;margin-top:16px}}
.ehh-stat{{display:grid;grid-template-columns:repeat(4,1fr);margin-top:44px;border:1px solid rgba(255,255,255,.22);border-radius:16px;overflow:hidden}}
.ehh-stat div{{padding:16px 20px;border-right:1px solid rgba(255,255,255,.22)}}
.ehh-stat div:last-child{{border-right:0}}
.ehh-stat b{{display:block;font:700 26px Poppins,sans-serif}}
.ehh-stat span{{font-size:13px;color:rgba(255,255,255,.75)}}
.ehh-g4{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
.ehh-g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}}
.ehh-card{{background:#fff;border:1px solid var(--ln);border-radius:16px;padding:22px;display:flex;flex-direction:column}}
.ehh-dark .ehh-card{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.2)}}
.ehh-card h3{{font:700 17px/1.35 Poppins,sans-serif;margin:0 0 6px}}
.ehh-card h3{{color:var(--nv)}}
.ehh-card p{{margin:0;font-size:14.5px;color:var(--mu)}}
.ehh-ic{{width:40px;height:40px;border-radius:10px;display:grid;place-items:center;background:#e8eef9;color:var(--bl);margin-bottom:14px}}
.ehh-dark .ehh-ic{{background:rgba(219,192,51,.2);color:var(--gd)}}
.ehh-ic svg{{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}}
.ehh-no{{font:700 13px Poppins,sans-serif;color:var(--gd);margin-bottom:8px}}
.ehh-more{{margin-top:auto;padding-top:14px;font:600 14px Poppins,sans-serif;color:var(--bl)!important;text-decoration:none!important}}
.ehh-jr{{display:flex;align-items:center;gap:20px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);border-radius:16px;padding:16px 18px;margin-bottom:10px}}
.ehh-dt{{flex:none;width:66px;height:66px;border-radius:12px;background:var(--gd);color:var(--nv);display:grid;place-items:center;align-content:center;line-height:1}}
.ehh-dt b{{font:800 26px Poppins,sans-serif}}
.ehh-dt span{{font:700 10.5px Poppins,sans-serif;letter-spacing:.08em;margin-top:4px}}
.ehh-jx{{flex:1;min-width:0}}
.ehh-jx h3{{font:600 15.5px/1.4 Poppins,sans-serif;margin:0 0 2px;color:#fff}}
.ehh-jx p{{margin:0;font-size:13px}}
.ehh-pr b{{font:700 19px Poppins,sans-serif;color:var(--gd)}}
.ehh-jr .ehh-btn{{flex:none;font-size:14px;padding:10px 14px}}
.ehh-legal{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.ehh-legal div{{border:1px solid var(--ln);border-radius:12px;padding:12px 14px;background:var(--soft)}}
.ehh-legal small{{display:block;font-size:12px;color:var(--mu)}}
.ehh-legal b{{font:600 15px Poppins,sans-serif;color:var(--nv)}}
.ehh-tiers{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}}
.ehh-tier{{background:#fff;border:1px solid var(--ln);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.ehh-th{{padding:16px;color:#fff}}
.ehh-th span{{display:inline-block;background:rgba(255,255,255,.2);border-radius:999px;padding:3px 10px;font:700 10.5px Poppins,sans-serif;letter-spacing:.05em;text-transform:uppercase}}
.ehh-th h3{{font:700 19px/1.25 Poppins,sans-serif;margin:10px 0 2px;color:#fff}}
.ehh-th i{{font-style:normal;font-size:12px;letter-spacing:2px;color:#ffe48a}}
.t1 .ehh-th{{background:linear-gradient(135deg,#7a4a22,#b98150)}}.t2 .ehh-th{{background:linear-gradient(135deg,#4f5d70,#95a3b5)}}
.t3 .ehh-th{{background:linear-gradient(135deg,#8c6812,#d0a534)}}.t4 .ehh-th{{background:linear-gradient(135deg,#004AAD,#1684CF)}}
.t5 .ehh-th{{background:linear-gradient(135deg,#8e1b1b,#c0504d)}}
.ehh-tb{{padding:16px;display:flex;flex-direction:column;flex:1}}
.ehh-tb small{{font-size:12px;color:var(--mu)}}
.ehh-tb b{{font:700 22px Poppins,sans-serif;color:var(--nv);white-space:nowrap}}
.ehh-tb p{{font-size:13.5px;color:var(--mu);margin:10px 0 16px}}
.ehh-tb .ehh-btn{{margin-top:auto;font-size:14px;padding:11px}}
.ehh-mos{{display:grid;grid-template-columns:2fr 1fr 1fr;grid-auto-rows:220px;gap:10px}}
.ehh-mos figure{{position:relative;margin:0;border-radius:16px;overflow:hidden}}
.ehh-mos .big{{grid-row:span 2}}
.ehh-mos img{{width:100%;height:100%;object-fit:cover;display:block}}
.ehh-mos figcaption{{position:absolute;left:0;right:0;bottom:0;padding:24px 12px 10px;font-size:12.5px;color:#fff;background:linear-gradient(transparent,rgba(0,0,0,.6))}}
.ehh-ust{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.ehh-ust figure{{margin:0;background:#fff;border:1px solid var(--ln);border-radius:14px;overflow:hidden;text-align:center}}
.ehh-ust img{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}}
.ehh-ust figcaption{{padding:12px 10px;font:600 14px Poppins,sans-serif;color:var(--nv)}}
.ehh-faq{{max-width:820px}}
.ehh-faq details{{background:#fff;border:1px solid var(--ln);border-radius:12px;padding:0 18px;margin-bottom:10px}}
.ehh-faq summary{{cursor:pointer;font:600 15px Poppins,sans-serif;padding:15px 0;color:var(--nv)}}
.ehh-faq p{{margin:0 0 15px;color:var(--mu);font-size:14.5px}}
@media (max-width:1060px){{.ehh-tiers{{grid-template-columns:repeat(3,1fr)}}.ehh-g4{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:900px){{.ehh-hero-in{{flex-direction:column;align-items:stretch}}.ehh-next{{width:auto}}.ehh-stat{{grid-template-columns:repeat(2,1fr)}}.ehh-stat div:nth-child(2){{border-right:0}}.ehh-stat div:nth-child(-n+2){{border-bottom:1px solid rgba(255,255,255,.22)}}.ehh-g3,.ehh-legal{{grid-template-columns:1fr 1fr}}.ehh-ust{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:640px){{.ehh .ehh-sec{{padding:52px 0}}.ehh-hero{{padding:48px 0 32px}}.ehh-g4,.ehh-g3,.ehh-legal,.ehh-tiers{{grid-template-columns:1fr}}.ehh-jr{{flex-wrap:wrap}}.ehh-jr .ehh-btn{{width:100%}}.ehh-mos{{grid-template-columns:1fr 1fr;grid-auto-rows:140px}}.ehh-mos .big{{grid-column:span 2;grid-row:span 1;height:220px}}.ehh-hero .ehc-ctas .ehh-btn{{width:100%}}}}
</style>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}, ensure_ascii=False)}</script>'''

assert '&&' not in hero + tengah + akhir
page = '\n\n'.join([ref('gaya'), ref('lebar'), ref('paket'), blk(hero), blk(tengah), ref('testimoni'), blk(akhir)])
open(HERE + 'halaman/beranda-baru.html', 'w').write(page)
print('beranda-baru', len(page), 'jadwal', len(jadwal), 'pertama', pertama['tgl'], pertama['bln'], pertama['nama'])
