"""Halaman paket umroh (Bronze, Silver, 12 Hari, Platinum, Premium, Syawal, Musim Dingin).
Jalankan: python3 halaman-paket/build_paket.py  → menulis halaman-paket/halaman/<kunci>.html
Kartu harga diambil dari pattern 9996 (halaman-kota/pattern/9996-paket-harga.html) sesuai aturan `pilih` tiap halaman,
jadi harga di halaman paket selalu sama dengan daftar harga di halaman kota."""
import json, os, re, urllib.parse as up

HERE = os.path.dirname(os.path.abspath(__file__)) + '/'
ROOT = HERE + '../'
SITE = 'https://elharamainwisata.com/'
PUSAT = '6281287292422'
PATTERNS = dict(lebar=9999, gaya=9991, layanan=9992, ketentuan=9993, fasilitas=9995, testimoni=9994, paket=10076)
# pattern 'Paket: kartu & rotator WA' (CSS kartu + script rotator), dipakai semua halaman paket
POLA_PAKET = HERE + 'pattern/10076-kartu-rotator.html'

harga = open(ROOT + 'halaman-kota/pattern/9996-paket-harga.html').read()
css = re.search(r'<style>\n\.ehpk\{.*?</style>', harga, re.S).group(0)
# hanya aturan kartu (tanpa tab), grid selalu tampil
css = re.sub(r'#ehpk-t\d:checked[^\n]*\n', '', css)
css = css.replace('.ehpk .grid{--gap:24px;--col:3;display:none;', '.ehpk .grid{--gap:24px;--col:3;display:flex;')
PERIODE = ['Januari 2027', 'Ramadhan 2027', 'Syawal 2027']
grids = re.findall(r'<div class="grid g\d">(.*?)</div>\n', harga, re.S)
assert len(grids) == len(PERIODE), len(grids)
# semua kartu: (periode, kelas tag, nama paket, html kartu)
SEMUA = []
for per, g in zip(PERIODE, grids):
    for c in re.findall(r'<a class="card" .*?</a>', g, re.S):
        kelas, nama = re.search(r'<span class="tag ([a-z]+)">([^<]+)</span>', c).groups()
        SEMUA.append((per, kelas, nama, c))

# kunci, page id, slug, nama pendek, judul h1, eyebrow, paragraf hero, aturan kartu, kelompokkan per periode
PAGES = [
    dict(key='bronze', id=8869, slug='umroh-bronze', nama='Bronze', h1='Paket Umroh <em>Bronze</em>',
         eyebrow='Paket paling hemat · hotel bintang 5',
         intro='Umroh hemat tanpa turun kelas: hotel bintang 5 di Makkah dan Madinah, penerbangan langsung, ziarah Thaif, kereta cepat Haramain, dan bimbingan asatidz lulusan Timur Tengah. Tersedia keberangkatan Januari sampai Syawal 2027.',
         pilih=lambda k, n: k == 'bronze'),
    dict(key='silver', id=8896, slug='paket-umroh-silver', nama='Silver', h1='Paket Umroh <em>Silver</em>',
         eyebrow='Hotel bintang 5 · terbang dengan Saudia',
         intro="Umroh 9 hari dengan hotel Anjum bintang 5 di Makkah dan Al-Aqeeq bintang 5 di Madinah, penerbangan langsung Saudia Airlines, ziarah Thaif, kereta cepat Haramain, dan bimbingan asatidz lulusan Timur Tengah. Ada juga paket I'tikaf 17 hari untuk 10 malam terakhir Ramadhan.",
         pilih=lambda k, n: k == 'silver' and '12 Hari' not in n),
    dict(key='silver-12', id=8910, slug='umroh-silver-12-hari', nama='12 Hari', h1='Paket Umroh <em>12 Hari</em>',
         eyebrow='Waktu ibadah lebih panjang · hotel bintang 5',
         intro='Lebih lama di Tanah Suci tanpa terburu-buru. Pilih Silver 12 Hari dengan hotel Anjum, atau Gold 12 Hari dengan hotel Marwa Rotana / Movenpick di Zamzam Tower. Di Madinah menginap di Al-Aqeeq bintang 5. Januari terbang dengan Saudia, Syawal dengan Garuda Indonesia.',
         pilih=lambda k, n: '12 Hari' in n),
    dict(key='platinum', id=8908, slug='umroh-platinum', nama='Platinum', h1='Paket Umroh <em>Platinum</em>',
         eyebrow='Hotel di Zamzam Tower · depan Masjidil Haram',
         intro='Menginap di Zamzam Tower, tepat di depan Masjidil Haram: hotel Marwa Rotana atau Movenpick Hajar bintang 5. Terbang langsung dengan Saudia Airlines, lengkap dengan ziarah Thaif, kereta cepat Haramain, dan bimbingan asatidz lulusan Timur Tengah. Tersedia Januari, Ramadhan, dan Syawal 2027.',
         pilih=lambda k, n: k == 'platinum'),
    dict(key='premium', id=8909, slug='umroh-premium', nama='Premium', h1='Paket Umroh <em>Premium</em>',
         eyebrow='Kelas tertinggi · Fairmont Makkah',
         intro="Umroh paling nyaman bersama Elharamain Wisata: hotel Fairmont Makkah Clock Royal Tower bintang 5 di depan Masjidil Haram, terbang langsung dengan Saudia Airlines, ziarah Thaif dan kereta cepat Haramain. Paket Ramadhan sudah termasuk golf car untuk umroh dan sa'i.",
         pilih=lambda k, n: k == 'premium'),
    dict(key='syawal', id=9935, slug='umroh-syawal', nama='Syawal', h1='Paket Umroh <em>Syawal 2027</em>',
         eyebrow='Berangkat Maret 2027 · setelah Lebaran',
         intro='Umroh setelah Idul Fitri, berangkat 8 sampai 22 Maret 2027. Pilih Bronze, Silver, Silver 12 Hari, Platinum, atau Gold 12 Hari, terbang dengan Riyadh Air, Saudia Airlines, atau Garuda Indonesia. Semua paket menginap di hotel bintang 5.',
         pilih=lambda k, n: True, periode=['Syawal 2027']),
    dict(key='musim-dingin', id=9581, slug='paket-umroh-musim-dingin', nama='Musim Dingin', h1='Paket Umroh <em>Musim Dingin 2027</em>',
         eyebrow='Januari & Ramadhan 2027 · cuaca sejuk',
         intro='Umroh saat cuaca Makkah dan Madinah paling sejuk. Ada 10 pilihan paket keberangkatan Januari dan Ramadhan 2027 (berangkat Februari), dari Bronze sampai Premium, semuanya terbang langsung dengan Saudia Airlines.',
         pilih=lambda k, n: True, periode=['Januari 2027', 'Ramadhan 2027'], kelompok=True),
]


