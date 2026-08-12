import parser
import analyzer
import os
import requests

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
load_dotenv()
# Şifremiz ve adresimiz aynı, kusursuz çalışıyor
api_sifresi = os.environ["GEMINI_API_KEY"]

def bot_cevabini_al(prompt):
    """
    Doğrudan Google'a bağlanır, gelen cevabı okur ve analyzer.py'daki 
    etiketlere göre rapor ve metni makas gibi keserek birbirinden ayırır.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_sifresi}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        gelen_metin = response.json()['candidates'][0]['content']['parts'][0]['text']
        
        # --- AKILLI AYIKLAMA (PARSING) BÖLÜMÜ ---
        try:
            # Gelen metni [RAPOR_BASLANGICI] ve [RAPOR_BITISI] arasından kesiyoruz
            rapor_kismi = gelen_metin.split("[RAPOR_BASLANGICI]")[1].split("[RAPOR_BITISI]")[0].strip()
            
            # Gelen metni [METIN_BASLANGICI] ve [METIN_BITISI] arasından kesiyoruz
            metin_kismi = gelen_metin.split("[METIN_BASLANGICI]")[1].split("[METIN_BITISI]")[0].strip()
            
            return {
                "dosya_c_raporu": rapor_kismi,
                "yeni_makale": metin_kismi
            }
        except IndexError:
            # Eğer yapay zeka bir anlık hatayla etiketleri koymayı unutursa diye sigorta
            return {
                "dosya_c_raporu": "HATA: Yapay zeka etiketleri düzgün oluşturamadı.\n\nTam Cevap:\n" + gelen_metin,
                "yeni_makale": "HATA: Yapay zeka metin etiketlerini düzgün oluşturamadı."
            }
    else:
        return {
            "dosya_c_raporu": f"BAĞLANTI HATASI ({response.status_code})",
            "yeni_makale": response.text
        }

def ciktilari_kaydet(rapor, yeni_metin):
    """Üretilen yeni metinleri 'ciktilar' klasörüne kaydeder."""
    os.makedirs("ciktilar", exist_ok=True)
    
    with open(os.path.join("ciktilar", "DOSYA_C_Rapor.txt"), "w", encoding="utf-8") as f:
        f.write(rapor)
        
    with open(os.path.join("ciktilar", "Guncellenmis_DOSYA_B.txt"), "w", encoding="utf-8") as f:
        f.write(yeni_metin)
    
    print("\n✅ İŞLEM TAMAMLANDI! Akıllı ayıklama yapıldı ve dosyalar başarıyla klasöre kaydedildi.")

if __name__ == "__main__":
    makale = parser.metin_dosyasi_oku("makale.txt")
    yorumlar = parser.metin_dosyasi_oku("hakem_yorumlari.txt")
    
    hazir_prompt = analyzer.analiz_istegi_olustur(makale, yorumlar)
    
    print("Google Gemini metinleri inceliyor ve etiketlere göre ayırıyor...")
    cevap = bot_cevabini_al(hazir_prompt)
    
    ciktilari_kaydet(cevap["dosya_c_raporu"], cevap["yeni_makale"])