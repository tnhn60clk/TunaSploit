#!/bin/bash

# Python3-pip'in yüklü olup olmadığını kontrol et
if ! command -v pip3 &> /dev/null
then
    echo "pip3 komutu bulunamadı, lütfen önce pip'i yükleyin."
    exit 1
fi

# Gerekli Python kütüphanelerini yükle
echo "Kütüphaneler yükleniyor..."
pip3 install python3-nmap
pip3 install subprocess.run
pip3 install regex
pip3 install sockets

echo "Kütüphaneler başarıyla yüklendi."
