import nmap3
import subprocess
import re


nmap = nmap3.Nmap()


hedef_ip = input("Hedef IP adresini girin: ")


def agresif_tarama(ip):
    print(f"{ip} adresinde agresif tarama başlatılıyor...")
    sonuclar = nmap.nmap_version_detection(ip)
    return sonuclar


def metasploit_arama(sonuclar):
    print("Metasploit'te uygun modüller aranıyor...")
    for servis in sonuclar:
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
        else:
            print(f"Port {port} için servis bilgisi bulunamadı.")


if __name__ == "__main__":
    tarama_sonuclari = agresif_tarama(hedef_ip)
    metasploit_arama(tarama_sonuclari)
