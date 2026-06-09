import shutil #Dosyalama işlemleri için kullanılan bir modül-kütüphane. Dosya kopyalama, taşıma ve silme gibi işlemleri kolayca yapmamızı sağlar. Bu sayede seçilen resimleri belirlediğimiz bir klasöre kopyalayarak düzenli bir sekilde saklarız.
import os #Dosya ve dizin işlemleri için kullanılır. Dosya yollarını yönetir. OS: Operating System(işletim sistemi)
from PyQt5.QtCore import Qt#Qt PyQt5 kütüphanesinin çekirdek(Core) modülüdür. Grafiksel değildir. Qt nesnesi özelleştirme için birçok sabit ve yardımcı fonksiyon barındırır kısaca ayar.
import sys # Bu modül, python çalışma ortamı ile doğrudan iletişim kkurmanı sağlar.Uygulamanın temiz bir şekilde kapatılması veya komut satırı argümanlarına erişim için kulllanılır.Sistemle ilgili parametreleri ve fonksiyonları barındırır.
import sqlite3 # Programın verileri bilgisayarda bir dosya (veritabanı) olarak saklanacaktır ve bunu herhangi bir eklenti olmadan yapabilmemizi sağlar.
from PyQt5.QtWidgets import * #PyQt5 kütüphanesi programın görsel arayüzünü oluşturmak 
#için kullanılan araç çantasıdır ve * diyerek tüm özelliklerini programımızda kullanıma açıyoruz.
from PyQt5.QtGui import QFont, QPixmap,QIcon,QPainter#QFont sınıfı, metinlerin yazı tipini, boyutunu ve sitilini belirlemek için kullanılır bu sayede uygulama daha çekici görünür ve okunabilirliği artar. Pixmap: Ekranda görsel görebilmeyi sağlar.
from PyQt5.QtCore import Qt, QSize #Qt sınıfı, PyQt5'te birçok sabit ve yardımcı fonksiyon içerir. Örneğin, hizalama
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas #Pasta grafiğini eklemek için  gerekli kütüphaneler //as: Çok uzun olan FigureCanvasQTAgg ismini kod  içinde sürekli yazmamak için ona kısaca Canvas lakabını takıyoruz. Bu sınıf, matplotlib ile çizdiğimiz grafikleri PyQt5 pencerelerinin içine birer görsel nesneymiş gibi yerleştirmemizi sağlayan bir köprü görevi görür
from matplotlib.figure import Figure# Grafiğin çizileceği boş beyaz sayfayı(çerçeveyi) temsil eder.
import matplotlib.pyplot as plt#pyplot grafik çizmeyi kolaylaştıran Matplotlib arayüzüdür.
#VERİTABANI YÖNETİCİSİ
class dbManager:#dbManager M büyük PascalCase
    def __init__(self, db_ad):#Sınıfın kurucu metodudur. Sınıftan nesne oluşturulduğunda otomatik olarak bir kez çalışır ve veritabanı bağlantısını kurar. ***** self:Sınıfın kendisine ait olan nesneyi temsil eder. Sınıf içindeki diğer fonksiyonların ve değişkenlerin birbirine erişebilmesi için ilk parametre olarak her zaman self yaılmalıdır. db_ad: Dışarıdan verilecek olan veritabanı dosya adını tutan parametre.
        self.baglanti = sqlite3.connect(db_ad) #Parametre olarak gelen isim adından bir veritabanı dosyası oluşturur veya var olan dosyaya bağlanır. self.baglanti diyerek veritabanına erişebiliriz
        self.cursor = self.baglanti.cursor()# Veritabanı üzerinde SQL komutlarını gerçekleştirmek için bir imleç(cursor) oluşturur. SQL komutlarını (Create, insert, select, delete:CRUD) veritabanına işleyebilmek ve gelen sonuçları okuyabilmek içinbu imleç nesnesine ihtiyacımız vardır.
        self.tablolari_olustur()#Nesne oluşturulur oluşturulmaz tabloların hazır olduğundan emin olmak için bu metodu çağırır.

    def tablolari_olustur(self):
        # Stok Tablosu (Yorumları üç tırnağın dışına, yani Python alanına taşıdık)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS stok (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_adi TEXT,
            kategori TEXT, 
            miktar INTEGER, 
            fiyat REAL,
            resim_yolu TEXT DEFAULT '')""")
            
        # Siparişler Tablosu
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS siparisler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musteri_ad TEXT,
            urun_tipi TEXT, 
            olcu_notu TEXT, 
            durum TEXT DEFAULT 'Beklemede')""")
            
        self.baglanti.commit()

    def veri_ekle(self, sorgu, parametreler):# veritabanına yeni bir ürün eklemek, bir siparişi güncellemek (update) veya bir kaydı silmek(delete) gibi değişiklikler için kullanılır. **** sorgu:Dışarıdan gönderilecek olan SQL komutunu tutar. parametreler:SQL sorgusundaki soru işaretlerinin (?) yerine gelecekolan gerçek verileri bir tuple (demet) veya listedir. içinde tutulur. Sql injection gibi güvenlik açıklarına önlem.
        self.cursor.execute(sorgu, parametreler)#Yazılan  sql komutunu ve içeriğini veritabanına gönderir
        self.baglanti.commit()#Yapılan ekleme, silme veya güncelleme işlemlerinin veritabanına kaydedilmesini sağlar
    def veri_getir(self, sorgu, parametreler=()):#Veritabanından veri okumak listelemek veya arama yapmak (select) gibi işlemler için kullanılır.***** parametreler=():varsayılan değer atar yani ikinci değer yazmazsan ,Python otomatik olarak onu boş bir demet() kabul eder.
        self.cursor.execute(sorgu, parametreler)#Belirtilen SELECT sorgusunu, varsa filtre parametreleriyle birlikte çalıştırır. Bilgisayar arka planda eşleşen verileri ile birlikte çalıştırır. Bilgisayar arka planda eşleşen verileri hazırlar ve imlecin(cursor) hafızasında tutar.
        return self.cursor.fetchall()# fetchall() metodu, imlecin hafızasında tutulan tüm sonuçları toplar.Bu verileri bize bir liste içinde demetler(tuple) şeklinde sunar.
