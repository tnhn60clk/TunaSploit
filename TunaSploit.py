import subprocess
import random
import threading
import sys
import os
import signal

# Tarama sonuçlarını saklamak için bir sözlük
tarama_sonuclari = {}

# CTRL-C sinyali ile güvenli çıkış yapmak için işleyici
def signal_handler(sig, frame):
    print('CTRL-C ile çıkış yapılıyor...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    import readline  # Kullanıcı girdisini iyileştirmek için
except ImportError:
    pass  # readline modülü bazı sistemlerde mevcut olmayabilir

# Ekranı temizleme fonksiyonu
def clear_screen():
    if os.name == 'nt':  # Windows için
        _ = os.system('cls')
    else:  # Mac ve Linux için (os.name: 'posix')
        _ = os.system('clear')

# Program başladığında ekranı temizle
clear_screen()

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
            komut += parametreler.split() + [ip]
        print(f"{' '.join(komut)} komutu çalıştırılıyor...")
        sonuc = subprocess.check_output(komut, text=True)
        print(sonuc)
        if "80/tcp open" in sonuc:
            dirb_calistir = input("80 portu açık algılandı. dirb aracını çalıştırmak ister misiniz? (E/H): ")
            if dirb_calistir.lower() == 'e':
                dirb_parametreleri = input("dirb için ekstra parametreler girin (örn: -w -l), yoksa boş bırakın: ")
                threading.Thread(target=dirb_calistir, args=(ip, dirb_parametreleri)).start()
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# dirb ile dizin taraması yap ve sonuçları kaydet
def dirb_calistir(ip, dirb_parametreleri=None):
    komut = ['dirb', f"http://{ip}"]
    if dirb_parametreleri:
        komut += dirb_parametreleri.split()
    print(f"{' '.join(komut)} komutu çalıştırılıyor...")
    process = subprocess.Popen(komut, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tarama_sonuclari[ip] = []
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output and ('+ ' in output):  # Sadece başarılı sonuçları kaydet
            tarama_sonuclari[ip].append(output.strip())
            print(output.strip())
            sys.stdout.flush()
    rc = process.poll()
    return rc

# dirb sonuçlarını okuma fonksiyonu
def dirb_sonuclari_oku(ip):
    if ip in tarama_sonuclari:
        print(f"{ip} için dirb sonuçları:")
        for sonuc in tarama_sonuclari[ip]:
            print(sonuc)
    else:
        print(f"{ip} için herhangi bir dirb sonucu bulunamadı.")

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
        '5': 'dirb sonuçlarını oku'
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
            hedef_ip = input("Lütfen dirb sonuçlarını okumak istediğiniz hedef IP adresini girin: ")
            dirb_sonuclari_oku(hedef_ip)
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
        dirb_calistir(hedef_ip, dirb_parametreleri)
    elif secim == '4':
        metasploit_arama()

# Ana fonksiyon
if __name__ == "__main__":
    tunasploit_shell()
