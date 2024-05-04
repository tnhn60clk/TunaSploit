import subprocess
import random
import signal
import sys

# SIGINT sinyalini yakalamak için bir handler fonksiyonu tanımlayın
def signal_handler(sig, frame):
    print('Program kapatılıyor...')
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

# nmap ile agresif tarama yap ve sonuçları ekrana yazdır
def nmap_agresif_tarama(ip):
    try:
        print(f"nmap -A {ip} komutu çalıştırılıyor...")
        sonuc = subprocess.run(['nmap', '-A', ip], text=True, capture_output=True)
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
    hedef_ip = input("Lütfen nmap agresif tarama yapılacak hedef IP adresini girin: ")
    nmap_agresif_tarama(hedef_ip)
    metasploit_arama()

