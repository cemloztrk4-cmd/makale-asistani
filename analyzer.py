import parser

def analiz_istegi_olustur(makale, yorumlar):
    """
    Hakem yorumlarını ve makaleyi yapay zekanın hem rapor (DOSYA C) 
    hem de revize metin (DOSYA B) üreteceği net bir komut formatına çevirir.
    """
    istek_metni = f"""
    Sen uzman bir akademik editör ve metin mühendisisin.
    Aşağıda sana bir ana metin (DOSYA B) ve bu metinle ilgili yapılması istenen hakem değerlendirmeleri / düzeltmeler (DOSYA A) verilmiştir.

    --- DOSYA A (HAKEM YORUMLARI) ---
    {yorumlar}

    --- DOSYA B (MAKALE/ANA METİN) ---
    {makale}

    Görevlerin:
    1. DOSYA A'daki yorumları analiz et ve DOSYA B'de hangi kısımların değiştirilmesi gerektiğini maddeler halinde akademik bir dille raporla (Bu kısım DOSYA C raporu olacaktır).
    2. Hakem yorumlarındaki direktifleri birebir uygulayarak DOSYA B'nin güncellenmiş, revize edilmiş tam halini oluştur (Bu kısım Güncellenmiş DOSYA B olacaktır).

    Lütfen yanıtını tam olarak şu iki etiket arasına yazarak yapılandır:

    [RAPOR_BASLANGICI]
    (Buraya DOSYA C için hazırladığın detaylı analiz, eleştiri ve revizyon planı raporunu yaz)
    [RAPOR_BITISI]

    [METIN_BASLANGICI]
    (Buraya hakem yorumlarına göre baştan sona güncellenmiş ve düzeltilmiş DOSYA B makale metninin tam halini yaz)
    [METIN_BITISI]
    """
    return istek_metni

if __name__ == "__main__":
    # 1. Adım: Parser modülümüzü kullanarak dosyaları okuyalım
    makale_metni = parser.metin_dosyasi_oku("makale.txt")
    yorum_metni = parser.metin_dosyasi_oku("hakem_yorumlari.txt")
    
    # 2. Adım: Okunan metinleri yapay zeka için formatlayalım
    hazir_prompt = analiz_istegi_olustur(makale_metni, yorum_metni)
    
    print("=== YAPAY ZEKA İÇİN HAZIRLANAN GÖREV EMRİ ===")
    print(hazir_prompt)