#ANA PENCERE (NESNE: Uygulamanın kendisi) DASHBOARD Kullanıcının göreceği ana iskelet
class StokPastaGrafigi(Canvas):#FigureCanvasQTAgg sınıfından miras alarak kendi grafik sınıfımızı tanımlıyoruz. StokPastaGrafigi artık sadece düz bir kod bloğu değil, doğrudan PyQt5 içine gömülebilen görsel bir grafik çizim alanıdır.
    def __init__(self, parent=None, width=4, height=3, dpi=100):#parent=None:Bu grafik alanının hangi PyQy5 penceresine ait olacağını belirler. Eğer çağırılırken bir pencere belirtilmezse,None (hiçbiri) yani bağımsız bir alan olarak başlar. width=4, height=3:Grafiğin çerçevesini(Figure) inç cinsinden varsayılan genişlik (width) ve yükseklik (height) değerleridir. ****dpi=100:Dost Per Inch(inç başına düşen nokta sayısı). Grafiğin çözünürlük kalitesini belirler. 100 oldukça ideal ve net bir değerdir.
        # Projenin genel krem/vintage temasına uygun bir arka plan rengi seçiyoruz
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#F7F4EF')
        #self.fig=Figure(...):Figure sınıfından yeni bir boş grafik sayfası (tuvali üretir) figsize=(width, height):Genişlik ve yükseklik parametrelerini bir demek (tuple) olarak içeriye aktarır. facecolor='#F7F4EF': grafiğin arka plan rengini HEX renk kodu olan krem/vintage tonuna boyar. Oluşan bu grafik sayfası self.fig özelliğine kaydedilir.
        self.axes = self.fig.add_subplot(111)#self.fig.add_subplot(111) Grafiğin çizilecek koordinat sistemini(eksenleri) oluşturur. 111 bir klasiktir: 1 satır 1 sütunluk bir tablonun 1. grafiği olsun yani tüm tuvali tek bir grafik kaplasın demektir.
        #self.axes: Çizimi yapacak olan diğital ekseni değişkende tutuyoruz.
        super().__init__(self.fig)#Miras aldığımız ana sınıfa gidip 'Seni benim oluşturduğum bu self.fig ile başlatıyorum der. PyQt5 ile Matplotlib arasndaki köprüyü kuran hayati satır burasıdır. 
        self.setParent(parent)#Bu grafik nesnesini, üst pencerenin(parent) içerisine fiziksel olarak yerleştirir ve onun bir parçası yapar

    def grafik_guncelle(self, veritabanı_baglantisi):#dışarıdan veritabani_baglantisi adında bir nesne ister.
        """Veritabanındaki ürünleri kategorilerine göre gruplayarak pasta grafiği çizer"""
        self.axes.clear()#Yeni grafiği çizmeden önce eski çizimleri tamamen siler, temiz bir sayfa açar. Bu yapılmazsa yeni grafik eskilerinin üstüne biner ve çorba olur
        
        try:#Hata çıkabilecek bir bölüme giriyoruz, dikkatli ol bloğudur. Veritabanınadan veri çekerken oluşabilecek anlık kesintilerde programın çökmesi engellenir
            cursor = veritabanı_baglantisi.cursor()#GElen veritabanı nesnesinin üzerinden SQL sorgusu çalıştırabilmek için anlık bir cursor (imleç) oluşturur
            # MÜHENDİSLİK DOKUNUŞU: Ürünleri tek tek çekmek yerine kategorilerine göre TOPLAM miktarlarını çekiyoruz.
            cursor.execute("SELECT kategori, SUM(CAST(miktar AS INTEGER)) FROM stok GROUP BY kategori")#execute(...):SQL komutunu çalıştırır. Sorgunun içindeki sihirli mantık şudur: SELECT kategori: Kategorilerin isimlerini seç CAST(miktar AS INTEGER) veritabanında metin veya farklı türde kaydedilmemiş olma ihtimaline karşı, miktar sütununu matematiksel tam sayıya dönüştürür. SUM(...) Aynı kategoriye ait tüm ürünlerin miktarını toplar. GROUP BY kategori: verileri kategorilerine göre paketler
            veriler = cursor.fetchall()#sorgu sonucu oluşan listeyi veriler isimli değişkene aktarır
        except Exception as e:#Eğer try içindeki kodlarda (SQL hatası, veri tipi uyumsuzluğu vb.) bir sorun çıkarsa, hata e değişkenine aktarılır,
            print("Veritabanı veya Dönüşüm Hatası:", e)#terminale yazdırılır
            veriler = []#programın çökmemesi için veriler listesi boş [] bir list olarak ayarlanır.
        
        if not veriler:#Eğer veriler listesi boşsa veritabanında hiç ürün yoksa veya hata oluştuysa bu blok çalışacak
            self.axes.text(0.5, 0.5, "Stok Verisi Bulunmuyor", ha='center', va='center', color='#7E6B5A')#Grafiğin tam ortasına 0.5 ve 0.5 koordinatlarına "Stok Verisi Bulunamadı" yazısı basar ha='center':Yatayda ortala (Horizontal Alignment) va='center':Dikeyde ortala (Vertical Alignment) color='#7E6B5A': Yazıyı kahverengi/ bohem tonunda yazar.
            self.draw()
            return

        # Sadece kategori isimlerini ve toplam miktarları alıyoruz
        kategoriler = [satir[0] if satir[0] else "Belirsiz" for satir in veriler]#kategoriler=veriler içindeki bir satırın ilk elemanını (satir[0],yani kategori adını) alır. Eğer kategori adı boşsa (None), ekranda çirkin durmasın diye yerine "Belirsiz" yazar.
        miktarlar = [satir[1] if satir[1] else 0 for satir in veriler]#miktarlar: Her satırın ikinci elemanını(satir[1],yani toplam miktarı) alır. Eğer miktar yoksa 0 kabul eder.
        
        # Soft bohem renk tonlarımız
        renkler = ['#D9C5B2', '#7E6B5A', '#B5A492', '#4A3B32', '#EAE6E1', '#C4B5A5', '#A89F91']
        
        # Pasta grafiğini çiziyoruz
        #self.axes.pie(...):Pasta grafiği çizmek için kullanılan ana fonksiyondur. İçine verdiğimiz verilerle dilimleri oluşturur. Verilen parametreler sırasıyla: miktarlar: Her dilimin büyüklüğünü belirler, labels=kategoriler: Her dilimin kenarına kategori isimlerini yazar, colors=renkler[:len(kategoriler)]: Dilimlerin renklerini belirler, textprops={'fontsize': 9, 'color': '#4A3B32', 'weight': 'bold'}: Yazıların stilini belirler.
        wedges, texts, autotexts = self.axes.pie(#wedges:Pasta dilinin geometrik şekilleri texts:Dilimlerin kenarlarına yazılan kategori isimlerinin yazı nesneleri
            miktarlar, 
            labels=kategoriler,#Artık uzun ürün isimleri değil, sadece temiz kategori adları yazacak!
            autopct='%1.1f%%',# ****autopct='%1.1f%%': Her dilimin içine yüzde değerini yazar
            startangle=140,#Grafiğin başlangıç açısını 140 derece yaparak daha hoş bir görünüm sağlar
            colors=renkler[:len(kategoriler)],
            textprops={'fontsize': 9, 'color': '#4A3B32', 'weight': 'bold'}#Yazıların stilini belirler.
        )
        
        self.axes.set_title("Kategori Bazlı Stok Dağılımı", fontsize=11, weight='bold', color='#4A3B32')
        self.fig.tight_layout()#tight_layout() grafiğin kenar boşluklarını otomatik olarak ayarlar, böylece yazılar ve dilimler birbirine yapışmaz, daha düzenli görünür.
        self.draw()
