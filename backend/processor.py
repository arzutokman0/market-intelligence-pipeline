from google import genai

def extract_skills_with_gemini(job_description):
    # Elindeki anahtarı tırnak işaretlerinin içine yapıştır
    api_key = os.getenv("GEMINI_API_KEY")
    
  # Yeni kütüphanenin istemci (client) yapısı
    client = genai.Client(api_key=api_key)
    
    print("Gemini API'ye bağlanılıyor ve analiz yapılıyor...")
    
    try:
        prompt = f"""Analyze the following job descriptions and extract the most in-demand technical skills, tools, and technologies. 
Return the result strictly in English as a clean, comma-separated list. Do not use extra sentences.

Job Listings:
{job_description}"""
        
        # Yeni kütüphanede generate_content kullanımı
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        return response.text
    except Exception as e:
        return f"API Hatası Oluştu: {e}"