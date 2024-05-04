import subprocess
import random
import signal
import sys
import os
import threading

# Tarama sonuçlarını saklamak için bir sözlük
tarama_sonuclari = {}

try:
    import readline  # Kullanıcı girdisini iyileştirmek için
except ImportError:
    pass  # readline modülü bazı sistemlerde mevcut olmayabilir

# SIGINT sinyalini yakalamak için bir handler fonksiyonu tanımlayın
def signal_handler(sig, frame):
    print('Ctrl-C basıldı, program kapatılıyor...')
    sys.exit(0)

# Ekranı temizleme fonksiyonu
def clear_screen():
    if os.name == 'nt':  # Windows için
        _ = os.system('cls')
    else:  # Mac ve Linux için (os.name: 'posix')
        _ = os.system('clear')

# Banner yükleme fonksiyonu
def banner_yukle():
    with open('banners.txt', 'r', encoding='utf-8') as file:
        banners = file.read().strip().split('---')
    secilen_banner = random.choice(banners)
    print(secilen_banner)

# arp-scan ile ağdaki cihazları tara ve ekrana yazdır
def arp_scan_tara_ve_yazdir():
    try:
        print("arp-scan komutu çalıştırılıyor...")
        sonuc = subprocess.check_output(['arp-scan', '-l'], text=True)
        print(sonuc)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# nmap ile tarama yap ve sonuçları ekrana yazdır
def nmap_tarama(ip, parametreler=None):
    try:
        komut = ['nmap', ip]
        if parametreler:
            komut = ['nmap'] + parametreler.split() + [ip]
        print(f"{' '.join(komut)} komutu çalıştırılıyor...")
        sonuc = subprocess.check_output(komut, text=True)
        print(sonuc)
        if "80/tcp open" in sonuc:
            dirb_calistir = input("80 portu açık algılandı. dirb aracını çalıştırmak ister misiniz? (E/H): ")
            if dirb_calistir.lower() == 'e':
                dirb_parametreleri = input("dirb için ekstra parametreler girin (örn: -w -l), yoksa boş bırakın: ")
                threading.Thread(target=dirb, args=(ip, dirb_parametreleri)).start()
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# dirb ile dizin taraması yap ve sonuçları kaydet
def dirb(ip, parametreleri=None):
    komut = ['dirb', f"http://{ip}"]
    if parametreleri:
        komut += parametreleri.split()
    print(f"{' '.join(komut)} komutu çalıştırılıyor...")
    sonuc = subprocess.run(komut, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tarama_sonuclari[ip] = sonuc.stdout
    print(sonuc.stdout)

# Metasploit'te arama yap
def metasploit_arama():
    arama_sorgusu = input("Lütfen Metasploit'te aramak istediğiniz versiyonu girin: ")
    try:
        print(f"msfconsole -x 'search name:{arama_sorgusu}; exit' komutu çalıştırılıyor...")
        sonuc = subprocess.check_output(['msfconsole', '-q','-x', f"search name:{arama_sorgusu}; exit"], text=True)
        print(sonuc)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# TunaSploit shell'i başlat
def tunasploit_shell():
    opsiyonlar = {
        '1': 'arp-scan',
        '2': 'nmap taraması',
        '3': 'dirb',
        '4': 'metasploit taraması',
        '5': 'dirb sonuçlarını görüntüle'
    }
    while True:
        komut = input("TunaSploit> ")
        if komut == 'exit':
            break
        elif komut == 'clear':
            clear_screen()
        elif komut == 'banner':
            banner_yukle()
        elif komut == 'opsiyon':
            for key, value in opsiyonlar.items():
                print(f"{key}: {value}")
        elif komut == '5':
            dirb_sonuclari_goruntule()
        elif komut in opsiyonlar:
            islem_sec(komut)
        else:
            print(f"'{komut}' komutu tanınmadı.")

# İşlem seçme fonksiyonu
def islem_sec(secim):
    if secim == '1':
        arp_scan_tara_ve_yazdir()
    elif secim == '2':
        hedef_ip = input("Lütfen nmap taraması yapılacak hedef IP adresini girin: ")
        nmap_parametreleri = input("Eğer ekstra nmap taraması parametreleri kullanmak isterseniz girin (örn: -A -T4), yoksa boş bırakın: ")
        nmap_tarama(hedef_ip, nmap_parametreleri)
    elif secim == '3':
        hedef_ip = input("Lütfen dirb taraması yapılacak hedef IP adresini girin: ")
        dirb_parametreleri = input("dirb için ekstra parametreler girin (örn: -w -l), yoksa boş bırakın: ")
        dirb(hedef_ip, dirb_parametreleri)
    elif secim == '4':
        metasploit_arama()

# dirb sonuçlarını görüntüleme fonksiyonu
def dirb_sonuclari_goruntule():
    if not tarama_sonuclari:
        print("Henüz dirb taraması yapılmadı.")
        return
    for index, (ip, sonuc) in enumerate(tarama_sonuclari.items(), start=1):
        print(f"{index}: {ip}")
    secim = input("Görüntülemek istediğiniz tarama numarasını girin: ")
    if secim.isdigit() and int(secim) in range(1, len(tarama_sonuclari) + 1):
        ip = list(tarama_sonuclari.keys())[int(secim) - 1]
        print(tarama_sonuclari[ip])
    else:
        print("Geçersiz seçim.")

# Ana fonksiyon
if __name__ == "__main__":
    tunasploit_shell()