def label(per, c):
    # tampilkan periode keberangkatan di atas nama paket, lalu tombol WhatsApp
    # (span, karena kartu sudah berupa link WA yang ikut dirotasi)
    c = c.replace('<span class="tag ', f'<span class="per">{per}</span><span class="tag ', 1)
    return c.replace('</p></div></a>', f'</p><span class="ehc-btn wa wa-kartu">{WA_SVG} Tanya via WhatsApp</span></div></a>', 1)


wa = lambda t: f'https://api.whatsapp.com/send?phone={PUSAT}&text=' + up.quote(t, safe='')
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.1.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.4Z"/></svg>'

# Rotator WA: semua link WhatsApp ke nomor pusat di halaman ini dialihkan ke salah satu nomor CS kantor
# (pilihan pemilik: 5 nomor Click to Chat + Tangerang & Bogor). Satu pengunjung tetap dapat CS yang sama (localStorage).
# Catatan: jangan pakai && di script inline — wptexturize mengubahnya jadi &#038;&#038; dan script rusak.
ROTATOR = ['6281287292422', '6281214178056', '6285179988198', '628132212344', '6285843372026',
           '6285693883208', '6282260126394']
SCRIPT = """
<script data-no-optimize="1" data-no-defer="1" data-cfasync="false">
(function(){
  var PUSAT='%s', NOMOR=%s, KEY='ehc_wa_cs';
  function nomorCS(){
    var n=NOMOR,no=null;
    try{no=localStorage.getItem(KEY);}catch(e){}
    if(!no||n.indexOf(no)==-1){no=n[Math.floor(Math.random()*n.length)];try{localStorage.setItem(KEY,no);}catch(e){}}
    return no;
  }
  function ganti(a){
    if(!/whatsapp\\.com|wa\\.me/.test(a.href)) return;
    if(!a.dataset.waAsli) a.dataset.waAsli=a.href;
    a.href=a.dataset.waAsli.split(PUSAT).join(nomorCS());
  }
  function semua(){document.querySelectorAll('a[href*="'+PUSAT+'"]').forEach(ganti);}
  document.addEventListener('click',function(e){if(!e.target.closest)return;var a=e.target.closest('a[href]');if(!a)return;if(a.dataset.waAsli||a.href.indexOf(PUSAT)!=-1)ganti(a);},true);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',semua);else semua();
})();
</script>""" % (PUSAT, json.dumps(ROTATOR))

blk = lambda h: '<!-- wp:html -->\n' + h.strip() + '\n<!-- /wp:html -->'
ref = lambda k: '<!-- wp:block {"ref":%d} /-->' % PATTERNS[k]