class AtolyeApp(QMainWindow): #QMainWindow, PyQt5'in en üst düzey pencere şablonudur ve bu sınıfından miras aldık.Bu sayede uygulama ana penceresi, menü çubuğu(Menu Bar) ve durum çbukları(status bar) gibi özelliklere sahip olur. 
    def __init__(self):#
        super().__init__()#Mira aldığımız sınıfın kurucu metodu urada bir def açılacak.
        self.db = dbManager(r"C:\Users\busra\OneDrive\Desktop\Yeniklasor\Busra_atolyesi.db")#Yazdığımız veritabanı sınıfından bir nesne üretiyoruz. Amaç:Veritabanına daha kolay erişmek için r"..." :yol metninin ham (raw) string olarak değerlendirilmesini sağlar. Böylece ters bölü (\) karakteri özel bir anlam taşımaz ve dosya yolunu doğru şekilde tanımlar.*****yoksa python bunları(/) kaçış karakteri olarak algılar ve hata verir.
        self.setWindowTitle("Büşra'nın Tasarım Atölyesi v1.0")#Pencereye isim-başlık veriyoruz
        self.setGeometry(100, 100, 1200, 800)#Pencerenin ekranda açılacağı konumu ve boyutunu belirler. (x, y, width, height) şeklinde parametre alır. 100,100: Pencerenin sol üst köşesinin ekranda 100 piksel sağa ve 100 piksel aşağıda açılmasını sağlar. 1200,800: Pencerenin genişliğini 1200 piksel, yüksekliğini ise 800 piksel yapar.
        # 1. Sekme Kontrolünü Oluştur
        self.tabs = QTabWidget()#Sekmeler arası geçiş yapmamızı sağlayacak olan QTabWidget sınıfından bir nesne oluşturuyoruz. Bu nesne, farklı sayfaları (sekmeleri) tek bir pencere içinde düzenlememize olanak tanır. Kullanıcılar bu sekmeler arasında tıklayarak geçiş yapabilirler. tab=sekme
        self.setCentralWidget(self.tabs)#QMainWindow mimarisinde pencerenin tam ortasındaki ana gövdeye ne yerleştirileceğini seçeriz.Bu satırla  birlikte, pencerenin tüm ana alaını sekmeler kaplamış olur 
        # 2. Sayfaları (Widget) Tanımla
        self.sekme_ana_sayfa = QWidget()
        self.sekme_stok = QWidget()
        self.sekme_ozel_tasarim = QWidget()
        # 3. Sekmeleri İsimlendirerek Ekle (Sıralama: Ana Sayfa en başta olsun)
        self.tabs.addTab(self.sekme_ana_sayfa, "🏠 Ana Sayfa")
        self.tabs.addTab(self.sekme_stok, "📦 Stok Durumu")
        self.tabs.addTab(self.sekme_ozel_tasarim, "🎨 Özel Tasarım")

        # 4. CRITICAL: Tasarım Fonksiyonlarını Çağır (Bu satırlar olmazsa sayfalar boş kalır)
        self.ana_ekran_tasarimi()# Az önce eklediğin metod
        self.stok_tasarimi()# Tablonun olduğu metod
        self.ozel_tasarim_tasarimi() # Bunu sonra yapacağız
        self.stoklari_yenile() # Uygulama açılır açılmaz depodaki her şeyi getir!
    def arayuz_hazirla(self):
        self.setWindowTitle("Büşra'nın Tasarım Atölyesi v1.0")
        self.setGeometry(100, 100, 900, 700)

        # Merkezi Widget ve Ana Layout
        self.merkez_widget = QWidget()#PyQt5'te ana pencerenin içine her şeyi tutacak bir boş 
        #kutu yerleştirmen gerekir
        self.setCentralWidget(self.merkez_widget)
        self.ana_layout = QVBoxLayout(self.merkez_widget)#Dikey düzen oluşturur.

        # Başlık
        self.baslik = QLabel("✂️ ATÖLYE YÖNETİM PANELİ")
        self.baslik.setFont(QFont("Arial", 18, QFont.Bold))
        self.ana_layout.addWidget(self.baslik)#Hazırladığımız başlığı Layout'un en üstüne  ekledik.

        # Sekmeler (QTabWidget)
        self.sekmeler = QTabWidget()
        self.ana_layout.addWidget(self.sekmeler)

        # SEKME 1: STOK YÖNETİMİ
        self.sekme_stok = QWidget()#Stok sayfası için yen boş alan oluşturur.
        self.stok_tasarimi()
        self.sekmeler.addTab(self.sekme_stok, "📦 Stok Durumu")#Bu boş alanı "Stok durumu"
        #Başlığıyla sekmeler listesine ekler.

        # SEKME 2: ÖZEL TASARIM & SİPARİŞ
        self.sekme_siparis = QWidget()
        self.siparis_tasarimi()
        self.sekmeler.addTab(self.sekme_siparis, "🎨 Özel Tasarım")

    def stok_tasarimi(self):
        layout = QVBoxLayout(self.sekme_stok)
        
        # 1. ARAMA ÇUBUĞU
        self.arama_cubugu = QLineEdit()
        self.arama_cubugu.setPlaceholderText("🔍 Ürün adı veya kategori ara...")
        self.arama_cubugu.textChanged.connect(self.canli_arama) 
        layout.addWidget(self.arama_cubugu)

        # --- YENİ DÜZEN: ÜST KISIM (SOLDAN SAĞA) ---
        # Giriş çubukları ve pasta grafiğini yan yana getirecek ana yatay düzen
        ust_ana_layout = QHBoxLayout()

        # SOL KUTU: Giriş Alanları (Burada çubukları daraltıp topluyoruz)
        sol_giris_layout = QVBoxLayout()
        sol_giris_layout.setSpacing(8) # Çubukların arasındaki boşluğu şık bir seviyeye indirdik

        self.urun_adi_giris = QLineEdit(); self.urun_adi_giris.setPlaceholderText("Ürün Adı...")
        self.miktar_giris = QLineEdit(); self.miktar_giris.setPlaceholderText("Adet/Metre...")
        self.fiyat_giris = QLineEdit(); self.fiyat_giris.setPlaceholderText("Fiyat...")

        self.kategori_secim = QComboBox()
        self.kategori_secim.addItems(["Vintage Ceket","Elbise","Kemer","Korse","Çanta" ,"Bohem Etek","Kot Etek","Pantolon","Baggy Pantolon","Gömlek","Bluz"])
        
        self.resim_yolu_etiket = QLabel("Resim seçilmedi")
        self.resim_Sec_buton = QPushButton("📷 Resim Seç")
        self.resim_Sec_buton.clicked.connect(self.resim_sec)

        # Çubukları sol taraftaki dikey düzene ekliyoruz
        sol_giris_layout.addWidget(QLabel("<b>Ürün Bilgileri:</b>")) # Küçük bir başlık
        sol_giris_layout.addWidget(self.urun_adi_giris)
        sol_giris_layout.addWidget(self.kategori_secim)
        sol_giris_layout.addWidget(self.miktar_giris)
        sol_giris_layout.addWidget(self.fiyat_giris)
        sol_giris_layout.addWidget(self.resim_yolu_etiket)
        sol_giris_layout.addWidget(self.resim_Sec_buton)

        # SAĞ KUTU: Pasta Grafiği (Senin eklediğin grafik sınıfını buraya bağlıyoruz)
        self.stok_grafigi = StokPastaGrafigi(self, width=4, height=3)
        
        # Şimdi sol kutuyu ve sağdaki grafiği üst ana düzende birleştiriyoruz
        ust_ana_layout.addLayout(sol_giris_layout, stretch=2) # Giriş alanları %40 yer kaplasın
        ust_ana_layout.addWidget(self.stok_grafigi, stretch=3)    # Pasta grafiği %60 yer kaplasın

        # Hazırladığımız bu muhteşem üst düzeni ana sayfaya gömüyoruz
        layout.addLayout(ust_ana_layout)

        # 3. BUTONLAR (Ekleme ve Silme butonları yan yana şık dursun diye QHBoxLayout yapıyoruz)
        buton_layout = QHBoxLayout()
        self.ekle_butonu = QPushButton("✅ Stoka İşle")
        self.ekle_butonu.setStyleSheet("background-color: #ff6700; color: white; font-weight: bold; height: 30px;")
        self.ekle_butonu.clicked.connect(self.stok_ekle)
        
        self.sil_buton = QPushButton("🗑️ Seçili Ürünü Sil")
        self.sil_buton.setStyleSheet("font-weight: bold; height: 30px;")
        self.sil_buton.clicked.connect(self.stok_sil)
        
        buton_layout.addWidget(self.ekle_butonu)
        buton_layout.addWidget(self.sil_buton)
        layout.addLayout(buton_layout)

        # 4. TABLO VE ÖNİZLEME (Mevcut kodun, buraya dokunmuyoruz)
        self.yan_yana_layout = QHBoxLayout()
        
        self.stok_tablo = QTableWidget()
        self.stok_tablo.setColumnCount(6)
        self.stok_tablo.setHorizontalHeaderLabels(["ID", "Ürün", "Kategori", "Miktar", "Fiyat", "Resim Yolu"])
        self.yan_yana_layout.addWidget(self.stok_tablo)

        self.onizleme_etiket = QLabel("Resim Önizleme")
        self.onizleme_etiket.setFixedSize(250, 350)
        self.onizleme_etiket.setStyleSheet("border: 2px dashed #ff6700; background-color: #f9f9f9;")
        self.onizleme_etiket.setAlignment(Qt.AlignCenter)
        self.onizleme_etiket.setScaledContents(True)
        self.yan_yana_layout.addWidget(self.onizleme_etiket)

        layout.addLayout(self.yan_yana_layout)

        # 5. OLAYLAR VE İLK YÜKLEME
        self.stok_tablo.itemClicked.connect(self.resim_goster)
        self.stoklari_yenile()
        
        # Grafiğin veritabanından ilk verileri çekip çizilmesi için tetikliyoruz
        # Senin dbManager yapına göre bağlantıyı self.db.baglanti olarak gönderiyoruz
        if hasattr(self.db, 'baglanti'):
            self.stok_grafigi.grafik_guncelle(self.db.baglanti)
    def resim_goster(self, item):
        satir = item.row() # Hangi satıra tıklandığını bul
        # Resim yolu 5. sütunda (0'dan başladığı için: ID:0, Ürün:1, Kat:2, Mik:3, Fiyat:4, Yol:5)
        resim_item = self.stok_tablo.item(satir, 5)
        
        if resim_item:
            resim_yolu = resim_item.text()
            if resim_yolu and os.path.exists(resim_yolu):
                pixmap = QPixmap(resim_yolu)
                self.onizleme_etiket.setPixmap(pixmap)
            else:
                self.onizleme_etiket.setText("Resim Yok")
    def resim_sec(self):
        # Bilgisayardaki dosyaları açan pencere (QFileDialog)
        dosya_yolu, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg)")
        
        if dosya_yolu:
            hedef_klasor="resimler"
            if not os.path.exists(hedef_klasor):
                os.makedirs(hedef_klasor)
            dosya_adi=os.path.basename(dosya_yolu)
            hedef_yol=os.path.join(hedef_klasor, dosya_adi)
            if dosya_yolu != hedef_yol:
                shutil.copy2(dosya_yolu,hedef_yol)
            # Seçilen resmin yolunu etikete yaz (Böylece seçildiğini anlarız)
            self.resim_yolu_etiket.setText(dosya_adi)
            # Seçilen yolu bir değişkende sakla ki veritabanına kaydedebilelim
            self.secilen_resim_yolu = hedef_yol
        else:
            self.resim_yolu_etiket.setText("Resim Seçilmedi")
            self.secilen_resim_yolu = ""

    def stoklari_yenile(self):
        # 1. Veritabanından tüm stok verilerini çek
        self.db.cursor.execute("SELECT * FROM stok")
        veriler = self.db.cursor.fetchall()
        
        # 2. Tabloyu temizle ve satır sayısını ayarla
        self.stok_tablo.setRowCount(0)
        
        # 3. Verileri tabloya yerleştir
        for satir_indeks, satir_veri in enumerate(veriler):
            self.stok_tablo.insertRow(satir_indeks)
            for sutun_indeks, veri in enumerate(satir_veri):
                # Her bir veriyi tablo hücresine (QTableWidgetItem) dönüştürerek ekle
                item = QTableWidgetItem(str(veri))
                self.stok_tablo.setItem(satir_indeks, sutun_indeks, item)    
    def stok_listele(self):
        # 1. Veritabanından tüm stok verilerini çekiyoruz
        veriler = self.db.veri_getir("SELECT * FROM stok")
        
        # 2. Tablonun satır sayısını sıfırlayıp yeniden dolduruyoruz
        self.stok_tablo.setRowCount(0)
        
        for satir_no, satir_veri in enumerate(veriler):
            self.stok_tablo.insertRow(satir_no)
            for sutun_no, veri in enumerate(satir_veri):
                # Her bir veriyi tablo hücresine yerleştiriyoruz
                self.stok_tablo.setItem(satir_no, sutun_no, QTableWidgetItem(str(veri)))

    def siparis_tasarimi(self):
        # Bu sekme için dikey bir yerleşim planı oluşturuyoruz
        layout = QVBoxLayout(self.sekme_siparis)
        # 1. Müşteri Bilgileri Grubu
        musteri_grup = QGroupBox("Müşteri Bilgileri")
        m_layout = QFormLayout() # Form düzeni: Sol etiket, sağ giriş alanı
        self.m_ad_giris = QLineEdit()
        self.m_tel_giris = QLineEdit()
        m_layout.addRow("Müşteri Ad Soyad:", self.m_ad_giris)
        m_layout.addRow("Telefon:", self.m_tel_giris)
        musteri_grup.setLayout(m_layout)
        layout.addWidget(musteri_grup)

        # 2. Tasarım Detayları Grubu
        tasarim_grup = QGroupBox("Tasarım & Ölçü Detayları")
        t_layout = QVBoxLayout()
        
        self.m_urun_tipi = QComboBox()
        self.m_urun_tipi.addItems(["Vintage Ceket","Elbise","Baggy Pantolon", "Vintage Düşük Bel Pantolon", "Bohem Elbise", "Kelebek Kesim Etek", "Gömlek"])
        t_layout.addWidget(QLabel("Ürün Tipi Seçiniz:"))
        t_layout.addWidget(self.m_urun_tipi)

        self.m_olcu_notu = QTextEdit() # Daha uzun notlar için geniş kutu
        self.m_olcu_notu.setPlaceholderText("Beden ölçülerini veya özel istekleri buraya yazın... (Örn: M Beden, Kol boyu +2cm)")
        t_layout.addWidget(QLabel("Ölçü ve Özel Notlar:"))
        t_layout.addWidget(self.m_olcu_notu)
        
        tasarim_grup.setLayout(t_layout)
        layout.addWidget(tasarim_grup)

        # 3. Sipariş Oluştur Butonu
        self.siparis_buton = QPushButton("🧶 SİPARİŞİ OLUŞTUR VE TAKVİME EKLE")
        self.siparis_buton.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 40px;")
        self.siparis_buton.clicked.connect(self.siparis_kaydet) # Birazdan bu fonksiyonu yazacağız
        layout.addWidget(self.siparis_buton)
    def siparis_kaydet(self):
        # Bilgileri arayüzden alıyoruz
        ad = self.m_ad_giris.text()
        tel = self.m_tel_giris.text()
        urun = self.m_urun_tipi.currentText()
        notlar = self.m_olcu_notu.toPlainText() # QTextEdit'ten veri alma şekli

        if ad and tel:
            # Veritabanına ekliyoruz
            self.db.veri_ekle(
                "INSERT INTO siparisler (musteri_ad, urun_tipi, olcu_notu) VALUES (?,?,?)",
                (ad, urun, notlar)
            )
            QMessageBox.information(self, "Başarılı", "Sipariş başarıyla alındı! Atölyede dikim sırasına eklendi.")
            # Formu temizleyelim
            self.m_ad_giris.clear()
            self.m_tel_giris.clear()
            self.m_olcu_notu.clear()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen müşteri adı ve telefon bilgilerini eksiksiz girin!")

    def stok_ekle(self):
        ad = self.urun_adi_giris.text()
        miktar = self.miktar_giris.text()
        fiyat = self.fiyat_giris.text()
        
        # 1. KRİTİK DÜZELTME: Kategori seçimini en başta, sorgudan ÖNCE almalısın
        kategori = self.kategori_secim.currentText() 
        
        # Resim kontrolü
        resim = getattr(self, 'secilen_resim_yolu', "")

        if ad and miktar and fiyat:
            # 2. KRİTİK DÜZELTME: "Hazır Ürün" yazan yere 'kategori' değişkenini koyuyoruz
            sorgu = "INSERT INTO stok (urun_adi, kategori, miktar, fiyat, resim_yolu) VALUES (?, ?, ?, ?, ?)"
            self.db.veri_ekle(sorgu, (ad, kategori, miktar, fiyat, resim))
            
            self.stoklari_yenile() 
            QMessageBox.information(self, "Başarılı", f"Ürün '{kategori}' kategorisiyle eklendi!")
            self.stok_grafigi.grafik_guncelle(self.db.baglanti)
            # Formu Temizleme
            self.urun_adi_giris.clear()
            self.miktar_giris.clear()
            self.fiyat_giris.clear()
            self.resim_yolu_etiket.setText("Resim seçilmedi")
            self.secilen_resim_yolu = ""
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
    def stok_sil(self):
        secili_satir = self.stok_tablo.currentRow()
        if secili_satir >=0:
            urun_id=self.stok_tablo.item(secili_satir,0).text() #ID yi alır.
            self.db.cursor.execute("DELETE FROM stok WHERE id=?", (urun_id,))
            self.db.baglanti.commit()
            self.stoklari_yenile()
            
            QMessageBox.information(self, "Silindi", "Ürün başarıyla silindi!")
            self.stok_grafigi.grafik_guncelle(self.db.baglanti)
        else:
            QMessageBox.warning(self, "Hata", "Lütfen silmek için bir satır seçin!")
    def ana_ekran_tasarimi(self):
        # Ana Sayfa için Layout oluşturuyoruz
        ana_layout = QVBoxLayout(self.sekme_ana_sayfa)
        ana_layout.setContentsMargins(50, 50, 50, 50) # Kenarlardan boşluk verelim ki şık dursun
        ana_layout.setSpacing(30)
        # 1. Üst Başlık (Milla Turuncusu)
        self.baslik = QLabel("BÜŞRA'NIN TASARIM ATÖLYESİ")
        self.baslik.setAlignment(Qt.AlignCenter)
        self.baslik.setStyleSheet("""
            font-size: 35px; 
            font-weight: bold; 
            color: #ff6700; 
            letter-spacing: 2px;
            font-family: 'Segoe UI', sans-serif;
        """)
        ana_layout.addWidget(self.baslik)
        # 2. Alt Başlık / Slogan
        self.slogan = QLabel("Yeni Sezon Koleksiyonunu Keşfet")
        self.slogan.setAlignment(Qt.AlignCenter)
        self.slogan.setStyleSheet("font-size: 18px; color: #555; font-style: italic;")
        ana_layout.addWidget(self.slogan)
        # 3. Kategori Kartları Alanı (Yan Yana)
        kategori_layout = QHBoxLayout()
        # Kategoriler listesi (İsim ve senin klasöründeki ikon resimleri)
        # ÖNEMLİ: resimler klasöründe bu isimde dosyalar olduğundan emin ol veya yolunu düzelt!
        kategoriler = [
            ("Bluz", "visual/3hafta/resimler/ikon/bluz_ikon.png"),
            ("Elbise", "visual/3hafta/resimler/ikon/elbise_ikon.png"),
            ("Gömlek", "visual/3hafta/resimler/ikon/gomlek_ikon.png"),
            ("Ceket", "visual/3hafta/resimler/ikon/ceket_ikon.png"),
            ("Pantolon", "visual/3hafta/resimler/ikon/pantolon_ikon.png"),
            ("Etek", "visual/3hafta/resimler/ikon/etek_ikon.png"),
            ("Korse", "visual/3hafta/resimler/ikon/korse_ikon.png"),
            ("Kemer", "visual/3hafta/resimler/ikon/kemer_ikon.png"),
            ("Çanta", "visual/3hafta/resimler/ikon/canta_ikon.png")
        ]

        for ad, resim_yolu in kategoriler:
            # Her kategori için bir dikey kutu
            kart_kutusu = QVBoxLayout()
            # Resimli Buton (QToolButton bunun için en iyisidir)
            btn = QToolButton()
            btn.setText(ad)
            # Eğer resim varsa yükle, yoksa ikon koyma hata vermesin
            if os.path.exists(resim_yolu):
                btn.setIcon(QIcon(resim_yolu))
            btn.setIconSize(QSize(100, 100))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # Yazı ikonun altında olsun
            btn.setFixedSize(140, 180)
            # Trendyol Tarzı Hover (Üzerine gelince renk değişimi) ve Yuvarlak Köşeler
            btn.setStyleSheet("""
                QToolButton {
                    border: 2px solid #f0f0f0;
                    border-radius: 15px;
                    background-color: white;
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                }
                QToolButton:hover {
                    border: 2px solid #ff6700;
                    background-color: #fffaf0;
                }
            """)
            # BUTONA TIKLAYINCA: Hazır Ürünler (Stok) sekmesine geçiş yapılacak
            # lambda kullanıyoruz ki fonksiyon hemen çalışmasın, tıklandığında çalışsın
            btn.clicked.connect(lambda checked=False, k=ad: self.kategori_buton_tiklandi(k))
            kategori_layout.addWidget(btn)
        ana_layout.addLayout(kategori_layout)
        ana_layout.addStretch() # Elemanları yukarı yasla, altta boşluk bırak
    def kategori_buton_tiklandi(self, kategori):
        # 1. Stok sekmesine git (Burası çalışıyor)
        self.tabs.setCurrentIndex(1) 
        
        # Şimdilik bunu kontrol ederek çalıştıralım:
        if hasattr(self, 'stoklari_filtrele'):
            self.stoklari_filtrele(kategori)
        else:
            print(f"Bilgi: {kategori} için filtreleme fonksiyonu henüz eklenmemiş.")
    def kategoriye_git(self, kategori_adi):
        # Sekmeyi 'Stok Durumu' (Index: 1) yap
        self.tabs.setCurrentIndex(1)
        # İleride buraya o kategoriyi otomatik filtreleyen kod da ekleyebiliriz!
        print(f"{kategori_adi} kategorisine gidiliyor...")
    def ozel_tasarim_tasarimi(self):
        # Ana yatay yerleşim (Sol Menü | Sağ Önizleme)
        ana_ozel_layout = QHBoxLayout(self.sekme_ozel_tasarim)

        # --- SOL TARAF: SEÇENEKLER ---
        secenekler_paneli = QVBoxLayout()
        secenekler_paneli.setSpacing(15)
        
        baslik = QLabel("✨ TASARIM SİHİRBAZI")
        baslik.setStyleSheet("font-size: 20px; font-weight: bold; color:#ff6700;")
        secenekler_paneli.addWidget(baslik)
        #BU KISIM YAPAY ZEKA İLE KOORDİNE YÜRÜTÜLMEZSE BAZI SEÇENEKLE RSADECE SEÇİLİR FAKAT KULLANICIYA TAHMİNİ 
        #GÖRDEL GÖSTERİLEMEZ
        # Üst Seçimi
        secenekler_paneli.addWidget(QLabel("👕 Üst Kesim:"))
        secenekler_paneli.addWidget(QLabel("Etek tasarlamak istiyorsanız üst kategorisinde tamamen yok seçiniz:"))
        secenekler_paneli.addWidget(QLabel("Yaka tipi:"))
        self.combo_yaka = QComboBox()
        self.combo_yaka.addItems(["Yok","Bisiklet","V","Kare","Degaje","Madonna","Tek Omuz","Polo","Hakim(Mandarin)","Kayık","Straplez","Polo"])
        secenekler_paneli.addWidget(self.combo_yaka)

        secenekler_paneli.addWidget(QLabel("Kol Tipİ:"))
        self.combo_kol = QComboBox()
        self.combo_kol.addItems(["Yok", "Karpuz Kol","Çan/İspanyol Kol","Volanlı Kol","Reglan Kol","Düşük Omuz","Yarasa Kol","Askılı"])
        secenekler_paneli.addWidget(self.combo_kol)

        secenekler_paneli.addWidget(QLabel("Kol Uzunluğu:"))
        self.combo_kol_uzunlugu = QComboBox()
        self.combo_kol_uzunlugu.addItems(["Yok", "Kısa", "Truvakar(3/4)", "Uzun"])
        secenekler_paneli.addWidget(self.combo_kol_uzunlugu)

        secenekler_paneli.addWidget(QLabel("Askı Tipi:"))
        self.combo_askı = QComboBox()
        self.combo_askı.addItems(["Yok", "Kalın ", "Spagetti(İnce)", "Şeffaf", "Halter","Çapraz"])
        secenekler_paneli.addWidget(self.combo_askı)

        # Etek Seçimi
        secenekler_paneli.addWidget(QLabel("👗 Etek Boyutu:"))
        self.combo_etek_boyu = QComboBox()
        self.combo_etek_boyu.addItems(["Yok", "Mini", "Midi", "Maxi"])
        secenekler_paneli.addWidget(self.combo_etek_boyu)

        secenekler_paneli.addWidget(QLabel("👗 Etek Modeli:"))
        self.combo_etek_modeli = QComboBox()
        self.combo_etek_modeli.addItems(["Kalem","A Kesim","Akordiyon","Kat Kat Fırfırlı","Balon","Kloş","Pileli","Asimetrik",
        "Volanlı Balık","Yırtmaçlı","Önü kısa arkası uzun"])
        secenekler_paneli.addWidget(self.combo_etek_modeli)

        # Renk Seçimi
        secenekler_paneli.addWidget(QLabel("🎨 Renk Paleti:"))
        self.combo_renk = QComboBox()
        self.combo_renk.addItems(["Beyaz", "Siyah", "Kırmızı", "Mavi","Mint Yeşili", "Kahverengi","Bordo","Mor"])
        secenekler_paneli.addWidget(self.combo_renk)

        secenekler_paneli.addWidget(QLabel("Desen:"))
        self.combo_desen = QComboBox()
        self.combo_desen.addItems(["Yok","Ekose","Çiçek(Mini)","Çiçek(Orta)","Çiçek(Maxi)","Puantiyeli","Çizgili(Dikey)","Çizgili(Yatay)","Etnik","Şal","Jakarlı","Brokar"])
        secenekler_paneli.addWidget(self.combo_desen)

        secenekler_paneli.addWidget(QLabel("Kumaş Türü:"))
        self.combo_kumas = QComboBox()
        self.combo_kumas.addItems(["Pamuk","Keten","Krep","Kot","Saten","Şifon","Kadife","Dantel","Triko","Likra"])
        secenekler_paneli.addWidget(self.combo_kumas)

        # Tasarla Butonu
        # ... (Yukarıdaki ComboBox ve Tasarla Butonu kodların aynen kalıyor)

        # Tasarla Butonu
        self.tasarla_btn = QPushButton("🧵 TASARIMI OLUŞTUR")
        self.tasarla_btn.setStyleSheet("background-color: #ff6700; color: white; height: 40px; font-weight: bold;")
        self.tasarla_btn.clicked.connect(self.tasarimi_guncelle)
        secenekler_paneli.addWidget(self.tasarla_btn)

        # === YENİ BUTONLAR BURAYA GELECEK (addStretch satırının yukarısına) ===
        # 1. Buton: Bilgisayara Kaydetme Butonu (Yeşil)
        self.btn_kaydet = QPushButton("💾 TASARIMI BİLGİSAYARA KAYDET")
        self.btn_kaydet.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 35px; margin-top: 10px;")
        self.btn_kaydet.clicked.connect(self.tasarimi_resim_olarak_kaydet) 
        secenekler_paneli.addWidget(self.btn_kaydet)

        # 2. Buton: Yazıcıya Gönderme Butonu (Koyu Kahve/Bohem)
        self.btn_yazdir = QPushButton("🖨️ NİHAİ TASARIMI YAZDIR / ÇIKTI AL")
        self.btn_yazdir.setStyleSheet("background-color: #7E6B5A; color: white; font-weight: bold; height: 35px;")
        self.btn_yazdir.clicked.connect(self.tasarimi_yaziciya_gonder) 
        secenekler_paneli.addWidget(self.btn_yazdir)

        # Esneklik payı ve sağ taraftaki önizleme yerleşimi en sonda kalmalı
        secenekler_paneli.addStretch()
        ana_ozel_layout.addLayout(secenekler_paneli, 1)

        # --- SAĞ TARAF: DİNAMİK ÖNİZLEME ---
        self.tasarim_alani = QLabel()
        self.tasarim_alani.setFixedSize(500, 700)
        self.tasarim_alani.setStyleSheet("border: 2px solid #ddd; background-color: #ffffff; border-radius: 10px;")
        self.tasarim_alani.setAlignment(Qt.AlignCenter)
        ana_ozel_layout.addWidget(self.tasarim_alani, 2)
    def canli_arama(self):
        aranan = self.arama_cubugu.text().lower()
        for satir in range(self.stok_tablo.rowCount()):
            satir_gorunsun_mu = False
            for sutun in range(self.stok_tablo.columnCount()):
                item = self.stok_tablo.item(satir, sutun)
                if item and aranan in item.text().lower():
                    satir_gorunsun_mu = True
                    break
            self.stok_tablo.setRowHidden(satir, not satir_gorunsun_mu)
    def stok_listele_ozel(self, veriler):
        self.stok_tablo.setRowCount(0)
        for satir_no, satir_veri in enumerate(veriler):
            self.stok_tablo.insertRow(satir_no)
            for sutun_no,veri in enumerate(satir_veri):
                self.stok_tablo.setItem(satir_no,sutun_no,QTableWidgetItem(str(veri)))
    def stoklari_filtrele(self, kategori_adi):
        # 1. Arama çubuğuna kategori adını yazdır
        # Screenshot 2026-05-13 114056.png'de en üstteki 'Ürün adı veya kategori ara...' yazan yer
        self.arama_cubugu.setText(kategori_adi) 
        
        # 2. Mevcut arama fonksiyonunu tetikle
        # Senin arama çubuğuna yazı yazınca çalışan fonksiyonunun adı muhtemelen 'stok_ara'
        if hasattr(self, 'stok_ara'):
            self.stok_ara()
    def tasarimi_guncelle(self):
        from PyQt5.QtGui import QPainter, QPixmap
        from PyQt5.QtCore import Qt

        # 1. MANKENİ YÜKLE
        manken_yolu = "visual/3hafta/resimler/manken_bos.png"
        manken = QPixmap(manken_yolu)
        
        if manken.isNull():
            self.tasarim_alani.setText("HATA: Manken bulunamadı!")
            return

        # Tuval ve Manken Çizimi
        tuval = QPixmap(manken.size())
        tuval.fill(Qt.transparent)
        painter = QPainter(tuval)
        painter.drawPixmap(0, 0, manken)
        
        manken_merkez = manken.width() / 2 # Sabit merkez çizgimiz

        def temizle(metin):
            return metin.lower().replace(' ', '_').replace('ı', 'i').replace('ğ', 'g').replace('ş', 's').replace('ç', 'c').replace('ö', 'o').replace('ü', 'u')

        # --- 2. ÜST PARÇA (Yaka) ---
        yaka_secim = self.combo_yaka.currentText()
        if yaka_secim != "Yok":
            yol_ust = f"visual/3hafta/resimler/{temizle(yaka_secim)}.png"
            pix_ust = QPixmap(yol_ust)
            if not pix_ust.isNull():
                pix_ust = pix_ust.scaledToWidth(240, Qt.SmoothTransformation)
                x_ust = manken_merkez - (pix_ust.width() / 2)
                painter.drawPixmap(int(x_ust), 70, pix_ust)

        # --- 3. ALT PARÇA (Etek) ---
        alt_secim = self.combo_etek_modeli.currentText()
        if alt_secim != "Yok":
            # Klasördeki 'alt_' eklerini sildiğimiz için temizle(alt_secim) doğrudan aratılıyor
            yol_alt = f"visual/3hafta/resimler/{temizle(alt_secim)}.png"
            
            pix_alt = QPixmap(yol_alt)
            if not pix_alt.isNull():
                pix_alt = pix_alt.scaledToWidth(430, Qt.SmoothTransformation)
                x_alt = manken_merkez - (pix_alt.width() / 2)
                y_alt_koordinat = 240 
                painter.drawPixmap(int(x_alt), y_alt_koordinat, pix_alt)
                
        painter.end()
        self.tasarim_alani.setPixmap(tuval.scaled(self.tasarim_alani.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def tasarimi_resim_olarak_kaydet(self):
        from PyQt5.QtWidgets import QFileDialog
        # Kullanıcıya nereye kaydedeceğini soran pencereyi açıyoruz
        dosya_yolu, _ = QFileDialog.getSaveFileName(self, "Tasarımı Kaydet", "", "Resim (*.png)")
        
        # Nokta atışı sağ taraftaki manken alanının görüntüsünü alıp kaydediyoruz
        if dosya_yolu and hasattr(self, 'tasarim_alani'): 
            self.tasarim_alani.grab().save(dosya_yolu)

    def tasarimi_yaziciya_gonder(self):
        from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
        printer = QPrinter()
        
        # Kullanıcı yazdırma penceresinde 'Tamam' derse, doğrudan manken alanını yazdırıyoruz
        if QPrintDialog(printer, self).exec_() and hasattr(self, 'tasarim_alani'): 
            self.tasarim_alani.grab().save(printer)
# ÇALIŞTIRMA
if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AtolyeApp()
    pencere.show()
    sys.exit(app.exec_())