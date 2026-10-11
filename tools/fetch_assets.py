"""Optional asset maintenance. Only downloads the explicitly reviewed Commons files."""
import html
import io
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    'damascus': 'The Umayyad Mosque, Courtyard, Damascus, Syria.jpg',
    'aleppo': 'Citadel of Aleppo.jpg',
    'homs': 'Homs mosque 3042.jpg',
    'hama': 'Noria of Hama, Hama, Syria.jpg',
    'latakia': 'Fishing boats off the coast of Ibn Hani near Latakia, Syria.jpg',
    'tartus': 'Sunset over the sea in Tartus Syria.jpg',
    'deir-ez-zor': 'Deir Ez-Zor Euphrates 9910.jpg',
    'palmyra': 'Palmyra, Syria, Colonnade at Palmyra.jpg',
    'bosra': 'Bosra theatre cavea 0559b.jpg',
    'maaloula': 'Maaloula 01.jpg',
    'kibbeh': 'Kibbeh3.jpg',
    'fattoush': 'Fattoush 1.JPG',
    'falafel': 'Falafel 1.JPG',
    'shawarma': 'Shawarma-Kebab stand in central Aleppo, Syria.jpg',
    'halawet-el-jibn': 'Hama حلاوة الجبن Halawat al-jibn 8611.jpg',
}
HEADER = {'User-Agent': 'SyriaFun/1.0 (https://github.com/abderlahmanalhnedi/syria.fun)'}

def download(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADER), timeout=60).read()

def photographs(only=None):
    media_path=ROOT/'assets/data/media.json'
    media = json.loads(media_path.read_text(encoding='utf-8')) if only and media_path.exists() else {}
    folder = ROOT / 'assets/images'
    folder.mkdir(parents=True, exist_ok=True)
    for key, title in FILES.items():
        if only and key not in only: continue
        params = dict(action='query', format='json', titles='File:'+title, prop='imageinfo', iiprop='url|extmetadata')
        data = json.loads(download('https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode(params)))
        info = next(iter(data['query']['pages'].values()))['imageinfo'][0]
        m = info['extmetadata']
        plain = lambda k: html.unescape(re.sub('<[^>]+>', '', m.get(k, {}).get('value', ''))).strip()
        license_name = plain('LicenseShortName')
        if not license_name.startswith(('CC BY', 'CC0')):
            raise ValueError('Review license before downloading: '+title)
        original = Image.open(io.BytesIO(download(info['url'].split('?')[0])))
        im = ImageOps.exif_transpose(original).convert('RGB')
        for width in (640, 1600):
            copy = im.copy()
            copy.thumbnail((width, width))
            copy.save(folder/f'{key}-{width}.webp', 'WEBP', quality=82, method=6)
        if key=='damascus':
            ImageOps.fit(im,(720,1080),method=Image.Resampling.LANCZOS,centering=(.55,.5)).save(folder/'damascus-hero-mobile.webp','WEBP',quality=78,method=6)
        raw_date=plain('DateTimeOriginal')
        capture_date=raw_date[:10] if re.match(r'^\d{4}-\d{2}-\d{2}',raw_date) else ''
        media[key] = dict(file=f'assets/images/{key}-640.webp', large=f'assets/images/{key}-1600.webp', source=info['descriptionurl'], author=plain('Artist'), license=license_name, license_url=plain('LicenseUrl').replace('http:', 'https:'), date=capture_date, source_date=raw_date, description=plain('ImageDescription'), type='photo')
        print('Verified and optimized:', key, license_name)
    (ROOT/'assets/data/media.json').write_text(json.dumps(media, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def fonts():
    folder = ROOT/'assets/fonts'
    folder.mkdir(parents=True, exist_ok=True)
    url = 'https://fonts.googleapis.com/css2?family=Cairo:wght@400..800&family=Inter:wght@400..700&display=swap'
    modern = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
    css = urllib.request.urlopen(urllib.request.Request(url, headers=modern), timeout=60).read().decode()
    # Keep Arabic and Latin scripts used by this edition; no unused script subsets.
    blocks = re.findall(r'/\* ([^*]+) \*/\s*(@font-face\s*\{[^}]+\})', css)
    if blocks:
        css = '\n\n'.join(block for subset, block in blocks if ('Cairo' in block and subset=='arabic') or ('Inter' in block and subset in ('latin', 'latin-ext')))
    # Google's response may repeat a font for each weight. Keep distinct files only.
    urls = list(dict.fromkeys(re.findall(r'url\((https://[^)]+)\)', css)))
    for i, font_url in enumerate(urls):
        ext = font_url.split('?')[0].rsplit('.',1)[1]
        name = f'font-{i}.{ext}'
        (folder/name).write_bytes(download(font_url))
        css = css.replace(font_url, '../fonts/'+name)
    (ROOT/'assets/css').mkdir(parents=True, exist_ok=True)
    (ROOT/'assets/css/fonts.css').write_text(css, encoding='utf-8')
    for family in ('cairo', 'inter'):
        (folder/f'{family}-OFL.txt').write_bytes(download(f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/OFL.txt'))
    print('Self-hosted font files:', len(urls))

if __name__ == '__main__':
    photographs()
    fonts()
