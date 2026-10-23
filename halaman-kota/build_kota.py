"""Jalankan: python3 halaman-kota/build_kota.py  → menulis halaman-kota/halaman/<kota>.html.
Bangun blok khusus kota (hero/kantor/jadwal, area/legalitas/langkah + WA cabang, FAQ/kantor lain/penutup + JSON-LD).
Sumber data kantor: repo khaeruddienfatih/web (tools/build_pages.py, tools/build_footer.py, README)."""
import json, re, sys, urllib.parse as up

import os
G = os.path.dirname(os.path.abspath(__file__)) + '/'
PUSAT = '6281287292422'
PATTERNS = dict(lebar=9999, gaya=9991, layanan=9992, harga=9996, ketentuan=9993, fasilitas=9995, testimoni=9994)

OFF = {
 'Bekasi': dict(id=9584, slug='bekasi', role='Kantor Pusat', spot='Harapan Indah, Bekasi', short='Harapan Indah',
   addr='Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya, Kec. Medan Satria, Kota Bekasi, Jawa Barat 17132',
   street='Ruko Emerald No.5 Blok EB 1, Jl. Harapan Indah Raya', loc='Kota Bekasi', reg='Jawa Barat', zip='17132',
   phone='081287292422', maps='Elharamain Wisata Ruko Emerald No.5 Blok EB 1 Harapan Indah Bekasi',
   region='se-Bekasi Raya', intro='dari Bekasi Kota sampai Cikarang', trip='±1 jam ke Soekarno-Hatta lewat Tol JORR',
   areas=['Bekasi Barat','Bekasi Utara','Bekasi Timur','Bekasi Selatan','Medan Satria','Harapan Indah','Pondok Gede','Jatiasih','Tambun','Cibitung','Cikarang']),
 'Jakarta': dict(id=9585, slug='jakarta', role='Kantor Cabang', spot='Tebet, Jakarta Selatan', short='Tebet',
   addr='Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet, Kota Jakarta Selatan, DKI Jakarta 12820',
   street='Jl. Tebet Raya No.39 B, Tebet Timur, Kec. Tebet', loc='Jakarta Selatan', reg='DKI Jakarta', zip='12820',
   phone='081214178056', maps='Elharamain Wisata Jl. Tebet Raya No.39 B Tebet Jakarta Selatan',
   region='se-DKI Jakarta', intro='dari Jakarta Selatan sampai Jakarta Utara', trip='±45–60 menit ke Soekarno-Hatta lewat tol dalam kota',
   areas=['Jakarta Selatan','Jakarta Timur','Jakarta Pusat','Jakarta Barat','Jakarta Utara','Tebet','Pancoran','Kuningan','Cawang','Kalibata','Pasar Minggu']),
 'Depok': dict(id=9586, slug='depok', role='Kantor Cabang', spot='Margonda, Depok', short='Margonda',
   addr='Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji, Kota Depok, Jawa Barat',
   street='Jl. Margonda No.252 D, Kemiri Muka, Kec. Beji', loc='Kota Depok', reg='Jawa Barat', zip='',
   phone='085179988198', maps='Elharamain Wisata Jl. Margonda No.252 D Kemiri Muka Beji Depok',
   region='se-Kota Depok', intro='dari Beji sampai Sawangan dan Cimanggis', trip='±1–1,5 jam ke Soekarno-Hatta lewat tol',
   areas=['Beji','Pancoran Mas','Sukmajaya','Cimanggis','Cilodong','Cinere','Limo','Sawangan','Bojongsari','Tapos']),
 'Tangerang': dict(id=9587, slug='tangerang', role='Kantor Cabang', spot='BSD, Tangerang Selatan', short='BSD',
   addr='Ruko Pasar Modern No.18 BSD, Rawa Mekar Jaya, Kec. Serpong, Kota Tangerang Selatan, Banten 15318',
   street='Ruko Pasar Modern No.18 BSD, Rawa Mekar Jaya, Kec. Serpong', loc='Tangerang Selatan', reg='Banten', zip='15318',
   phone='085693883208', maps='Elharamain Wisata Ruko Pasar Modern No.18 BSD Serpong Tangerang Selatan',
   region='se-Tangerang Raya', intro='dari BSD, Bintaro, sampai Kota dan Kabupaten Tangerang', trip='±45 menit ke Soekarno-Hatta lewat tol',
   areas=['Tangerang Selatan','BSD','Serpong','Gading Serpong','Pamulang','Ciputat','Bintaro','Pondok Aren','Kota Tangerang','Kabupaten Tangerang','Cikupa']),
 'Bogor': dict(id=9588, slug='bogor', role='Kantor Cabang', spot='Summarecon Bogor', short='Summarecon Bogor',
   addr='Ruko Graha Boulevard GBVD No.10, Jl. Summarecon Bogor, Sukatani, Kec. Sukaraja, Kab. Bogor, Jawa Barat 16144',
   street='Ruko Graha Boulevard GBVD No.10, Jl. Summarecon Bogor, Sukatani, Kec. Sukaraja', loc='Kabupaten Bogor', reg='Jawa Barat', zip='16144',
   phone='082260126394', maps='Elharamain Wisata Ruko Graha Boulevard GBVD No.10 Summarecon Bogor',
   region='se-Bogor Raya', intro='dari Kota Bogor sampai Cibinong dan Cileungsi', trip='±1,5–2 jam ke Soekarno-Hatta lewat Tol Jagorawi',
   areas=['Kota Bogor','Kabupaten Bogor','Sukaraja','Cibinong','Sentul','Ciawi','Citeureup','Cileungsi','Gunung Putri','Dramaga']),
 'Bandung': dict(id=9589, slug='bandung', role='Kantor Cabang', spot='Summarecon Bandung', short='Summarecon Bandung',
   addr='Jl. Boulevard Utama Blok RC No.18, Ruby Commercial Summarecon Bandung, Kota Bandung, Jawa Barat',
   street='Jl. Boulevard Utama Blok RC No.18, Ruby Commercial Summarecon Bandung', loc='Kota Bandung', reg='Jawa Barat', zip='',
   phone='08132212344', maps='Elharamain Wisata Ruby Commercial Summarecon Bandung',
   region='se-Bandung Raya', intro='dari Kota Bandung sampai Cimahi dan Soreang', trip='±3 jam ke Soekarno-Hatta lewat Tol Cipularang',
   areas=['Kota Bandung','Kabupaten Bandung','Bandung Barat','Cimahi','Gedebage','Buahbatu','Rancasari','Antapani','Arcamanik','Soreang']),
}

