"""Halaman paket Umroh Bronze (page 8869).
Jalankan: python3 halaman-paket/build_bronze.py  → menulis halaman-paket/halaman/bronze.html
Kartu harga diambil dari pattern 9996 (halaman-kota/pattern/9996-paket-harga.html), tag kelas "bronze",
jadi harga di halaman ini selalu sama dengan daftar harga di halaman kota."""
import json, os, re, urllib.parse as up

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
ROOT = HERE + '../'
PUSAT = '6281287292422'
PATTERNS = dict(lebar=9999, gaya=9991, layanan=9992, ketentuan=9993, fasilitas=9995, testimoni=9994)

harga = open(ROOT + 'halaman-kota/pattern/9996-paket-harga.html').read()
css = re.search(r'<style>\n\.ehpk\{.*?</style>', harga, re.S).group(0)
# hanya aturan kartu (tanpa tab), grid selalu tampil
css = re.sub(r'#ehpk-t\d:checked[^\n]*\n', '', css)
css = css.replace('.ehpk .grid{--gap:24px;--col:3;display:none;', '.ehpk .grid{--gap:24px;--col:3;display:flex;')
grids = re.findall(r'<div class="grid g\d">(.*?)</div>\n', harga, re.S)
periode = ['Januari 2027', 'Ramadhan 2027', 'Syawal 2027']
cards = []
for name, g in zip(periode, grids):
    for c in re.findall(r'<a class="card" .*?</a>', g, re.S):
        if 'class="tag bronze"' in c:
            cards.append((name, c))
assert len(cards) == 3, len(cards)


def label(name, c):
    # tampilkan periode keberangkatan di atas nama paket
    return c.replace('<span class="tag bronze">', f'<span class="per">{name}</span><span class="tag bronze">', 1)


wa = lambda t: f'https://api.whatsapp.com/send?phone={PUSAT}&text=' + up.quote(t, safe='')
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z"/></svg>'

top = f'''<div class="ehc"><section class="ehc-hero solo">
  <div class="ehc-wrap">
    <div>
      <nav class="ehc-crumb" aria-label="Breadcrumb"><a href="https://elharamainwisata.com/">Beranda</a> › <a href="https://elharamainwisata.com/paket-umroh-musim-dingin/">Paket Umroh</a> › Bronze</nav>
      <span class="ehc-eyebrow">Paket paling hemat · hotel bintang 5</span>
      <h1>Paket Umroh <em>Bronze</em></h1>
      <p>Umroh hemat tanpa turun kelas: hotel bintang 5 di Makkah dan Madinah, penerbangan langsung, ziarah Thaif, kereta cepat Haramain, dan bimbingan asatidz lulusan Timur Tengah. Tersedia keberangkatan Januari sampai Syawal 2027.</p>
      <div class="ehc-ctas">
        <a class="ehc-btn wa" href="{wa("Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi paket Umroh Bronze.")}" target="_blank" rel="noopener">{WA_SVG} Konsultasi Gratis</a>
        <a class="ehc-btn ghost" href="#harga-bronze">Lihat jadwal &amp; harga</a>
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
<section class="ehc-sec" id="harga-bronze">
  <div class="ehc-wrap">
    <span class="ehc-eyebrow">Jadwal &amp; harga</span>
    <h2>Semua keberangkatan Bronze</h2>
    <p class="ehc-lead">Harga per jamaah untuk kamar quad (ber-4). Harga kamar triple dan double ada di bawah setiap kartu. Klik kartu untuk tanya tanggal lewat WhatsApp.</p>
    {css}<style>.ehpk .per{{display:block;font:700 11px Poppins,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}</style>
    <div class="ehpk" style="margin-top:28px"><div class="grid">
{chr(10).join(label(n, c) for n, c in cards)}
    </div></div>
    <p class="ehc-note">Harga dapat berubah mengikuti kebijakan Saudi dan kurs (asumsi maks. Rp 17.000/USD). Hotel dapat diganti dengan hotel setaraf bila penuh.</p>
  </div>
</section></div>'''

