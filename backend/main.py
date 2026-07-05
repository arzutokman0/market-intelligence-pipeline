from scraper import fetch_job_listings
from processor import extract_skills_with_gemini

def run_pipeline():
    # Hangi kelimeyi arayacağımızı belirliyoruz
    search_term = "python data extraction"
    
    print("🚀 Market-Intelligence-Pipeline Başlatılıyor...")
    print(f"Hedef: Upwork üzerinde '{search_term}' araması yapılıp yetenekler analiz edilecek.\n")
    
    # --------------------------------------------------
    # 1. AŞAMA: VERİ KAZIMA (Scraping)
    # --------------------------------------------------
    print("--- [AŞAMA 1: VERİ KAZIMA] ---")
    jobs = fetch_job_listings(search_term)
    
    if not jobs:
        print("❌ İlan bulunamadı veya kazıma başarısız oldu. Program durduruluyor.")
        return
        
    # Gemini'ye göndermek üzere tüm ilanları tek bir uzun metinde birleştiriyoruz
    all_jobs_text = "İŞ İLANLARI LİSTESİ:\n\n"
    for idx, job in enumerate(jobs, 1):
        all_jobs_text += f"İlan {idx} Başlığı: {job['title']}\n"
        all_jobs_text += f"İlan {idx} Detayı: {job['description']}\n\n"
        
    # --------------------------------------------------
    # 2. AŞAMA: YAPAY ZEKA ANALİZİ (Gemini)
    # --------------------------------------------------
    print("\n--- [AŞAMA 2: YAPAY ZEKA ANALİZİ] ---")
    print("Gemini API'ye tüm ilanlar gönderiliyor, veriler analiz ediliyor...")
    
    # Birleştirilmiş ilan metnini processor'a (Gemini'ye) yolluyoruz
    sonuc = extract_skills_with_gemini(all_jobs_text)
    
    # --------------------------------------------------
    # 3. AŞAMA: SONUÇ
    # --------------------------------------------------
    print("\n" + "=" * 50)
    print("🌟 PİYASA ANALİZİ SONUCU (İstenen Yetenekler):")
    print("=" * 50)
    print(sonuc)
    print("=" * 50)

if __name__ == "__main__":
    run_pipeline()