def intl(p): return '62' + p[1:]
def fmt(p):
    return f'{p[:4]}-{p[4:8]}-{p[8:]}'
def wa(o, text): return f'https://api.whatsapp.com/send?phone={intl(o["phone"])}&text=' + up.quote(text, safe='')
def mapq(o): return o['maps'].replace(' ', '+')

DES = [('01','Des','Silver · Madinah First','9 hari · Saudia direct · juga 7 Des','Rp 38 jt','Umroh Silver Madinah First 1 Desember 2026'),
 ('07','Des','Platinum','9 hari · Saudia direct','Rp 46,5 jt','Umroh Platinum 7 Desember 2026'),
 ('08','Des','Bronze','9 hari · Saudia direct · paling hemat','Rp 36,5 jt','Umroh Bronze 8 Desember 2026'),
 ('08','Des','Silver · Makkah First','9 hari · Saudia direct','Rp 37,5 jt','Umroh Silver Makkah First 8 Desember 2026'),
 ('09','Des','Silver 12 Hari','12 hari · Saudia direct','Rp 41,5 jt','Umroh Silver 12 Hari 9 Desember 2026'),
 ('11','Des','Bronze Plus','9 hari · Saudia direct · juga 12 Des','Rp 37,5 jt','Umroh Bronze Plus 11 Desember 2026')]
SYA = [('08','Mar','Silver 12 Hari','12 hari · Garuda Indonesia · Anjum &amp; Al-Aqeeq','Rp 46 jt','Umroh Syawal Silver 12 Hari 8 Maret 2027'),
 ('08','Mar','Gold 12 Hari','12 hari · Garuda Indonesia · Marwa Rotana / Movenpick','Rp 57 jt','Umroh Syawal Gold 12 Hari 8 Maret 2027'),
 ('10','Mar','Platinum','9 hari · Saudia · juga 13 &amp; 14 Mar','Rp 47,5 jt','Umroh Syawal Platinum 10 Maret 2027'),
 ('11','Mar','Silver','9 hari · Saudia · juga 14 &amp; 22 Mar','Rp 39,5 jt','Umroh Syawal Silver 11 Maret 2027'),
 ('16','Mar','Bronze','10 hari · Riyadh Air · paling hemat','Rp 37,5 jt','Umroh Syawal Bronze 16 Maret 2027')]

WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z"/></svg>'

def row(o, city, r):
    d, m, t, meta, price, ask = r
    href = wa(o, f"Assalamu'alaikum, saya dari {city}, mau tanya {ask}.")
    return (f'<div class="ehc-row"><div class="ehc-badge"><b>{d}</b><span>{m}</span></div><div><h3>{t}</h3><div class="meta">{meta}</div></div>'
            f'<div class="from"><small>mulai</small><b>{price}</b></div><a class="ehc-btn wa" href="{href}" target="_blank" rel="noopener">Tanya tanggal ini</a></div>')

