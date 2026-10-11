"""Inspect Wikimedia licensing before selecting photographs; not used by the site."""
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

QUERIES = ['Palmyra columns panorama', 'Hama norias', 'Damascus Umayyad Mosque courtyard', 'Aleppo citadel', 'Latakia coast', 'Tartus old city', 'Deir ez Zor Euphrates', 'Bosra theatre', 'Maaloula village', 'Kibbeh dish', 'Fattoush', 'Baklava']

def inspect(query):
    params = dict(action='query', format='json', generator='search', gsrsearch=query+' filetype:bitmap', gsrnamespace=6, gsrlimit=4, prop='imageinfo', iiprop='url|extmetadata', iiurlwidth=1600)
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'SyriaFun/1.0 (https://github.com/abderlahmanalhnedi/syria.fun)'})
        data = json.load(urllib.request.urlopen(req, timeout=30))
        out = []
        for page in data.get('query', {}).get('pages', {}).values():
            info = page.get('imageinfo', [{}])[0]
            m = info.get('extmetadata', {})
            plain = lambda key: re.sub('<[^>]+>', '', m.get(key, {}).get('value', ''))
            out.append(dict(title=page['title'], license=plain('LicenseShortName'), author=plain('Artist'), date=plain('DateTimeOriginal'), description=plain('ImageDescription')[:450], url=info.get('url'), thumb=info.get('thumburl'), source=info.get('descriptionurl'), license_url=plain('LicenseUrl')))
        return {'query': query, 'candidates': out}
    except Exception as e:
        return {'query': query, 'error': str(e)}

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(inspect, QUERIES):
            print(json.dumps(result, ensure_ascii=True))
