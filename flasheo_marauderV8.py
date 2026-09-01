#!/usr/bin/env python3
import subprocess
import sys
import os
import glob

FIRMWARE_BIN = ""
FLASH_ADDR = "0x0"
BAUD_RATES = ["921600", "115200"]


def find_usb_port():
    ports = glob.glob("/dev/ttyUSB*")
    if not ports:
        print("[!] No se encontró ningún puerto /dev/ttyUSB*. ¿Está conectado el ESP32?")
        sys.exit(1)
    print(f"[+] Puerto detectado: {ports[0]}")
    return ports[0]


def check_permissions(port):
    if not os.access(port, os.R_OK | os.W_OK):
        print(f"[!] No tienes permisos para acceder a {port}.")
        print("    Solución: añade tu usuario a dialout y uucp:")
        print("    sudo usermod -a -G dialout $USER")
        print("    sudo usermod -a -G uucp $USER")
        print("    Luego cierra sesión y vuelve a entrar.")
        sys.exit(1)
    print("[+] Permisos correctos sobre el puerto.")


def check_bootloader(port):
    print("[*] Verificando si el ESP32 está en modo bootloader...")
    try:
        subprocess.check_call(["esptool", "--port", port, "chip_id"],
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        print("[+] ESP32 detectado en modo bootloader.")
    except subprocess.CalledProcessError:
        print("[!] El ESP32 no responde. Ponlo en modo bootloader:")
        print("    1. Mantén pulsado BOOT")
        print("    2. Pulsa RESET")
        print("    3. Suelta BOOT")
        sys.exit(1)


def flash_firmware(port):
    if not os.path.isfile(FIRMWARE_BIN):
        print(f"[!] No se encuentra el archivo de firmware: {FIRMWARE_BIN}")
        sys.exit(1)

    for baud in BAUD_RATES:
        print(f"[*] Intentando flashear a {baud} baud...")
        cmd = [
            "esptool",
            "--chip", "esp32",
            "--port", port,
            "--baud", baud,
            "write-flash",
            FLASH_ADDR, FIRMWARE_BIN
        ]

        print("    Comando:", " ".join(cmd))

        try:
            subprocess.check_call(cmd)
            print("[+] Flash completado correctamente.")
            print("[+] Reinicia el dispositivo para cargar el nuevo firmware.")
            return
        except subprocess.CalledProcessError:
            print(f"[!] Falló a {baud} baud. Probando siguiente velocidad...")

    print("[!] No se pudo flashear el firmware en ninguna velocidad.")
    sys.exit(1)


def main():
    print("[*] Iniciando flasheo automático del ESP32 Marauder V8...")

    port = find_usb_port()
    check_permissions(port)
    check_bootloader(port)
    flash_firmware(port)


if __name__ == "__main__":
    main()
