import socket

def port_scan(target_ip, start_port, end_port):
    print("Port taraması başlatılıyor...")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Bağlantı zaman aşımı süresini 1 saniye olarak ayarlayabilirsiniz
        
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Port {port} açık.")
        else:
            print(f"Port {port} kapalı.")
        
        sock.close()

# Port taramasını yapmak istediğiniz hedefin IP adresini girin
target_ip = "hedef_ip_adresi"

# Tarama yapmak istediğiniz port aralığını belirtin
start_port = 1
end_port = 100

# Port taramasını başlatın
port_scan(target_ip, start_port, end_port)
