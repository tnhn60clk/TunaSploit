#!/bin/bash

# Python3-pip'in yüklü olup olmadığını kontrol et
if ! command -v pip3 &> /dev/null
then
    echo "pip3 komutu bulunamadı, lütfen önce pip'i yükleyin."
    exit 1
fi

# Gerekli Python kütüphanelerini yükle
echo "nmap3, subprocess ve re kütüphaneleri yükleniyor..."
pip3 install python3-nmap
pip3 install subprocess.run
pip3 install regex

echo "Kütüphaneler başarıyla yüklendi."
