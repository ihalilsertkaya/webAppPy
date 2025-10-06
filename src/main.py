import os
import json
import requests
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

# Appwrite İstemcisini Başlatma
client = Client()
(
    client
    .set_endpoint(os.environ.get('APPWRITE_ENDPOINT')) # Örneğin: https://cloud.appwrite.io/v1
    .set_project(os.environ.get('APPWRITE_FUNCTION_PROJECT_ID'))
    .set_key(os.environ.get('APPWRITE_API_KEY'))
)
databases = Databases(client)

DATABASE_ID = os.environ.get('APPWRITE_DATABASE_ID')
PENDING_COLLECTION_ID = os.environ.get('PENDING_COLLECTION_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Basit Web Scraping Simülasyonu
def scrape_campaigns():
    # Normalde burada BeautifulSoup veya Scrapy kullanılır.
    # Örnek için sabit bir veri döndürüyoruz.
    return [
        {"raw": "Akbank'tan Opet'te 500 TL ve üzeri akaryakıt alımına 50 TL indirim! Son gün 30.11.2025.", "source": "Akbank"},
        {"raw": "Trendyol Cuma indirimleri başladı! Giyim alışverişlerinde %10 indirim kuponu kazanma şansı.", "source": "Trendyol"},
    ]

# AI Analizi Fonksiyonu (ChatGPT simülasyonu)
def analyze_with_ai(raw_text):
    # Gerçek hayatta OpenAI veya Gemini API çağrısı buraya gelir.
    # Örnek amaçlı, anahtar kelimeye göre etiketleme yapıyoruz.
    
    if "Opet" in raw_text or "akaryakıt" in raw_text:
        category = "Akaryakıt"
        title = raw_text.split('.')[0] 
    elif "Trendyol" in raw_text or "giyim" in raw_text:
        category = "Giyim"
        title = raw_text.split('!')[0]
    else:
        category = "Diğer"
        title = raw_text[:50] + "..."
        
    return {"title": title, "category": category}

def main(context):
    campaigns = scrape_campaigns()
    
    for campaign in campaigns:
        # 1. AI Analizi
        analysis_result = analyze_with_ai(campaign['raw'])
        
        # 2. Onay Bekleyenler Koleksiyonuna Kayıt
        try:
            databases.create_document(
                database_id=DATABASE_ID,
                collection_id=PENDING_COLLECTION_ID,
                document_id=ID.unique(),
                data={
                    "title": analysis_result["title"],
                    "category": analysis_result["category"],
                    "status": "pending",
                    "raw_data": campaign['raw']
                }
            )
            context.log(f"Kampanya kaydedildi: {analysis_result['title']}")
        except Exception as e:
            context.log(f"Hata oluştu: {e}")
            
    return context.res.json({"status": "success", "message": "Scraping ve analiz tamamlandı."})