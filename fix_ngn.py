# save as fix_ngn.py
import urllib.request
import urllib.parse
import re
from pathlib import Path

def download_image(url, filepath):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            if len(data) > 5000:
                with open(filepath, 'wb') as f:
                    f.write(data)
                return True
    except:
        pass
    return False

def search_bing_images(query, max_results=50):
    urls = []
    try:
        encoded = urllib.parse.quote(query)
        url = f'https://www.bing.com/images/search?q={encoded}&count={max_results}'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            urls = re.findall(r'murl&quot;:&quot;(https?://[^&]+?)&quot;', html)
            urls += re.findall(r'"murl":"(https?://[^"]+?)"', html)
    except Exception as e:
        print(f"  Error: {e}")
    return urls[:max_results]

save_dir = Path('data/raw/images/NGN')
queries = ['500 naira note', '1000 naira note', 'nigerian naira banknote', 'naira currency note']
count = len(list(save_dir.iterdir()))
print(f"NGN: currently {count} images")

for query in queries:
    if count >= 120:
        break
    print(f"  Searching: {query}")
    urls = search_bing_images(query)
    print(f"  Found {len(urls)} urls")
    for url in urls:
        if count >= 120:
            break
        filepath = save_dir / f'fix_{count:04d}.jpg'
        if download_image(url, filepath):
            count += 1

print(f"✅ NGN: {count} images total")