def top(city, o):
    pusat = o['role'] == 'Kantor Pusat'
    return f'''<div class="ehc"><section class="ehc-hero solo">
  <div class="ehc-wrap">
    <div>
      <nav class="ehc-crumb" aria-label="Breadcrumb"><a href="https://elharamainwisata.com/">Beranda</a> › <a href="https://elharamainwisata.com/kantor-cabang/">Kantor Cabang</a> › {city}</nav>
      <span class="ehc-eyebrow">{o["role"]} · {o["spot"]}</span>
      <h1>Travel Umroh <em>{city}</em> Resmi &amp; Terpercaya</h1>
      <p>Melayani jamaah {o["region"]}, {o["intro"]}. Hotel bintang 5 dekat Masjidil Haram, pesawat langsung Saudia, ziarah Thaif, dan kereta cepat Haramain. Izin resmi Kemenag, bisa Anda cek sendiri.</p>
      <div class="ehc-ctas">
        <a class="ehc-btn wa" href="{wa(o, f"Assalamu'alaikum Elharamain Wisata {city}, saya ingin konsultasi paket umroh.")}" target="_blank" rel="noopener">{WA_SVG} Konsultasi Gratis</a>
        <a class="ehc-btn ghost" href="#paket-harga">Lihat paket &amp; harga</a>
      </div>
      <div class="ehc-chips">
        <span class="ehc-chip">Izin Umrah SK Kemenag No. 63/2020</span>
        <span class="ehc-chip">Izin Haji SK No. 846/2020</span>
        <span class="ehc-chip">Anggota HIMPUH &amp; IATA</span>
      </div>
    </div>
  </div>
</section>
<section class="ehc-stats" aria-label="Sekilas Elharamain">
  <div class="ehc-wrap">
    <div class="ehc-stat"><b>6.800+</b><span>ulasan Google bintang 5</span></div>
    <div class="ehc-stat"><b>6 kantor</b><span>Bekasi, Jakarta, Depok, Tangerang, Bogor, Bandung</span></div>
    <div class="ehc-stat"><b>Akreditasi A</b><span>Komite Akreditasi Nasional</span></div>
    <div class="ehc-stat"><b>IATA</b><span>Kode 15333220</span></div>
  </div>
</section>
<section class="ehc-sec" id="kantor">
  <div class="ehc-wrap ehc-office">
    <div class="ehc-card">
      <span class="ehc-eyebrow">Kantor {city}</span>
      <h2>Mampir, ngobrol langsung dengan tim kami</h2>
      <p class="ehc-lead">Konsultasi paket, serahkan berkas paspor, dan daftar langsung di {"kantor pusat" if pusat else "kantor " + o["short"]}. Kabari kami lewat WhatsApp sebelum datang supaya tim siap menyambut.</p>
      <div class="ehc-dl">
        <div><svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg><p><b>Alamat</b><span>{o["addr"]}</span></p></div>
        <div><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg><p><b>Telepon / WhatsApp</b><span><a href="tel:+{intl(o["phone"])}">{fmt(o["phone"])}</a></span></p></div>
        <div><svg viewBox="0 0 24 24"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5Z"/></svg><p><b>Bandara keberangkatan</b><span>Soekarno-Hatta, kumpul di VIP Lounge Umroh</span></p></div>
      </div>
      <div class="ehc-ctas" style="margin-top:0">
        <a class="ehc-btn pri" href="https://www.google.com/maps/search/?api=1&query={mapq(o)}" target="_blank" rel="noopener">Buka di Google Maps</a>
        <a class="ehc-btn out" href="{wa(o, f"Assalamu'alaikum, saya ingin atur kunjungan ke kantor Elharamain {city}.")}" target="_blank" rel="noopener">Atur kunjungan</a>
      </div>
      <div class="ehc-route"><b>Rute ke bandara:</b> dari {o["short"]} {o["trip"]}, tergantung lalu lintas.</div>
      <p class="ehc-arealbl"><b>Area layanan:</b></p>
      <div class="ehc-areas ehc-areas-l">{"".join(f'<span class="ehc-area">{a}</span>' for a in o["areas"])}</div>
    </div>
    <div class="ehc-map">
      <iframe title="Peta kantor Elharamain Wisata {city}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={mapq(o)}&output=embed"></iframe>
    </div>
  </div>
</section></div>'''

