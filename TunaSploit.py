import subprocess
import random
import signal
import sys

acılısbanner = """ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||T |||u |||n |||a |||S |||p |||l |||o |||i |||t ||
||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|"""
print(acılısbanner)
# SIGINT sinyalini yakalamak için bir handler fonksiyonu tanımlayın
def signal_handler(sig, frame):
    print('Ctrl-C basıldı, program kapatılıyor...')
    sys.exit(0)

# SIGINT sinyalini bu handler'a yönlendirin
signal.signal(signal.SIGINT, signal_handler)

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
        sonuc = subprocess.run(['arp-scan', '-l'], text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

# nmap ile tarama yap ve sonuçları ekrana yazdır
def nmap_tarama(ip, parametreler=None):
    try:
        komut = ['nmap', ip]
        if parametreler:
            komut = ['nmap'] + parametreler.split() + [ip]
        print(f"{' '.join(komut)} komutu çalıştırılıyor...")
        sonuc = subprocess.run(komut, text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

# Metasploit'te arama yap
def metasploit_arama():
    arama_sorgusu = input("Lütfen Metasploit'te aramak istediğiniz versiyonu girin: ")
    try:
        print(f"msfconsole -x 'search name:{arama_sorgusu}; exit' komutu çalıştırılıyor...")
        sonuc = subprocess.run(['msfconsole', '-q','-x', f"search name:{arama_sorgusu}; exit"], text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

if __name__ == "__main__":
    banner_yukle()
    arp_scan_tara_ve_yazdir()
    hedef_ip = input("Lütfen nmap taraması yapılacak hedef IP adresini girin: ")
    nmap_parametreleri = input("Eğer ekstra nmap taraması parametreleri kullanmak isterseniz girin (örn: -A -T4), yoksa boş bırakın: ")
    nmap_tarama(hedef_ip, nmap_parametreleri)
    metasploit_arama()
