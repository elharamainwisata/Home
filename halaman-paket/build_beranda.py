"""Calon pengganti beranda (halaman terpisah; beranda asli page 7840 TIDAK diubah sampai pemilik setuju).
Jalankan: python3 halaman-paket/build_beranda.py  → menulis halaman-paket/halaman/beranda-baru.html
Bagian paket = kartu paket Musim Dingin (Januari & Ramadhan) dari pattern 9996, sama seperti /paket-umroh-musim-dingin/."""
import json, re
from build_paket import HERE, SITE, SEMUA, label, wa, WA_SVG, blk, ref

PERIODE = ['Januari 2027', 'Ramadhan 2027']
cards = [(per, c) for per, k, n, c in SEMUA if per in PERIODE]

# pembimbing ibadah (foto dari beranda lama, Media WordPress 2025/03)
UP = 'https://elharamainwisata.com/wp-content/uploads/2025/03/'
USTADZ = [('12-5', 'Ust. Ahmad Shobirin, Lc., MA'), ('11-5', 'Ust. Dr. Muhammad Tahir, Lc., MA'),
          ('10-9', 'Ust. Didi Wibawa, Lc., MA'), ('9-9', 'Ust. Furqon Abdurrohman, Lc., MA'),
          ('8-8', 'Ust. Ahmad Husain, Lc., M.Pd'), ('7-5', 'Ust. Idrus Abidin, Lc., MA'),
          ('13-5', 'Ust. Zulfahmi Yusuf, S.Pd.I'), ('6-5', 'Ust. Ade Abu Yusuf, Lc.')]

paket = ''.join(f'''
    <h3 class="ehpk-per">{per}</h3>
    <div class="ehpk"><div class="grid">
{chr(10).join(label(q, c) for q, c in cards if q == per)}
    </div></div>''' for per in PERIODE)

top = f'''<div class="ehc"><section class="ehc-hero solo">
  <div class="ehc-wrap">
    <div>
      <span class="ehc-eyebrow">Umroh &amp; Haji Plus · resmi Kemenag</span>
      <h1>Umroh dan Haji Plus yang <em>Nyaman dan Berkesan</em></h1>
      <p>Hotel bintang 5, penerbangan langsung, kereta cepat Haramain, dan bimbingan ibadah sesuai sunnah bersama asatidz lulusan Timur Tengah. Kantor di Bekasi, Jakarta, Depok, Tangerang, Bogor, dan Bandung.</p>
      <div class="ehc-ctas">
        <a class="ehc-btn wa" href="{wa("Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi paket umroh.")}" target="_blank" rel="noopener">{WA_SVG} Konsultasi Gratis</a>
        <a class="ehc-btn ghost" href="#paket-umroh">Lihat paket umroh</a>
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
<section class="ehc-sec" id="paket-umroh">
  <div class="ehc-wrap">
    <span class="ehc-eyebrow">Paket umroh musim dingin</span>
    <h2>Paket umroh Januari &amp; Ramadhan 2027</h2>
    <p class="ehc-lead">Harga per jamaah untuk kamar quad (ber-4). Harga kamar triple dan double ada di bawah setiap kartu. Tekan tombol WhatsApp di kartu untuk tanya tanggal dan sisa kursi.</p>{paket}
    <p class="ehc-note">Harga dapat berubah mengikuti kebijakan Saudi dan kurs (asumsi maks. Rp 17.000/USD). Hotel dapat diganti dengan hotel setaraf bila penuh.</p>
  </div>
</section></div>'''

mid = f'''<div class="ehc"><section class="ehc-sec" id="pembimbing">
  <div class="ehc-wrap">
    <span class="ehc-eyebrow">Lulusan terbaik Timur Tengah</span>
    <h2>Pembimbing ibadah umroh &amp; haji</h2>
    <p class="ehc-lead">Ibadah dibimbing langsung oleh asatidz yang mendampingi jamaah dari manasik sampai pulang ke tanah air.</p>
    <div class="ehb-ust">{"".join(f'<figure><img loading="lazy" src="{UP}{f}.jpg" alt="{n}, pembimbing ibadah Elharamain Wisata"><figcaption>{n}</figcaption></figure>' for f, n in USTADZ)}</div>
  </div>
</section>
<section class="ehc-sec" id="haji-plus">
  <div class="ehc-wrap ehb-haji">
    <div>
      <span class="ehc-eyebrow">Haji khusus resmi</span>
      <h2>Haji Plus 1448 H / 2027</h2>
      <p>Elharamain Wisata adalah penyelenggara haji khusus (PIHK) dengan izin SK Kemenag No. 846/2020. Lihat program, fasilitas, dan cara mendaftar porsi Haji Plus.</p>
    </div>
    <div class="ehc-ctas">
      <a class="ehc-btn pri" href="{SITE}haji/">Lihat paket Haji Plus</a>
      <a class="ehc-btn wa" href="{wa("Assalamu'alaikum Elharamain Wisata, saya ingin konsultasi Haji Plus.")}" target="_blank" rel="noopener">{WA_SVG} Tanya Haji Plus</a>
    </div>
  </div>
</section></div>
<style>
.ehb-ust{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:28px}}
.ehb-ust figure{{margin:0;background:#fff;border:1px solid #e6e8ee;border-radius:14px;overflow:hidden;text-align:center}}
.ehb-ust img{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}}
.ehb-ust figcaption{{padding:12px 10px;font:600 14px Poppins,sans-serif;color:#1d2433}}
.ehb-haji{{display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap}}
.ehb-haji>div:first-child{{max-width:640px}}
.ehb-haji .ehc-ctas{{flex:0 1 auto}}
.ehb-haji .ehc-btn{{width:auto}}
@media (max-width:900px){{.ehb-ust{{grid-template-columns:repeat(2,1fr)}}}}
@media (max-width:640px){{.ehb-haji .ehc-ctas{{flex:1 1 100%}}.ehb-haji .ehc-btn{{width:100%}}}}
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
                             "url": f"{SITE}paket-umroh-musim-dingin/"}})
end = f'''<style>
/* urutan latar: paket(putih) pembimbing(abu) haji(putih) layanan(abu) ketentuan(putih) fasilitas(abu) testimoni(putih) */
body .ehc-sec:has(.ehfk){{background:#fff!important}}
#paket-umroh,#haji-plus{{background:#fff!important}}
#pembimbing{{background:var(--soft)!important}}
</style>
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": trips}, ensure_ascii=False)}</script>'''

assert '&&' not in top + mid + end
page = '\n\n'.join([ref('gaya'), ref('lebar'), ref('paket'), blk(top), blk(mid), ref('layanan'), ref('ketentuan'),
                    ref('fasilitas'), ref('testimoni'), blk(end)])
open(HERE + 'halaman/beranda-baru.html', 'w').write(page)
print('beranda-baru', len(page), len(cards))
