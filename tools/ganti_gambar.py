"""Ganti gambar Cloudinary (akun v6gwkqrb dinonaktifkan, 23 Okt 2026) dengan gambar di Media WordPress.
Sumber gambar: Canva (salinan desain "web" DAHYz54LrZM, brosur Januari/Desember/Ramadhan, desain "Perlengkapan").
Jalankan: python3 tools/ganti_gambar.py   → mengubah file pattern & halaman paket di tempat."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../'
UP = 'https://elharamainwisata.com/wp-content/uploads/2026/10/'

# kartu paket: foto rombongan per kelas (1400x1000), dipilih dari alt kartu
FOTO = {'bronze': 'foto-paket-bronze', 'silver': 'foto-paket-silver', 'silver12': 'foto-paket-silver-12',
        'platinum': 'foto-paket-platinum', 'premium': 'foto-paket-premium'}


def kelas(alt):
    a = alt.lower()
    if 'bronze' in a: return 'bronze'
    if 'premium' in a: return 'premium'
    if 'platinum' in a: return 'platinum'
    if '12 hari' in a or 'gold' in a: return 'silver12'
    return 'silver'


def kartu(m):
    tag = m.group(0)
    alt = re.search(r'alt="([^"]*)"', tag).group(1)
    return re.sub(r'src="https://res\.cloudinary\.com/[^"]+"', f'src="{UP}{FOTO[kelas(alt)]}-768x549.jpg"', tag)


def hotel(m):
    # nama file hotel di Media WordPress diberi akhiran -1 (nama lama sudah terpakai)
    base = UP + m.group(1) + '-1'
    return (f'src="{base}-768x399.jpg" srcset="{base}-300x156.jpg 300w, {base}-768x399.jpg 768w, {base}.jpg 1000w"')


def perlengkapan(m):
    base = UP + m.group(1) + '-2026'
    return (f'src="{base}-1536x864.jpg" srcset="{base}-768x432.jpg 768w, {base}-1536x864.jpg 1536w, {base}.jpg 2560w"')


# kolase hotel (gedung + 2 foto kamar), dibuat dari foto situs resmi hotel & halaman fasilitas brosur Canva
KOLASE = ['anjum', 'prestige', 'marwa-rotana', 'movenpick-hajar', 'fairmont', 'al-shohada', 'royal-majestic',
          'al-aqeeq', 'peninsula-worth', 'movenpick-madinah', 'royal-andalus']

CLD = r'https://res\.cloudinary\.com/v6gwkqrb/image/upload/[^"\s)]*?/'


def ganti(s):
    s = re.sub(r'<img [^>]*kartu-paket-\d+\.jpg[^>]*>', kartu, s)
    s = re.sub(r'src="' + CLD + r'(fasilitas-(?:hotel-[a-z-]+|bus))\.jpg" srcset="[^"]*"', hotel, s)
    s = re.sub(r'src="' + CLD + r'(perlengkapan-(?:pria|wanita))-2026(?:-a)?\.png" srcset="[^"]*"', perlengkapan, s)
    s = re.sub(r'href="' + CLD + r'(perlengkapan-(?:pria|wanita))-2026(?:-a)?\.png"', lambda m: f'href="{UP}{m.group(1)}-2026.jpg"', s)
    s = re.sub(CLD + r'1\.jpg', UP + 'hero-jamaah-kabah.jpg', s)
    for h in KOLASE:
        s = s.replace(f'fasilitas-hotel-{h}-1', f'kolase-hotel-{h}')
    return s


FILES = ['halaman-kota/pattern/9991-gaya.html', 'halaman-kota/pattern/9995-perlengkapan-hotel-dokumentasi.html',
         'halaman-kota/pattern/9996-paket-harga.html']
if __name__ == '__main__':
    for f in FILES:
        p = ROOT + f
        s = open(p).read()
        t = ganti(s)
        open(p, 'w').write(t)
        print(f, 'cloudinary tersisa:', t.count('cloudinary'))
