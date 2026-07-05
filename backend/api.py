from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import fetch_job_listings
from processor import extract_skills_with_gemini

app = FastAPI(title="Market Intelligence API")

# Tarayıcı (Next.js) üzerinden gelecek isteklere izin veriyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Web sitesinden gelecek isteğin yapısını tanımlıyoruz
class SearchRequest(BaseModel):
    search_term: str

@app.post("/api/analyze")
def analyze_jobs(request: SearchRequest):
    print(f"\n🚀 YENİ İSTEK GELDİ: '{request.search_term}' aranıyor...")
    
    # 1. AŞAMA: Tarayıcıyı Aç ve Veri Kazı (Canlı Şov Kısmı)
    jobs = fetch_job_listings(request.search_term)
    
    if not jobs:
        return {"status": "error", "message": "İlan bulunamadı veya kazıma başarısız oldu."}
        
    # İlanları Gemini'nin anlayacağı bir metne dönüştür
    all_jobs_text = "İŞ İLANLARI LİSTESİ:\n\n"
    for idx, job in enumerate(jobs, 1):
        all_jobs_text += f"İlan {idx} Başlığı: {job['title']}\n"
        all_jobs_text += f"İlan {idx} Detayı: {job['description']}\n\n"
        
    # 2. AŞAMA: Yapay Zeka Analizi
    print("\n🧠 Veriler Gemini API'ye gönderiliyor...")
    sonuc = extract_skills_with_gemini(all_jobs_text)
    
    print("✅ İşlem tamamlandı. Sonuçlar web sitesine gönderiliyor.")
    
    # 3. AŞAMA: Sonucu Web Sitesine (Frontend) Gönder
    return {
        "status": "success",
        "search_term": request.search_term,
        "jobs_count": len(jobs),
        "extracted_skills": sonuc,
        "raw_jobs": jobs # İlanların listesini de ekranda kart olarak göstermek istersek diye gönderiyoruz
    }