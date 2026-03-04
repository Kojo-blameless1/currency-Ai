import urllib.request
import urllib.parse
import json
import os
import re
from pathlib import Path

CURRENCIES = {
    'USD': ['1 dollar bill', '20 dollar bill', '100 dollar bill'],
    'EUR': ['5 euro note', '20 euro note', '50 euro banknote'],
    'GBP': ['5 pound note', '20 pound note', '50 pound note'],
    'INR': ['100 rupee note', '500 rupee note', 'indian rupee banknote'],
    'JPY': ['1000 yen note', '5000 yen note', '10000 yen note'],
    'AUD': ['10 australian dollar note', '50 australian dollar note'],
    'CAD': ['10 canadian dollar note', '20 canadian dollar note'],
    'BRL': ['10 real note brazil', '50 real note brazil'],
    'NZD': ['10 new zealand dollar', '50 nzd banknote'],
    'SGD': ['10 singapore dollar', '50 singapore dollar note'],
    'GHS': ['5 cedi note ghana', '20 cedi note ghana', '50 cedi ghana'],
    'NGN': ['200 naira note', '500 naira note', '1000 naira note'],
}

TARGET = 150

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
        print(f"    Search error: {e}")
    return urls[:max_results]

for currency, queries in CURRENCIES.items():
    save_dir = Path(f'data/raw/images/{currency}')
    save_dir.mkdir(parents=True, exist_ok=True)
    
    current = len(list(save_dir.iterdir()))
    print(f"\n📥 {currency}: currently {current} images")
    
    if current >= TARGET:
        print(f"✅ Already at target!")
        continue

    count = current
    for query in queries:
        if count >= TARGET:
            break
        print(f"  Searching: {query}")
        urls = search_bing_images(query)
        print(f"  Found {len(urls)} urls")
        for url in urls:
            if count >= TARGET:
                break
            filepath = save_dir / f'img_{count:04d}.jpg'
            if download_image(url, filepath):
                count += 1

    print(f"✅ {currency}: {count} images total")

print("\nAll done! 🎉")