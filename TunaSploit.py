import subprocess
import random
import signal
import sys
import os

try:
    import readline  # Kullanıcı girdisini iyileştirmek için
except ImportError:
    pass  # readline modülü bazı sistemlerde mevcut olmayabilir

# SIGINT sinyalini yakalamak için bir handler fonksiyonu tanımlayın
def signal_handler(sig, frame):
    print('Ctrl-C basıldı, program kapatılıyor...')
    sys.exit(0)

# SIGTSTP (ctrl-t) sinyalini yakalamak için bir handler fonksiyonu tanımlayın
def sigtstp_handler(sig, frame):
    print('Ctrl-T basıldı, TunaSploit shell\'ine geri dönülüyor...')
    tunasploit_shell()

# SIGINT ve SIGTSTP sinyallerini bu handler'lara yönlendirin
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTSTP, sigtstp_handler)

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

# TunaSploit shell'i başlat
def tunasploit_shell():
    opsiyonlar = {
        '1': 'arp-scan',
        '2': 'nmap taraması',
        '3': 'dirb',
        '4': 'metasploit taraması'
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
