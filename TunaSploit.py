import nmap3
import subprocess
import re
import socket

# Nmap3 kütüphanesini kullanarak nmap taraması yapma
nmap = nmap3.Nmap()

# Ağdaki cihazların IP adreslerini bulma
def agdaki_cihazlari_bul():
    # Kendi IP adresimizi bul
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    
    # Ağ aralığını belirle
    ip_base = ".".join(local_ip.split('.')[:-1]) + '.'
    ip_listesi = [ip_base + str(i) for i in range(1, 255)]
    
    # Ağdaki cihazları tara
    cihazlar = nmap.scan_top_ports(ip_listesi, args="-sn")
    
    # Aktif cihazların IP adreslerini listele
    aktif_cihazlar = [cihaz for cihaz in cihazlar if cihazlar[cihaz]['state']['state'] == 'up']
    
    return aktif_cihazlar

# Kullanıcıdan seçim yapmasını iste ve IP adresini döndür
def ip_secimi_yap(aktif_cihazlar):
    # Cihazları numaralandır ve ekrana yazdır
    for num, ip in enumerate(aktif_cihazlar, start=1):
        print(f"{num}: {ip}")
    
    # Kullanıcıdan bir numara seçmesini iste
    secim = int(input("Lütfen bir cihaz numarası girin: "))
    
    # Seçilen IP adresini döndür
    return aktif_cihazlar[secim - 1]

# Agresif tarama ve Metasploit arama fonksiyonu
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
            process = subprocess.Popen(msf_arama_komutu, shell=True, stdout=subprocess.PIPE)
            sonuc, hata = process.communicate()
            if hata:
                print(f"Hata: {hata}")
            else:
                print(f"Port {port} için bulunan modüller:")
                print(sonuc.decode())

# Ana fonksiyon
if __name__ == "__main__":
    aktif_cihazlar = agdaki_cihazlari_bul()
    secilen_ip = ip_secimi_yap(aktif_cihazlar)
    agresif_tarama_ve_metasploit_arama(secilen_ip)
