import nmap3
import subprocess
import re
import socket

# Banner
banner = """
████████╗██╗   ██╗███╗   ██╗ █████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
╚══██╔══╝██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
   ██║   ██║   ██║██╔██╗ ██║███████║███████╗██████╔╝██║     ██║   ██║██║   ██║   
   ██║   ██║   ██║██║╚██╗██║██╔══██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
   ██║   ╚██████╔╝██║ ╚████║██║  ██║███████║██║     ███████╗╚██████╔╝██║   ██║   
   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
                                                                                 """
print(banner)

# Nmap nesnesi
nmap = nmap3.Nmap()

def arp_scan_tara():
    # arp-scan ile ağdaki cihazları tara
    try:
        sonuc = subprocess.check_output(['arp-scan', '-l'], text=True)
        cihazlar = []
        for satir in sonuc.split('\n'):
            if satir and not satir.startswith('Interface:'):
                # IP adresini ve MAC adresini ayıkla
                ip_mac = satir.split()[:2]
                if ip_mac:
                    cihazlar.append(ip_mac)
        return cihazlar
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")
        return []

def cihaz_secimi_yap(cihazlar):
    # Cihazları numaralandır ve ekrana yazdır
    for num, (ip, mac) in enumerate(cihazlar, start=1):
        print(f"{num}: IP: {ip}, MAC: {mac}")
    
    # Kullanıcıdan bir numara seçmesini iste
    while True:
        try:
            secim = int(input("Lütfen bir cihaz numarası girin: "))
            if 1 <= secim <= len(cihazlar):
                return cihazlar[secim - 1][0]  # IP adresini döndür
            else:
                print("Geçersiz numara, lütfen listedeki numaralardan birini girin.")
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

def agresif_tarama_ve_metasploit_arama(ip):
    # Agresif tarama yap
    print(f"{ip} adresinde agresif tarama başlatılıyor...")
    tarama_sonuclari = nmap.nmap_version_detection(ip)
    
    # Metasploit'te versiyon bilgilerini ara
    print("Metasploit'te uygun modüller aranıyor...")
    for servis in tarama_sonuclari:
        port = servis['port']
        servis_adi = servis['service']['name']
        if 'product' in servis['service']:
            versiyon = servis['service']['product']
            if 'version' in servis['service']:
                versiyon += " " + servis['service']['version']
            arama_sorgusu = f"{servis_adi} {versiyon}"
            arama_sorgusu = re.escape(arama_sorgusu)
            msf_arama_komutu = f"msfconsole -x 'search name:{arama_sorgusu}; exit'"
            process = subprocess.Popen(msf_arama_komutu, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            sonuc, hata = process.communicate()
            if hata:
                print(f"Hata: {hata.decode()}")
            else:
                print(f"Port {port} için bulunan modüller:")
                print(sonuc.decode())

if __name__ == "__main__":
    cihazlar = arp_scan_tara()
    if cihazlar:
        secilen_ip_mac = cihaz_secimi_yap(cihazlar)
        # secilen_ip_mac[0] IP adresini temsil eder
        # secilen_ip_mac[1] MAC adresini temsil eder
        agresif_tarama_ve_metasploit_arama(secilen_ip_mac[0])
    else:
        print("Ağda aktif cihaz bulunamadı.")
