#!/usr/bin/env python3

from colorama import Fore, Back, Style
import socket, os, sys, struct, concurrent.futures, subprocess
import signal
import os

def handler(sig, frame):
    os.system("clear")
    print(Fore.RED+Style.DIM+"\n\n[+] Saliendo...\n"+Fore.WHITE+Style.NORMAL)
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

# Crear dos listas vacías para guardar los puertos abiertos de TCP y UDP
tcp_ports = []
udp_ports = []

def scan_tcp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1) # Reducir el tiempo de espera a 0.1 segundos
    try:
        s.connect((host, port))
        print(Fore.BLUE+Style.DIM+f"[+] El puerto {port} TCP está abierto")
        # Añadir el puerto a la lista de TCP
        tcp_ports.append(str(port))
        s.close()
    except:
        pass

def scan_udp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1) # Reducir el tiempo de espera a 0.1 segundos
    if port == 53: # Si el puerto es 53, enviar una consulta DNS
        data = struct.pack("!HHHHHH", 1, 0, 1, 0, 0, 0) # ID = 1, flags = 0, QDCOUNT = 1, ANCOUNT = 0, NSCOUNT = 0, ARCOUNT = 0
        data += b"\x03www\x07example\x03com\x00" # QNAME = www.example.com en formato de etiquetas
        data += struct.pack("!HH", 1, 1) # QTYPE = A (1), QCLASS = IN (1)
    else: # Si el puerto no es 53, enviar un mensaje vacío
        data = b""
    s.sendto(data, (host, port))
    try:
        data, addr = s.recvfrom(1024)
        print(Fore.YELLOW+f"[+] El puerto {port} UDP está abierto")
        # Añadir el puerto a la lista de UDP
        udp_ports.append(str(port))
        s.close()
    except socket.timeout:
        pass
    except socket.error as e:
        print(f"Error en el puerto {port} UDP: {e}")
        pass

if __name__ == '__main__':
    
    os.system("clear && figlet Host Scan | lolcat")
    
    host = input(Fore.MAGENTA+Style.BRIGHT+"Introduce la IP a analizar: "+Fore.WHITE+Style.NORMAL)
    print("\n")
    
    # Modificar los hilos máximos que se pueden ejecutar en el sistema
    os.system("ulimit -n 5100")
    
    # Crear un pool de hilos con un máximo de 5000
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5000)

    # Usar el método map para asignar cada puerto a un hilo del pool
    executor.map(scan_tcp, [host]*65535, range(1,65536))
    print("\n")
    executor.map(scan_udp, [host]*65535, range(1,65536))

    # Esperar a que todos los hilos terminen
    executor.shutdown(wait=True)

    print(Fore.LIGHTCYAN_EX+Style.BRIGHT+"\n[+] ¡El escaneo ha terminado!")

    # Preguntar al usuario si quiere copiar los puertos TCP
    respuesta_tcp = input(Fore.LIGHTMAGENTA_EX+Style.NORMAL+"\n¿Copiar los puertos TCP? (y/n): ")

    if respuesta_tcp == "y":
        # Convertir la lista de puertos TCP en una cadena separada por comas
        tcp_ports_str = ",".join(tcp_ports)
        # Ejecutar el comando xclip con los puertos TCP como entrada estándar
        subprocess.run(["xclip", "-sel", "clip"], input=tcp_ports_str.encode(), check=True)
        print(Fore.GREEN+Style.BRIGHT+"\n[+] ¡Puertos TCP copiados al portapapeles!")
    else:
        pass

    # Preguntar al usuario si quiere copiar los puertos UDP
    respuesta_udp = input(Fore.LIGHTMAGENTA_EX+Style.NORMAL+"\n¿Desea copiar los puertos UDP? (y/n): ")

    if respuesta_udp == "y":
        # Convertir la lista de puertos UDP en una cadena separada por comas
        udp_ports_str = ",".join(udp_ports)
        # Ejecutar el comando xclip con los puertos UDP como entrada estándar
        subprocess.run(["xclip", "-sel", "clip"], input=udp_ports_str.encode(), check=True)
        print(Fore.LIGHTGREEN_EX+Style.BRIGHT+"\n[+] ¡Puertos UDP copiados al portapapeles!\n"+Fore.WHITE+Style.NORMAL)
    else:
        print(Fore.RED+Style.DIM+"\n[-] No se copian los puertos UDP\n"+Style.NORMAL+Fore.WHITE)
