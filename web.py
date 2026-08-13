# pyrefly: ignore [missing-import]
import streamlit as st
import analyzer
import editor

# Sayfa ayarları (Geniş ekran, sekme başlığı ve ikon)
st.set_page_config(page_title="Makale Asistanı - Web", page_icon="🤖", layout="wide")

# Sadece Fork ve GitHub ikonunu gizler, 3 nokta menüsü yerinde kalır
gizle_kalabalik = """
    <style>
    .stAppDeployButton {display: none !important;}
    </style>
"""
st.markdown(gizle_kalabalik, unsafe_allow_html=True)


# Başlık ve Açıklama
st.title("🤖 Yapay Zeka Makale Editörü")
st.markdown("DOSYA A (Hakem Yorumları) ve DOSYA B (Ana Metin) okunarak **Gemini 3.5 Flash** modeli ile analiz edilecektir.")
st.divider() # Araya şık ve ince bir çizgi çekiyoruz

# Ekranı iki kolona bölüyoruz (Sol panel girdiler, Sağ panel çıktılar)
sol_kolon, sag_kolon = st.columns(2)

with sol_kolon:
    st.subheader("📝 Girdi Alanı")
    makale_metni = st.text_area("Ana Metin (DOSYA B):", height=250, placeholder="Düzeltilecek makale metnini buraya yapıştırın...")
    yorum_metni = st.text_area("Hakem Yorumları (DOSYA A):", height=150, placeholder="Hakemin düzeltme taleplerini buraya yapıştırın...")
    
    # Buton oluşturuyoruz (Genişliği kolona tam sığacak şekilde ayarladık)
    analiz_butonu = st.button("🚀 Analizi Başlat", use_container_width=True, type="primary")

with sag_kolon:
    st.subheader("📊 Çıktı Alanı")
    
    # Eğer butona basılırsa çalışacak işlemler
    if analiz_butonu:
        if not makale_metni or not yorum_metni:
            st.warning("⚠️ Lütfen analizi başlatmadan önce her iki metin kutusunu da doldurun!")
        else:
            # Ekranda şık bir yükleniyor animasyonu gösteriyoruz
            with st.spinner('Google Gemini sunucularına bağlanılıyor ve metin analiz ediliyor. Lütfen bekleyin...'):
                try:
                    # 1. Görev emrini oluştur
                    hazir_prompt = analyzer.analiz_istegi_olustur(makale_metni, yorum_metni)
                    
                    # 2. Google'a gönder ve cevabı al
                    cevap = editor.bot_cevabini_al(hazir_prompt)
                    
                    # 3. Klasöre yedekle (Eski sistemimiz çalışmaya devam etsin)
                    editor.ciktilari_kaydet(cevap["dosya_c_raporu"], cevap["yeni_makale"])
                    
                    # 4. Sonuçları ekrana yazdır
                    st.success("✅ İşlem Başarılı! Çıktılar aşağıya yazdırıldı ve klasöre yedeklendi.")
                    
                    st.text_area("Yapay Zeka Raporu (DOSYA C):", value=cevap["dosya_c_raporu"], height=200)
                    st.text_area("Güncellenmiş Metin (Revize DOSYA B):", value=cevap["yeni_makale"], height=250)
                except Exception as hata:
                    st.error(f"❌ Bir hata oluştu: {str(hata)}")
    else:
        st.info("Sonuçları görmek için sol taraftan metinleri girip 'Analizi Başlat' butonuna tıklayın.")
