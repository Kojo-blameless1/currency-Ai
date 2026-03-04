from icrawler.builtin import BingImageCrawler
import os

# Different search terms to get more variety
EXTRA_SEARCHES = {
    'USD': ['american dollar note', 'federal reserve note', 'greenback dollar'],
    'EUR': ['european union banknote', 'euro paper money', 'euro bill currency'],
    'GBP': ['england pound note', 'sterling banknote', 'bank of england note'],
    'INR': ['reserve bank of india note', 'india paper money', 'rupee currency note'],
    'JPY': ['bank of japan note', 'japan paper money', 'yen currency bill'],
    'AUD': ['reserve bank australia note', 'australia paper money', 'aussie dollar note'],
    'CAD': ['canada paper money', 'canadian banknote', 'bank of canada note'],
    'BRL': ['brazil paper money', 'real brasileiro', 'banco central brasil note'],
    'NZD': ['new zealand paper money', 'kiwi dollar note', 'reserve bank nz note'],
    'SGD': ['singapore paper money', 'monetary authority singapore note', 'sing dollar bill'],
    'GHS': ['bank of ghana note', 'ghanaian cedi paper money', 'ghana paper currency'],
    'NGN': ['central bank nigeria note', 'nigerian paper money', 'naira currency bill'],
}

TARGET = 100  # target images per currency

for currency, queries in EXTRA_SEARCHES.items():
    save_dir = f'data/raw/images/{currency}'
    current = len(os.listdir(save_dir))
    
    if current >= TARGET:
        print(f"✅ {currency}: already has {current} images, skipping")
        continue
    
    print(f"\n📥 {currency}: has {current}, downloading more...")
    
    for query in queries:
        current = len(os.listdir(save_dir))
        if current >= TARGET:
            break
        crawler = BingImageCrawler(storage={'root_dir': save_dir})
        crawler.crawl(keyword=query, max_num=50)
    
    final = len(os.listdir(save_dir))
    print(f"✅ {currency}: {final} images total")

print("\nAll done! 🎉")