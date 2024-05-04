import subprocess
import random
import signal
import sys

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

# TunaSploit shell'i başlat
def tunasploit_shell():
    while True:
        komut = input("TunaSploit> ")
        if komut == 'exit':
            break
        elif komut == 'banner':
            banner_yukle()
        elif komut == 'opsiyon':
            print("1: arp-scan\n2: nmap taraması\n3: dirb\n4: metasploit taraması")
            secim = input("Seçiminizi girin: ")
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
        else:
            print(f"'{komut}' komutu tanınmadı.")

# nmap ile tarama yap ve sonuçları ekrana yazdır
def nmap_tarama(ip, parametreler=None):
    try:
        komut = ['nmap', ip]
        if parametreler:
            komut = ['nmap'] + parametreleri.split() + [ip]
        print(f"{' '.join(komut)} komutu çalıştırılıyor...")
        sonuc = subprocess.run(komut, text=True, capture_output=True)
        print(sonuc.stdout)
        if "80/tcp open" in sonuc.stdout:
            dirb_calistir = input("80 portu açık algılandı. dirb aracını çalıştırmak ister misiniz? (E/H): ")
            if dirb_calistir.lower() == 'e':
                dirb_parametreleri = input("dirb için ekstra parametreler girin (örn: -w -l), yoksa boş bırakın: ")
                dirb_calistir(ip, dirb_parametreleri)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

# dirb ile dizin taraması yap ve arka planda çalıştır
def dirb_calistir(ip, parametreler=None):
    komut = ['dirb', f"http://{ip}"]
    if parametreler:
        komut += parametreler.split()
    print(f"{' '.join(komut)} komutu arka planda çalıştırılıyor...")
    subprocess.Popen(komut)

# Metasploit'te arama yap
def metasploit_arama():
    arama_sorgusu = input("Lütfen Metasploit'te aramak istediğiniz versiyonu girin: ")
    try:
        print(f"msfconsole -x 'search name:{arama_sorgusu}; exit' komutu çalıştırılıyor...")
        sonuc = subprocess.run(['msfconsole', '-q','-x', f"search name:{arama_sorgusu}; exit"], text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

# Ana fonksiyon
if __name__ == "__main__":
    tunasploit_shell()
