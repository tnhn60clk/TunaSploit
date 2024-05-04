import subprocess
import random

# Banner
bannerlar = ["""
████████╗██╗   ██╗███╗   ██╗ █████╗ ███████╗██████╗ ██╗      ██████╗ ██╗████████╗
╚══██╔══╝██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
   ██║   ██║   ██║██╔██╗ ██║███████║███████╗██████╔╝██║     ██║   ██║██║   ██║   
   ██║   ██║   ██║██║╚██╗██║██╔══██║╚════██║██╔═══╝ ██║     ██║   ██║██║   ██║   
   ██║   ╚██████╔╝██║ ╚████║██║  ██║███████║██║     ███████╗╚██████╔╝██║   ██║   
   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   
                                                                                 """,""" ███████████                                  █████████            ████            ███   █████   
░█░░░███░░░█                                 ███░░░░░███          ░░███           ░░░   ░░███    
░   ░███  ░  █████ ████ ████████    ██████  ░███    ░░░  ████████  ░███   ██████  ████  ███████  
    ░███    ░░███ ░███ ░░███░░███  ░░░░░███ ░░█████████ ░░███░░███ ░███  ███░░███░░███ ░░░███░   
    ░███     ░███ ░███  ░███ ░███   ███████  ░░░░░░░░███ ░███ ░███ ░███ ░███ ░███ ░███   ░███    
    ░███     ░███ ░███  ░███ ░███  ███░░███  ███    ░███ ░███ ░███ ░███ ░███ ░███ ░███   ░███ ███
    █████    ░░████████ ████ █████░░████████░░█████████  ░███████  █████░░██████  █████  ░░█████ 
   ░░░░░      ░░░░░░░░ ░░░░ ░░░░░  ░░░░░░░░  ░░░░░░░░░   ░███░░░  ░░░░░  ░░░░░░  ░░░░░    ░░░░░  
                                                         ░███                                    
                                                         █████                                   
                                                        ░░░░░                                    """,""" _______  __   __  __    _  _______  _______  _______  ___      _______  ___   _______ 
|       ||  | |  ||  |  | ||   _   ||       ||       ||   |    |       ||   | |       |
|_     _||  | |  ||   |_| ||  |_|  ||  _____||    _  ||   |    |   _   ||   | |_     _|
  |   |  |  |_|  ||       ||       || |_____ |   |_| ||   |    |  | |  ||   |   |   |  
  |   |  |       ||  _    ||       ||_____  ||    ___||   |___ |  |_|  ||   |   |   |  
  |   |  |       || | |   ||   _   | _____| ||   |    |       ||       ||   |   |   |  
  |___|  |_______||_|  |__||__| |__||_______||___|    |_______||_______||___|   |___|  ""","""  .--.            .--.
 """]
secilenbanner = random.choice(bannerlar)
print(secilenbanner)

def arp_scan_tara_ve_yazdir():
    # arp-scan ile ağdaki cihazları tara ve ekrana yazdır
    try:
        print("arp-scan komutu çalıştırılıyor...")
        sonuc = subprocess.run(['arp-scan', '-l'], text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

def nmap_agresif_tarama(ip):
    # nmap ile agresif tarama yap ve sonuçları ekrana yazdır
    try:
        print(f"nmap -A {ip} komutu çalıştırılıyor...")
        sonuc = subprocess.run(['nmap', '-A', ip], text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

def metasploit_arama():
    # Kullanıcıdan Metasploit'te arama yapmak istediği versiyonu al
    arama_sorgusu = input("Lütfen Metasploit'te aramak istediğiniz versiyonu girin: ")
    try:
        print(f"msfconsole -x 'search name:{arama_sorgusu}; exit' komutu çalıştırılıyor...")
        sonuc = subprocess.run(['msfconsole', '-q','-x', f"search name:{arama_sorgusu}; exit"], text=True, capture_output=True)
        print(sonuc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hata: {e.output}")

if __name__ == "__main__":
    arp_scan_tara_ve_yazdir()
    # Kullanıcıdan hedef IP adresi al
    hedef_ip = input("Lütfen nmap agresif tarama yapılacak hedef IP adresini girin: ")
    nmap_agresif_tarama(hedef_ip)
    metasploit_arama()

