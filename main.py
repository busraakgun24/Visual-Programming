import sys
import sqlite3
import random
import urllib.request  # İnternetten resmi anlık çekmek için ekledik
from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize

class BayrakOyunu(QWidget):
    def __init__(self):
        super().__init__()
        
        # 1. ÖNCE DEĞİŞKENLERİ VE HAFIZAYI TANIMLA (Bellekte yer açılsın)
        self.soru_havuzu = []    
        self.yanlis_havuzu = []  
        self.dogru_cevap = None  
        self.oyun_modu = "Bayrak"  # İşte hata veren değişken artık en başta!

        # 2. SONRA SİSTEMLERİ BAŞLAT
        self.init_db()
        self.init_ui()

    def init_db(self):
        """Veritabanına bağlanır."""
        self.db = sqlite3.connect("oyun.db")
        self.cursor = self.db.cursor()

    def init_ui(self):
        """Ana Menü (Dashboard) ve Oyun Arenasını barındıran katman."""
        self.setWindowTitle("Pro Eğitim Platformu - Çoklu Mod")
        self.setFixedSize(450, 650)
        
        # ----------------------------------------------------
        # MERKEZİ SAYFA YÖNETİCİSİ (QStackedWidget)
        # ----------------------------------------------------
        self.sayfa_yoneticisi = QStackedWidget()
        
        # ====================================================
        # SAYFA 0: ANA MENÜ (DASHBOARD) TASARIMI
        # ====================================================
        self.ana_menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setSpacing(20) # Butonların arasındaki boşluk
        
        # Üst Başlık (Görseldeki gibi şık bir karşılama yazısı)
        self.label_baslik = QLabel("Günlük Meydan Okuma\nModunu Seç ve Başla!")
        self.label_baslik.setAlignment(Qt.AlignCenter)
        self.label_baslik.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50; margin: 20px;")
        self.menu_layout.addWidget(self.label_baslik)
        
        # Kart 1: Bayrak Bulma Butonu (Kırmızı/Turuncu Tonu)
        self.btn_mod_bayrak = QPushButton("🏳️  Ülke Adı (Bayrak Bulma)")
        self.btn_mod_bayrak.setMinimumHeight(90)
        self.btn_mod_bayrak.setStyleSheet("""
            QPushButton {
                background-color: #FF5A5F; 
                color: white; 
                font-weight: bold; 
                font-size: 16px; 
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover { background-color: #E04F54; }
        """)
        
        # Kart 2: Başkent Bulma Butonu (Mavi Tonu)
        self.btn_mod_baskent = QPushButton("🏛️  Başkent İmaj Yarışması")
        self.btn_mod_baskent.setMinimumHeight(90)
        self.btn_mod_baskent.setStyleSheet("""
            QPushButton {
                background-color: #3498DB; 
                color: white; 
                font-weight: bold; 
                font-size: 16px; 
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover { background-color: #2980B9; }
        """)
        
        # Butonları tıklama sinyallerine bağlıyoruz
        self.btn_mod_bayrak.clicked.connect(lambda: self.modu_baslat("Bayrak"))
        self.btn_mod_baskent.clicked.connect(lambda: self.modu_baslat("Baskent"))
        
        # Butonları menü layout'una ekle
        self.menu_layout.addWidget(self.btn_mod_bayrak)
        self.menu_layout.addWidget(self.btn_mod_baskent)
        self.menu_layout.addStretch() # Alttaki boşluğu doldursun diye esneklik ekledik
        
        self.ana_menu_widget.setLayout(self.menu_layout)
        
        # ====================================================
        # SAYFA 1: OYUN ARENASI TASARIMI (Senin Eski Kodların Tamamı)
        # ====================================================
        self.oyun_arenasi_widget = QWidget()
        self.oyun_layout = QVBoxLayout()
        
        # İlerleme Çubuğu (Progress Bar)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.oyun_layout.addWidget(self.progress)
        
        # Soru Metni Durum Bilgisi
        self.label_durum = QLabel("Bu bayrak hangi ülkeye ait?")
        self.label_durum.setAlignment(Qt.AlignCenter)
        self.label_durum.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        self.oyun_layout.addWidget(self.label_durum)
        
        # Bayrak Resminin Gösterileceği Alan
        self.label_resim = QLabel()
        self.label_resim.setAlignment(Qt.AlignCenter)
        self.label_resim.setStyleSheet("border: 2px solid #ddd; background-color: white; border-radius: 8px;")
        self.label_resim.setFixedSize(400, 240)
        self.oyun_layout.addWidget(self.label_resim)
        
        # 4 Adet Cevap Şıkkı Butonları
        self.button_layout = QVBoxLayout()
        self.butonlar = []
        for i in range(4):
            btn = QPushButton(f"Şık {i+1}")
            btn.setMinimumHeight(50)
            btn.setStyleSheet("font-size: 14px; border: 1px solid #bbb; border-radius: 5px; background-color: #fafafa;")
            btn.clicked.connect(self.cevap_kontrol)
            self.butonlar.append(btn)
            self.button_layout.addWidget(btn)
            
        self.oyun_layout.addLayout(self.button_layout)
        self.oyun_arenasi_widget.setLayout(self.oyun_layout)
        
        # SAYFALARI YÖNETİCİYE KAYDET VE PENCEREYE BAS
        self.sayfa_yoneticisi.addWidget(self.ana_menu_widget)     # İndeks 0
        self.sayfa_yoneticisi.addWidget(self.oyun_arenasi_widget)  # İndeks 1
        
        # Pencerenin ana iskeletine sayfa yöneticisini gömüyoruz
        pencere_iskelet_layout = QVBoxLayout()
        pencere_iskelet_layout.addWidget(self.sayfa_yoneticisi)
        self.setLayout(pencere_iskelet_layout)
        
        # UYGULAMA İLK AÇILDIĞINDA ANA MENÜ GÖSTERİLSİN (İndeks 0)
        self.sayfa_yoneticisi.setCurrentIndex(0)
    def oyunu_baslat(self):
        """Sadece henüz ÖĞRENİLMEMİŞ (is_learned = 0) soruları rastgele seçer."""
        if self.oyun_modu == "Baskent":
            # Filtreyi geri aldık; artık başkentler geleceği için sadece gerçek başkenti olanlar seçilecek!
            self.cursor.execute("""SELECT isim, resim_url, baskent FROM bayraklar 
                                   WHERE baskent NOT LIKE '%Belirtilmemiş%' AND is_learned = 0 
                                   ORDER BY RANDOM() LIMIT 10""")
        else:
            self.cursor.execute("""SELECT isim, resim_url, baskent FROM bayraklar 
                                   WHERE is_learned = 0 
                                   ORDER BY RANDOM() LIMIT 10""")
            
        self.soru_havuzu = [{"isim": satir[0], "url": satir[1], "baskent": satir[2]} for satir in self.cursor.fetchall()]
        
        print(f"DEBUG: {self.oyun_modu} modu için havuzdan çekilen soru sayısı -> {len(self.soru_havuzu)}")

        if not self.soru_havuzu:
            QMessageBox.information(self, "Bilgi", f"Harika! {self.oyun_modu} modunda öğrenilecek soru kalmadı! 🏆")
            self.sayfa_yoneticisi.setCurrentIndex(0)
            return

        self.progress.setRange(0, len(self.soru_havuzu))
        self.yanlis_havuzu = []
        self.progress.setValue(0)
        self.yeni_soru()

    def yeni_soru(self):
        """Uygulama moduna göre soruyu, şıkları ve görselleri dinamik olarak hazırlar."""
        try:
            if not self.soru_havuzu and self.yanlis_havuzu:
                QMessageBox.information(self, "Telafi Turu", "Bilemediğin sorular tekrar geliyor! 🧠")
                self.soru_havuzu = list(self.yanlis_havuzu)
                self.yanlis_havuzu = []
                
            if not self.soru_havuzu:
                QMessageBox.information(self, "Tebrikler", f"{self.oyun_modu} modunu başarıyla tamamladın! 🎉")
                self.sayfa_yoneticisi.setCurrentIndex(0)
                return

            self.dogru_cevap = self.soru_havuzu.pop(0)
            
            # Veritabanından rastgele 3 çeldirici şık seçiyoruz
            self.cursor.execute("SELECT isim, resim_url, baskent FROM bayraklar WHERE isim != ? ORDER BY RANDOM() LIMIT 3", (self.dogru_cevap['isim'],))
            yanlis_satirlar = self.cursor.fetchall()
            
            tum_siklar = [{"isim": satir[0], "url": satir[1], "baskent": satir[2]} for satir in yanlis_satirlar]
            tum_siklar.append(self.dogru_cevap)
            random.shuffle(tum_siklar)

            # ====================================================
            # MOD 1: BAYRAK BULMA MODU
            # ====================================================
            if self.oyun_modu == "Bayrak":
                self.label_durum.setText("Bu bayrak hangi ülkeye ait?")
                self.resim_yukle_ve_goster(self.label_resim, self.dogru_cevap['url'])
                
                for i, btn in enumerate(self.butonlar):
                    btn.setIcon(QIcon()) # Eski ikonları temizle
                    btn.setText(tum_siklar[i]['isim'])
                    btn.setProperty("ulke_adi", "") # Property temizle
                    # Klasik metin butonu stili
                    btn.setStyleSheet("font-size: 14px; border: 1px solid #bbb; border-radius: 5px; background-color: #fafafa;")
                    
            # ====================================================
            # MOD 2: BAŞKENT İMAJ YARIŞMASI MODU (ZAFER MODUMUZ!)
            # ====================================================
            # ====================================================
            # MOD 2: BAŞKENT İMAJ YARIŞMASI MODU
            # ====================================================
            elif self.oyun_modu == "Baskent":
                self.label_durum.setText(f"Başkenti '{self.dogru_cevap['baskent']}' olan ülke hangisidir?")
                
                PEXELS_API_KEY = "1fr97GSwvwhXLNZG6y6I8cOGNJhgePrT6nuj0tRctJHF8fguGFnM7QAb"
                
                import urllib.parse
                raw_sorgu = f"{self.dogru_cevap['isim']} cityscape"
                arama_sorgusu = urllib.parse.quote(raw_sorgu)
                
                sehir_resim_url = None
                
                try:
                    headers = {
                        "Authorization": PEXELS_API_KEY,
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    }
                    api_url = f"https://api.pexels.com/v1/search?query={arama_sorgusu}&per_page=1"
                    req = urllib.request.Request(api_url, headers=headers)
                    response = urllib.request.urlopen(req).read()
                    
                    import json
                    json_data = json.loads(response)
                    
                    # Eğer Pexels o ülkeye ait fotoğraf bulduysa linkini alıyoruz
                    if json_data.get("photos") and len(json_data["photos"]) > 0:
                        sehir_resim_url = json_data["photos"][0]["src"]["medium"]
                except Exception as api_hatasi:
                    print(f"Pexels API hatası: {api_hatasi}")

                # --- RESİM BASMA ALANINI GARANTİYE ALIYORUZ ---
                # Eğer şehir resmi bulunduysa onu göster, bulunamadıysa (boş döndüyse) bayrağını göster!
                if sehir_resim_url:
                    self.resim_yukle_ve_goster(self.label_resim, sehir_resim_url)
                else:
                    print(f"💡 {self.dogru_cevap['isim']} için şehir resmi bulunamadı, bayrak yükleniyor.")
                    self.resim_yukle_ve_goster(self.label_resim, self.dogru_cevap['url'])

                # --- BUTONLARI HER KOŞULDA RESİMLİ YAPACAK DÖNGÜ ---
                for i, btn in enumerate(self.butonlar):
                    btn.setText("") # Eski 'Şık X' yazılarını kesin olarak sil!
                    
                    pixmap = self.url_to_pixmap(tum_siklar[i]['url'])
                    if pixmap:
                        scaled_pixmap = pixmap.scaled(380, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        btn.setIcon(QIcon(scaled_pixmap))
                        btn.setIconSize(QSize(380, 80))
                        btn.setStyleSheet("""
                            QPushButton {
                                background-color: transparent; 
                                border: 2px solid #ddd; 
                                border-radius: 8px;
                                padding: 5px;
                            }
                            QPushButton:hover { border: 2px solid #3498DB; }
                        """)
                    else:
                        # Eğer o şıkkın bayrağı internetten anlık inmezse isim yazsın (Yine de şık yazısı kalmasın!)
                        btn.setText(tum_siklar[i]['isim'])
                        btn.setStyleSheet("font-size: 14px; border: 1px solid #bbb; border-radius: 5px; background-color: #fafafa;")
                    
                    btn.setProperty("ulke_adi", tum_siklar[i]['isim'])
                    
        except Exception as e:
            print(f"\n❌ YENİ SORU YÜKLENİRKEN HATA OLUŞTU: {e}")
            import traceback
            traceback.print_exc()

    def url_to_pixmap(self, url):
        """İnternet linkini PyQt5'in anlayacağı QPixmap nesnesine dönüştürür."""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            image = QImage()
            image.loadFromData(data)
            return QPixmap.fromImage(image)
        except:
            return None

    def resim_yukle_ve_goster(self, hedef_label, url):
        """İnternetten resmi çekip parametre olarak gelen hedef label içerisine basar."""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            image = QImage()
            image.loadFromData(data)
            pixmap = QPixmap.fromImage(image)
            # Resmi, gönderdiğimiz hedef_label'ın boyutuna göre ölçekleyip basıyoruz
            hedef_label.setPixmap(pixmap.scaled(hedef_label.width(), hedef_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            hedef_label.setText(f"Resim Yüklenemedi:\n{self.dogru_cevap['isim']}")
            print(f"Resim çekme hatası: {e}")
    def mod_degistir(self, yeni_mod):
        self.oyun_modu = yeni_mod
        self.oyunu_baslat()
    def modu_baslat(self, secilen_mod):
        self.oyun_modu = secilen_mod
        self.oyunu_baslat() # Veritabanından o moda göre 10 soru seçer
        self.sayfa_yoneticisi.setCurrentIndex(1) # Oyun sayfasını (İndeks 1) ekrana getirir!
    def cevap_kontrol(self):
        """Doğru/Yanlış durumuna göre butonları mod bağımsız olarak renklendirir."""
        gonderen_buton = self.sender()
        
        # Hangi modda olduğumuza göre seçilen cevabı ayırt ediyoruz
        if self.oyun_modu == "Baskent":
            secilen_cevap = gonderen_buton.property("ulke_adi")
        else:
            secilen_cevap = gonderen_buton.text()
            
        for btn in self.butonlar:
            btn.setEnabled(False)
        
        if secilen_cevap == self.dogru_cevap['isim']:
            # DOĞRU CEVAP: Seçilen butonu yeşil yap
            gonderen_buton.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: #2ECC71; border-radius: 5px;")
            self.progress.setValue(self.progress.value() + 1)
            
            # Akıllı Öğrenme Algoritması (Correct Streak İşlemleri)
            self.cursor.execute("SELECT correct_streak FROM bayraklar WHERE isim = ?", (self.dogru_cevap['isim'],))
            mevcut_seri = self.cursor.fetchone()[0] + 1
            
            if mevcut_seri >= 3:
                self.cursor.execute("UPDATE bayraklar SET correct_streak = ?, is_learned = 1 WHERE isim = ?", (mevcut_seri, self.dogru_cevap['isim']))
                print(f"🔥 {self.dogru_cevap['isim']} tamamen öğrenildi ve havuzdan elendi!")
            else:
                self.cursor.execute("UPDATE bayraklar SET correct_streak = ? WHERE isim = ?", (mevcut_seri, self.dogru_cevap['isim']))
            self.db.commit()

        else:
            # YANLIŞ CEVAP: Tıklanan hatalı butonu kırmızı yap
            gonderen_buton.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: #E74C3C; border-radius: 5px;")
            
            # --- DEBUGLADIĞIMIZ KRİTİK KISIM BURASI ---
            # Her iki modda da (Metin veya Resim fark etmeksizin) DOĞRU şıkkı bulup yeşile boyar
            for btn in self.butonlar:
                # Butonun metni veya arka plandaki gizli mülkü (property) doğru ülkeyle eşleşiyorsa:
                if btn.text() == self.dogru_cevap['isim'] or btn.property("ulke_adi") == self.dogru_cevap['isim']:
                    btn.setStyleSheet("font-size: 14px; font-weight: bold; color: white; background-color: #2ECC71; border-radius: 5px;")
            
            if self.dogru_cevap not in self.yanlis_havuzu:
                self.yanlis_havuzu.append(self.dogru_cevap)
            
            self.cursor.execute("UPDATE bayraklar SET fail_count = fail_count + 1, correct_streak = 0 WHERE isim = ?", (self.dogru_cevap['isim'],))
            self.db.commit()

        QTimer.singleShot(1000, self.sonraki_soruya_ilerle)

    def sonraki_soruya_ilerle(self):
        """Buton stillerini eski haline getirir ve yeni soruyu çağırır."""
        for btn in self.butonlar:
            btn.setEnabled(True)
            # Eski orijinal gri-beyaz haline geri döndür
            btn.setStyleSheet("font-size: 14px; border: 1px solid #bbb; border-radius: 5px; background-color: #fafafa;")
        
        self.yeni_soru()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = BayrakOyunu()
    pencere.show()
    sys.exit(app.exec_())