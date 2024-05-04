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
    arp_scan_tara_ve_yazdir()
    # Kullanıcıdan IP adresi al
    secilen_ip = input("Lütfen agresif tarama yapılacak IP adresini girin: ")
    agresif_tarama_ve_metasploit_arama(secilen_ip)