PAKET = [('Silver', 'paket-umroh-silver', 'Hotel bintang 5, 9 hari'), ('Silver 12 Hari', 'umroh-silver-12-hari', 'Lebih lama, 12 hari'),
         ('Platinum', 'umroh-platinum', 'Hotel di Zamzam Tower'), ('Premium', 'umroh-premium', 'Fairmont & Movenpick'),
         ('Umroh Syawal', 'umroh-syawal', 'Berangkat Maret 2027'), ('Musim Dingin', 'paket-umroh-musim-dingin', 'Semua paket Des–Ramadhan')]
KOTA = [('Bekasi', 'Harapan Indah (pusat)'), ('Jakarta', 'Tebet'), ('Depok', 'Margonda'), ('Tangerang', 'BSD'), ('Bogor', 'Summarecon Bogor'), ('Bandung', 'Summarecon Bandung')]
city = lambda href, b, s: f'<a class="ehc-city" href="{href}"><b>{b}</b><span>{s}</span></a>'
end = f'''<div class="ehc"><section class="ehc-sec" id="paket-lain">
  <div class="ehc-wrap">
    <span class="ehc-eyebrow">Bandingkan</span>
    <h2>Paket lain &amp; kantor terdekat</h2>
    <div class="ehc-cities ehc-6" style="margin-top:20px">{"".join(city(f"https://elharamainwisata.com/{s}/", n, d) for n, s, d in PAKET)}</div>
    <p class="ehc-arealbl" style="text-align:center;margin-top:28px!important"><b>Daftar langsung di kantor terdekat:</b></p>
    <div class="ehc-cities ehc-6">{"".join(city(f"https://elharamainwisata.com/travel-umroh-{k.lower()}/", k, s) for k, s in KOTA)}</div>
  </div>
</section></div>
<style>
/* Bronze: urutan latar harga(putih) layanan(abu) ketentuan(putih) fasilitas(abu) testimoni(putih) paket-lain(abu) */
body .ehc-sec:has(.ehfk){{background:#fff!important}}
#harga-bronze{{background:#fff!important}}
#paket-lain{{background:var(--soft)!important}}
.ehc-6{{grid-template-columns:repeat(6,1fr)}}
@media (max-width:960px){{.ehc-6{{grid-template-columns:repeat(3,1fr)}}}}
@media (max-width:640px){{.ehc-6{{grid-template-columns:repeat(2,1fr)}}}}
</style>'''

trips = []
for name, c in cards:
    title = re.search(r'alt="([^"]+)"', c).group(1)
    price = int(re.sub(r'\D', '', re.search(r'<b>(Rp [^<]+)</b>', c).group(1)))
    dates = re.search(r'Berangkat</i><span>([^<]+)</span>', c).group(1).replace('&amp;', '&')
    dur = re.search(r'Durasi</i><span>([^<]+)</span>', c).group(1)
    trips.append({"@type": "TouristTrip", "name": f"{title} ({dur})", "description": f"Keberangkatan {dates}",
                  "provider": {"@type": "TravelAgency", "name": "Elharamain Wisata", "url": "https://elharamainwisata.com/"},
                  "offers": {"@type": "Offer", "price": price, "priceCurrency": "IDR", "availability": "https://schema.org/InStock",
                             "url": "https://elharamainwisata.com/umroh-bronze/#harga-bronze"}})
ld = {"@context": "https://schema.org", "@graph": trips}
end += f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'

blk = lambda h: '<!-- wp:html -->\n' + h.strip() + '\n<!-- /wp:html -->'
ref = lambda k: '<!-- wp:block {"ref":%d} /-->' % PATTERNS[k]
page = '\n\n'.join([ref('gaya'), ref('lebar'), blk(top), ref('layanan'), ref('ketentuan'), ref('fasilitas'), ref('testimoni'), blk(end)])
os.makedirs(HERE + 'halaman', exist_ok=True)
open(HERE + 'halaman/bronze.html', 'w').write(page)
print('bronze', len(page), [n for n, _ in cards])
