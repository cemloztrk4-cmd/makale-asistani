import os

def metin_dosyasi_oku(dosya_adi):
    dosya_yolu = os.path.join("girdiler", dosya_adi)
    try:
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            return dosya.read()
    except FileNotFoundError:
        return f"Hata: {dosya_adi} bulunamadı!"

if __name__ == "__main__":
    makale_metni = metin_dosyasi_oku("makale.txt")
    yorum_metni = metin_dosyasi_oku("hakem_yorumlari.txt")
    
    print("--- DOSYA B (MAKALE) ---")
    print(makale_metni)
    
    print("\n--- DOSYA A (HAKEM YORUMLARI) ---")
    print(yorum_metni)