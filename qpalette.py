import sys
from PyQt5.QtWidgets import * #Tüm görsel bileşenleri(Buton,Liste,Pencere vb.)içe aktarır.
from PyQt5.QtGui import QPalette, QColor#Renk yönetimi(QColor) ve bir bileşenin tüm renk haritasını tutan
# "palet" yapısı(QPalette)getirir.
from PyQt5.QtCore import Qt#Hizalama veya klavye tuşları gibi temel çekirdek ayarları kontrol etmemizi sağlar.

class Window(QWidget):
    def __init__(self):
        super().__init__()#Miras aldığımız QWidget sınıfının (ata sınıf:parent) temel kurulumunu yapar. 
        #Bu satır olmazsa pencere nesnesi oluşturulamaz
        self.setWindowTitle("Renk Seçici Pro")
        self.setGeometry(100, 100, 400, 300)

        # 1. Arka plan boyama iznini verir.
        self.setAutoFillBackground(True)#Kritik satır! PyQt5 bileşenleri varsayılan olarak arka plan boyamaya 
        #kapalı olabilir. Bu komutla "Ben bu  pencereyi boyayacağım,buna izin ver"demiş oluyoruz.

        # 2. Ana düzeni kurar.
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 3. Liste Kutusu (ListWidget) oluşturur.
        self.listWidget = QListWidget()#Liste kutumuzu oluşturuyoruz.
        renkler = ['Red', 'Green', 'Blue', 'Yellow', 'Pink', 'Orange', 'Cyan', 'Magenta']
        self.listWidget.addItems(renkler)
        
        # --- ÖNEMLİ: Listenin kendi beyazlığını ve çerçevesini kaldırıyoruz ---
        # Bu sayede sadece yazılar görünür, arka plan rengi her yere yayılır.
        self.listWidget.setStyleSheet("background-color: transparent; border: none; font-size: 16px;")#Burası işin makyaj kısmıdır. 
        #CSS mantığıyla çalışır. "background-color: transparent;" ifadesi  listenin kendi varsayılan beyaz arka planını kaldırır ve 
        # saydamlık verir.Böylece pemcerenin kenarları değil tüm ekran seçilen rengi alır.border:none; ifadesi ise listenin etrafındaki siyah
        #çerçeveyi kaldırır. font-size:16px; yazıları biraz daha okunaklı kılar.
        
        # 4. Tıklama olayını bağlar. Sinyal-slot mekanizmasıdır. Kullanıcı listede tıklama yaptığında self.renk_degistir fonksiyonu tetiklenir.
        self.listWidget.clicked.connect(self.renk_degistir)

        # Listeyi ekrana yerleştirir.
        layout.addWidget(self.listWidget)

    def renk_degistir(self):
        # Seçilen rengin adını yakalar.
        renk_adi = self.listWidget.currentItem().text()#O an tıklanan öğrenin metnini alır.

        # Pencere paletini günceller.
        palette = self.palette()#Pemcerenin mevcut renk ayarlarının bir kopyasını alır.
        palette.setColor(QPalette.Window, QColor(renk_adi))#QPalette.Window:"Arka planı değiştir." talimatıdır. 
        #Qcolor(renk_adi): Aldığımız renk adının gerçek bir renk koduna dünüştürür ve bilgisayarın algılamasını sağlar
        self.setPalette(palette)#Hazırladığımız yeni paleti pencereye uygular.
        
        # Terminale bilgi yazar.
        print(f"Sistem Rengi değistirildi yeni renk: {renk_adi}")

# Uygulamayı başlatır.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())