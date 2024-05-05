import subprocess
import random
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

def sexy_banner_yukle():
    with open('sexyfile.txt', 'r', encoding='utf-8') as file:
        banners = file.read().strip().split('---')
    secilen_banner = random.choice(banners)
    print(secilen_banner)

# Banner yükleme fonksiyonu
def banner_yukle():
    with open('banners.txt', 'r', encoding='utf-8') as file:
        banners = file.read().strip().split('---')
    secilen_banner = random.choice(banners)
    print(secilen_banner)

# Ağdaki cihazları tara ve ekrana yazdır
def ag_cihazlarini_tara():
    print("Lütfen tarama aracını seçin:")
    print("1: arp-scan")
    print("2: netdiscover")
    secim = input("Seçiminiz (1/2): ")
    if secim == '1':
        try:
            print("arp-scan komutu çalıştırılıyor...")
            sonuc = subprocess.check_output(['arp-scan', '-l'], text=True)
            print(sonuc)
        except subprocess.CalledProcessError as e:
            print(f"Hata: {e}")
    elif secim == '2':
        try:
            print("netdiscover komutu çalıştırılıyor...")
            sonuc = subprocess.check_output(['netdiscover'], text=True)
            print(sonuc)
        except subprocess.CalledProcessError as e:
            print(f"Hata: {e}")

# Exploit arama fonksiyonu
def exploit_arama():
    print("Lütfen arama aracını seçin:")
    print("1: Metasploit")
    print("2: Searchsploit")
    secim = input("Seçiminiz (1/2): ")
    if secim == '1':
        metasploit_arama()
    elif secim == '2':
        searchsploit_arama()

# Searchsploit ile arama yap
def searchsploit_arama():
    arama_sorgusu = input("Lütfen Searchsploit'te aramak istediğiniz terimi girin: ")
    try:
        print(f"searchsploit {arama_sorgusu} komutu çalıştırılıyor...")
        sonuc = subprocess.check_output(['searchsploit', arama_sorgusu], text=True)
        print(sonuc)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# Dizin taraması yap ve sonuçları kaydet
def dizin_taramasi(ip):
    print("Lütfen dizin tarama aracını seçin:")
    print("1: dirb")
    print("2: gobuster")
    secim = input("Seçiminiz (1/2): ")
    if secim == '1':
        dirb_calistir(ip)
    elif secim == '2':
        gobuster_calistir(ip)

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

# gobuster ile dizin taraması yap ve sonuçları kaydet
def gobuster_calistir(ip, gobuster_parametreleri=None):
    komut = ['gobuster', 'dir', '-u', f"http://{ip}"]
    if gobuster_parametreleri:
        komut += gobuster_parametreleri.split()
    print(f"{' '.join(komut)} komutu çalıştırılıyor...")
    process = subprocess.Popen(komut, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    tarama_sonuclari[ip] = []
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output and ('200' in output or '301' in output):  # Sadece başarılı sonuçları kaydet
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
        '1': 'Ağdaki cihazları tarama:',
        '2': 'Port tarayıcı:',
        '3': 'Dizin taraması',
        '4': 'Explotations search',
        '5': 'Kayıt alanı'
    }
    while True:
        komut = input("TunaSploit> ")
        if komut == 'exit':
            break
        elif komut == 'clear':
            clear_screen()
        elif komut == 'banner':
            banner_yukle()
        elif komut == 'sexy banner':
            sexy_banner_yukle()
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
        ag_cihazlarini_tara()
    elif secim == '2':
        hedef_ip = input("Lütfen nmap taraması yapılacak hedef IP adresini girin: ")
        nmap_parametreleri = input("Eğer ekstra nmap taraması parametreleri kullanmak isterseniz girin (örn: -A -T4), yoksa boş bırakın: ")
        nmap_tarama(hedef_ip, nmap_parametreleri)
    elif secim == '3':
        hedef_ip = input("Lütfen dizin taraması yapılacak hedef IP adresini girin: ")
        dizin_taramasi(hedef_ip)
    elif secim == '4':
               exploit_arama()
    else:
        print(f"'{secim}' için bir işlem tanımlanmamış.")

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
            dirb = input("80 portu açık algılandı. dirb aracını çalıştırmak ister misiniz? (E/H): ")
            if dirb.lower() == 'e':
                dirb_parametreleri = input("dirb için ekstra parametreler girin (örn: -w -l), yoksa boş bırakın: ")
                dirb_calistir(ip, dirb_parametreleri)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e}")

# Ana fonksiyon
if __name__ == "__main__":
    tunasploit_shell()