def bangun(p):
    periode = p.get('periode', PERIODE)
    cards = [(per, c) for per, k, n, c in SEMUA if per in periode and p['pilih'](k, n)]
    assert cards, p['key']
    anchor = 'harga-' + p['key']
    if p.get('kelompok'):
        isi = ''.join(f'''
    <h3 class="ehpk-per">{per}</h3>
    <div class="ehpk"><div class="grid">
{chr(10).join(label(q, c) for q, c in cards if q == per)}
    </div></div>''' for per in periode)
    else:
        isi = f'''
    <div class="ehpk" style="margin-top:28px"><div class="grid">
{chr(10).join(label(q, c) for q, c in cards)}
    </div></div>'''
    crumb = '' if p['key'] == 'musim-dingin' else f' › <a href="{SITE}paket-umroh-musim-dingin/">Paket Umroh</a>'
    top = f'''<div class="ehc"><section class="ehc-hero solo">
  <div class="ehc-wrap">
    <div>
      <nav class="ehc-crumb" aria-label="Breadcrumb"><a href="{SITE}">Beranda</a>{crumb} › {p['nama'] if p['key'] != 'musim-dingin' else 'Paket Umroh Musim Dingin'}</nav>
      <span class="ehc-eyebrow">{p['eyebrow']}</span>
      <h1>{p['h1']}</h1>
      <p>{p['intro']}</p>
      <div class="ehc-ctas">
        <a class="ehc-btn wa" href="{wa(f"Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi paket Umroh {p['nama']}.")}" target="_blank" rel="noopener">{WA_SVG} Konsultasi Gratis</a>
        <a class="ehc-btn ghost" href="#{anchor}">Lihat jadwal &amp; harga</a>
      </div>
      <div class="ehc-chips">
        <span class="ehc-chip">Izin Umrah SK Kemenag No. 63/2020</span>
        <span class="ehc-chip">Izin Haji SK No. 846/2020</span>
        <span class="ehc-chip">Anggota HIMPUH &amp; IATA</span>
      </div>
    </div>
  </div>
</section>
<section class="ehc-stats" aria-label="Sekilas Elharamain Wisata">
  <div class="ehc-wrap">
    <div class="ehc-stat"><b>6.800+</b><span>ulasan Google bintang 5</span></div>
    <div class="ehc-stat"><b>6 kantor</b><span>Bekasi, Jakarta, Depok, Tangerang, Bogor, Bandung</span></div>
    <div class="ehc-stat"><b>Akreditasi A</b><span>Komite Akreditasi Nasional</span></div>
    <div class="ehc-stat"><b>IATA</b><span>Kode 15333220</span></div>
  </div>
</section>
<section class="ehc-sec" id="{anchor}">
  <div class="ehc-wrap">
    <span class="ehc-eyebrow">Jadwal &amp; harga</span>
    <h2>Semua keberangkatan {p['nama']}</h2>
    <p class="ehc-lead">Harga per jamaah untuk kamar quad (ber-4). Harga kamar triple dan double ada di bawah setiap kartu. Tekan tombol WhatsApp di kartu untuk tanya tanggal dan sisa kursi.</p>
    {isi}
    <p class="ehc-note">Harga dapat berubah mengikuti kebijakan Saudi dan kurs (asumsi maks. Rp 17.000/USD). Hotel dapat diganti dengan hotel setaraf bila penuh.</p>
  </div>
</section></div>'''

    # tanpa bagian "paket lain & kantor": menu paket ada di header, daftar kantor ada di footer (permintaan pemilik)
    end = f'''<style>
/* urutan latar harga(putih) layanan(abu) ketentuan(putih) fasilitas(abu) testimoni(putih) */
body .ehc-sec:has(.ehfk){{background:#fff!important}}
#{anchor}{{background:#fff!important}}
</style>'''

    trips = []
    for per, c in cards:
        title = re.search(r'alt="([^"]+)"', c).group(1)
        price = int(re.sub(r'\D', '', re.search(r'<b>(Rp [^<]+)</b>', c).group(1)))
        dates = re.search(r'Berangkat</i><span>([^<]+)</span>', c).group(1).replace('&amp;', '&')
        dur = re.search(r'Durasi</i><span>([^<]+)</span>', c).group(1)
        trips.append({"@type": "TouristTrip", "name": f"{title} ({dur})", "description": f"Keberangkatan {dates}",
                      "provider": {"@type": "TravelAgency", "name": "Elharamain Wisata", "url": SITE},
                      "offers": {"@type": "Offer", "price": price, "priceCurrency": "IDR", "availability": "https://schema.org/InStock",
                                 "url": f"{SITE}{p['slug']}/#{anchor}"}})
    end += f'\n<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": trips}, ensure_ascii=False)}</script>'
    assert '&&' not in top + end, p['key']
    page = '\n\n'.join([ref('gaya'), ref('lebar'), ref('paket'), blk(top), ref('layanan'), ref('ketentuan'), ref('fasilitas'), ref('testimoni'), blk(end)])
    open(HERE + f"halaman/{p['key']}.html", 'w').write(page)
    print(p['key'], p['id'], len(page), len(cards), [f'{q}: {re.search(r"tag [a-z]+.>([^<]+)", c).group(1)}' for q, c in cards])


if __name__ == '__main__':
    os.makedirs(HERE + 'halaman', exist_ok=True)
    gaya = '<style>.ehpk .per{display:block;font:700 11px Poppins,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}.ehpk .wa-kartu{margin-top:16px;width:100%}.ehpk-per{font:700 1.25rem Poppins,sans-serif;text-align:center;margin:36px 0 18px}</style>'
    open(POLA_PAKET, 'w').write(blk(css + gaya + SCRIPT))
    for p in PAGES:
        bangun(p)
