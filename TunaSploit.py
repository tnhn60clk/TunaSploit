import nmap3
import subprocess
import re

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

def arp_scan_tara_ve_yazdir():
    # arp-scan ile ağdaki cihazları tara ve ekrana yazdır
    try:
        sonuc = subprocess.check_output(['arp-scan', '-l'], text=True)
        print("Ağdaki cihazlar:")
        for satir in sonuc.split('\n'):
            if satir and not satir.startswith('Interface:'):
                # IP adresini ve MAC adresini ayıkla ve yazdır
                ip_mac = satir.split()[:2]
                if ip_mac:
                    print(f"IP: {ip_mac[0]}, MAC: {ip_mac[1]}")
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

def agresif_tarama(ip):
    # Agresif tarama yap ve sonuçları ekrana yazdır
    print(f"{ip} adresinde agresif tarama başlatılıyor...")
    tarama_sonuclari = nmap.nmap_version_detection(ip)
    print("Tarama Sonuçları:")
    for servis in tarama_sonuclari:
        print(f"Port: {servis['port']}, Servis: {servis['service']['name']}, Ürün: {servis['service'].get('product', 'Bilinmiyor')}, Versiyon: {servis['service'].get('version', 'Bilinmiyor')}")

def metasploit_arama():
    # Kullanıcıdan Metasploit'te arama yapmak istediği versiyonu al
    arama_sorgusu = input("Lütfen Metasploit'te aramak istediğiniz versiyonu girin: ")
    arama_sorgusu = re.escape(arama_sorgusu)
    msf_arama_komutu = f"msfconsole -x 'search name:{arama_sorgusu}; exit'"
    process = subprocess.Popen(msf_arama_komutu, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sonuc, hata = process.communicate()
    if hata:
        print(f"Hata: {hata.decode()}")
    else:
        print("Metasploit Arama Sonuçları:")
        print(sonuc.decode())

if __name__ == "__main__":
    arp_scan_tara_ve_yazdir()
    # Kullanıcıdan IP adresi al
    secilen_ip = input("Lütfen agresif tarama yapılacak IP adresini girin: ")
    agresif_tarama(secilen_ip)
    metasploit_arama()
