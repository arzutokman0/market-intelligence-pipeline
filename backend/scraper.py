import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

def fetch_job_listings(search_query):
    print(f"👻 Undetected browser initializing... Searching for '{search_query}' on Upwork.")
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=149) 
    
    url = f"https://www.upwork.com/nx/search/jobs/?q={search_query.replace(' ', '%20')}"
    jobs_data = []
    
    try:
        driver.get(url)
        print("⏳ Waiting for Cloudflare and job listings to load (15 seconds)...")
        time.sleep(15) # Sayfanın tam yüklenmesi için süreyi biraz uzattık
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        print("🔍 Extracting job listings from the page...")
        
        # Olası tüm başlık etiketlerini buluyoruz (Upwork ilan başlıkları genelde bunlardadır)
        headers = soup.find_all(['h2', 'h3', 'h4', 'h5'])
        
        for header in headers:
            title = header.get_text(strip=True)
            # Eğer başlık çok kısaysa veya içinde link yoksa bu bir iş ilanı değildir
            if len(title) > 5 and header.find('a'): 
                # Başlığın bulunduğu kapsayıcı kutuyu bul
                parent = header.find_parent('article') or header.find_parent('section') or header.find_parent('div', class_=lambda c: c and 'job' in c.lower())
                
                description = "Description not found."
                if parent:
                    # Kutu içindeki paragrafları veya span'leri tarayıp uzun metni (açıklamayı) bul
                    desc_tags = parent.find_all(['span', 'p'])
                    for tag in desc_tags:
                        text = tag.get_text(separator=" ", strip=True)
                        if len(text) > 50: 
                            description = text[:300] + "..."
                            break
                
                # Aynı ilanı iki kez eklememek için kontrol et
                if title not in [j['title'] for j in jobs_data]: 
                    jobs_data.append({"title": title, "description": description})
        
        # Eğer hala 0 ilan buluyorsa HTML'i incelemek için bir dosyaya kaydet
        if len(jobs_data) == 0:
            print("⚠️ Could not parse jobs. Saving the page source to 'debug.html' to inspect...")
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(html)
                
        print(f"✅ Successfully extracted {len(jobs_data)} job listings!")
        
        print("-" * 50)
        for idx, job in enumerate(jobs_data, 1):
            print(f"{idx}. {job['title']}")
            print(f"   Details: {job['description'][:100]}...\n")
        print("-" * 50)
        
        return jobs_data
        
    except Exception as e:
        print(f"❌ Scraper error: {e}")
        return None
    finally:
        try:
            driver.quit()
        except OSError:
            pass

if __name__ == "__main__":
    fetch_job_listings("python data extraction")