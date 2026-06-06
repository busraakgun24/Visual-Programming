import sqlite3
import requests

def veri_setini_hazirla():
    print("Dünya ülkeleri veri seti indiriliyor... Lütfen bekleyin.")
    
    # Ücretsiz ve açık kaynaklı ülkeler API'si (Türkçe isim desteği için)
    url = "https://restcountries.com/v3.1/all?fields=name,flags,capital"
    
    try:
        cevap = requests.get(url)
        ulkeler = cevap.json()
    except Exception as e:
        print(f"Hata oluştu, internet bağlantınızı kontrol edin: {e}")
        return

    # Veritabanına bağlanalım
    db = sqlite3.connect("oyun.db")
    cursor = db.cursor()
    
    # Eski test tablosunu uçuralım, temiz bir sayfa açalım
    cursor.execute("DROP TABLE IF EXISTS bayraklar")
    
    # Yeni tablomuzu oluşturalım. Bu sefer resim_adi yerine resim_url tutacağız!
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bayraklar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            resim_url TEXT NOT NULL,
            baskent TEXT DEFAULT 'Belirtilmemiş',
            fail_count INTEGER DEFAULT 0,
            correct_streak INTEGER DEFAULT 0,
            is_learned INTEGER DEFAULT 0
        )
    """)
    
    eklenen_sayisi = 0
    
    for ulke in ulkeler:
        try:
            isim = ulke['name']['translations']['tur']['common']
        except KeyError:
            isim = ulke['name']['common']
            
        # Başkent listesini güvenli bir şekilde string'e çeviriyoruz
        baskent_listesi = ulke.get('capital', [])
        if baskent_listesi and isinstance(baskent_listesi, list):
            baskent = str(baskent_listesi[0]).strip() # Köşeli parantezden kurtarıp temiz metin alıyoruz
        else:
            baskent = 'Belirtilmemiş'
            
        resim_url = ulke['flags']['png']
        
        # Veritabanına temiz veriyi yazıyoruz
        cursor.execute("""INSERT INTO bayraklar (isim, resim_url, baskent, fail_count, correct_streak, is_learned) 
                          VALUES (?, ?, ?, 0, 0, 0)""", (isim, resim_url, baskent))

    db.commit()
    db.close()
    print(f"Muhteşem! Toplam {eklenen_sayisi} ülke ve bayrağı başarıyla veritabanına kaydedildi.")

if __name__ == "__main__":
    veri_setini_hazirla()