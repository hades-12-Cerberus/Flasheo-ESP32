Este proyecto contiene un script en Python  para flashear el firmware en dispositivos ESP32 Marauder.

El script detecta el puerto USB, verifica permisos, comprueba que el dispositivo esta en modo bootloader y ejecuta "esptool" para flashear. 

Requisitos:

- Python3 instalado

- esptool instalado, pip install esptool

- Permisos sobre el puerto /dev/ttyUSB*

  sudo usermod -aG dialout $USER

  sudo usermod -aG uucp $USER

🚀 Uso del script:

1. Clona el repositorio con: git clone https://github.com/hades-12-Cerberus/Flasheo-ESP32.git

2. Descarga el archivo .bin del firmware para tu dispositivo ESP32 y añadelo en la parte de FIRMWARE_BIN = ""

3. Haz el script ejecutable con sudo chmod +x flasheo_marauderV8.py

4. Conecta tu dispositivo ESP32 por USB en modo bootloader 

5. Ejecuta con python3 flasheo_marauderV8.py