def mid(city, o):
    no = intl(o['phone'])
    areas = ''.join(f'<span class="ehc-area">{a}</span>' for a in o['areas'])
    tpl = open(G + 'template/c_mid.html').read()
    legal = re.search(r'<section class="ehc-sec" id="legalitas">.*?</section>', tpl, re.S).group(0)
    legal = re.sub(r'\s*<div class="ehc-warn">.*?</div>\n', '\n', legal, flags=re.S).replace('class="ehc-legal"', 'class="ehc-legal ehc-legal-1"')
    assert 'ehc-warn' not in legal
    script = re.search(r'<script.*?</script>', tpl, re.S).group(0).replace(f"var NO='{PUSAT}'", f"var NO='{no}'")
    assert f"var NO='{no}'" in script
    return f'''<div class="ehc">{legal}</div>
<!-- WA cabang: klik WhatsApp ke nomor pusat di halaman ini dialihkan ke nomor kantor {city}; rotasi Click to Chat dikunci ke nomor cabang. -->
{script}'''

def end(city, o):
    pusat = o['role'] == 'Kantor Pusat'
    others = ''.join(f'<a class="ehc-city" href="https://elharamainwisata.com/travel-umroh-{p["slug"]}/"><b>{c}</b><span>{p["short"]}</span></a>'
                     for c, p in OFF.items() if c != city)
    faqs = [
     (f'Di mana kantor Elharamain Wisata di {city}?', f'{o["addr"]}. {"Ini kantor pusat kami. " if pusat else ""}WhatsApp: {fmt(o["phone"])}.'),
     ('Perlu janji dulu sebelum datang ke kantor?', 'Sebaiknya kabari kami lewat WhatsApp sebelum datang, supaya tim yang menangani paket Anda siap menyambut.'),
     (f'Berapa biaya umroh dari {city}?', 'Mulai Rp 37.500.000 per jamaah (kamar quad) untuk keberangkatan Syawal 2027. Harga sama di semua kantor dan tergantung paket, hotel, serta tanggal.'),
     ('Ada paket umroh Syawal 2027?', 'Ada. Umroh Syawal berangkat 8–22 Maret 2027, mulai Rp 37.500.000 per jamaah (Bronze 10 hari, kamar quad). Tersedia juga Silver, Platinum, Silver 12 Hari, dan Gold 12 Hari dengan hotel bintang 5.'),
     (f'Jamaah {city} berangkat dari bandara mana?', f'Dari Bandara Soekarno-Hatta, berkumpul di VIP Lounge Umroh. Dari {o["short"]} {o["trip"]}, tergantung lalu lintas.'),
     ('Bagaimana sistem DP dan pelunasannya?', 'DP Rp 6.000.000 per jamaah, pelunasan paling lambat 35 hari sebelum berangkat. Pembayaran hanya sah ke rekening PT Dhiyaa El Haramain El Mubarakah.'),
     ('Apakah Elharamain travel umroh resmi?', 'Ya. Izin Umrah SK Kemenag No. 63 Tahun 2020 dan Izin Haji SK No. 846 Tahun 2020, anggota HIMPUH dan IATA, serta terakreditasi A oleh KAN.'),
    ]
    det = '\n'.join(f'      <details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faqs))
    addr = {"@type": "PostalAddress", "streetAddress": o['street'], "addressLocality": o['loc'], "addressRegion": o['reg'], "addressCountry": "ID"}
    if o['zip']: addr['postalCode'] = o['zip']
    ld = {"@context": "https://schema.org", "@graph": [
      {"@type": "TravelAgency", "name": f"Elharamain Wisata {city}", "legalName": "PT Dhiyaa El Haramain El Mubarakah",
       "url": f"https://elharamainwisata.com/travel-umroh-{o['slug']}/",
       "logo": "https://elharamainwisata.com/wp-content/uploads/2025/03/Assets-LP-Haji-ONH-Plus-3-1.webp",
       "telephone": '+' + intl(o['phone']), "address": addr, "areaServed": o['areas'], "priceRange": "Rp 37.500.000 - Rp 71.000.000"}]}
    return f'''<div class="ehc"><section class="ehc-sec alt" id="kantor-lain">
  <div class="ehc-wrap">
    <span class="ehc-eyebrow">Kantor lainnya</span>
    <h2>Lebih dekat ke kota lain?</h2>
    <p class="ehc-lead">Semua kantor melayani konsultasi, jadwal, dan pendaftaran dengan paket dan harga yang sama.</p>
    <div class="ehc-cities" style="margin-top:20px">{others}</div>
  </div>
</section></div>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'''

blk = lambda h: '<!-- wp:html -->\n' + h.strip() + '\n<!-- /wp:html -->'
ref = lambda k: '<!-- wp:block {"ref":%d} /-->' % PATTERNS[k]
for city, o in OFF.items():
    page = '\n\n'.join([ref('gaya'), ref('lebar'), blk(top(city, o)), ref('layanan'), ref('harga'), ref('ketentuan'),
                        blk(mid(city, o)), ref('fasilitas'), ref('testimoni'), blk(end(city, o))])
    open(G + f'halaman/{o["slug"]}.html', 'w').write(page)
    print(city, o['id'], len(page))
