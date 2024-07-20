# Hecho por ProjectGD, disfrutalo pa Bv

import os
import platform
import subprocess
import datetime
import threading
import time
from colorama import init, Fore, Style

os.system('title TxD Tools 1.0')

init(autoreset=True)

running_iponline = threading.Event()
running_scannet = threading.Event()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    text = """
   _______  __ ____     ______            __    
  /_  __/ |/ /| __ \\   /_  __/___  ____  / /____
   / /  |   |/ / / /    / / / __ \\/ __ \\/ / ___/
  / /  /   |/ /_/ /    / / / /_/ / /_/ / (__  ) 
 /_/  /_/|_/_____/    /_/  \\____/\\____/_/____/                                                 
         Finalmente esto funciona :,v
               Hora: {}
""".format(datetime.datetime.now().strftime("%H:%M:%S"))

    print(Fore.MAGENTA + text)

def show_menu():
    menu = """
Comandos disponibles:
1. exit - Sale de la consola
2. iponline - Muestra los dispositivos en línea (actualización automática)
3. scannet - Muestra las conexiones de la PC en línea (actualización automática)
4. ping - Hace ping a una dirección IP o dominio
"""
    print(Fore.CYAN + menu)

def exit_console():
    print(Fore.GREEN + "Saliendo de la consola...")
    running_iponline.set() 
    running_scannet.set()
    exit()

def ip_online():
    while not running_iponline.is_set():
        clear_screen()
        print_banner()
        print(Fore.CYAN + "Dispositivos en línea:")
        if platform.system() == "Windows":
            result = subprocess.run("arp -a", shell=True, capture_output=True, text=True)
            print(result.stdout)
        else:
            print(Fore.GREEN + "Este comando se ha simplificado para Windows.")
        time.sleep(1) 

def scan_net():
    while not running_scannet.is_set():
        clear_screen()
        print_banner()
        print(Fore.CYAN + "Conexiones de red activas:")
        if platform.system() == "Windows":
            result = subprocess.run("netstat -an", shell=True, capture_output=True, text=True)
            output = result.stdout
            connections = [line for line in output.splitlines() if "ESTABLISHED" in line]
            for conn in connections:
                print(conn)
        else:
            result = subprocess.run("ss -tunlp", shell=True, capture_output=True, text=True)
            output = result.stdout
            connections = [line for line in output.splitlines() if "ESTABLISHED" in line]
            for conn in connections:
                print(conn)
        time.sleep(1) 

def ping():
    target = input(Fore.GREEN + "Introduce la dirección IP o dominio para hacer ping: ")
    if platform.system() == "Windows":
        subprocess.run(f"ping {target}", shell=True)
    else:
        subprocess.run(f"ping -c 4 {target}", shell=True)

def monitor_commands():
    while True:
        command = input(Fore.GREEN + "txd> ").strip().lower()
        
        if command == "exit":
            exit_console()
        elif command == "iponline":
            if not running_iponline.is_set():
                running_iponline.clear()
                iponline_thread = threading.Thread(target=ip_online)
                iponline_thread.start()
                print(Fore.GREEN + "Comando 'iponline' iniciado. Presiona 'x' para detener.")
            else:
                print(Fore.GREEN + "El comando 'iponline' ya está en ejecución.")
        elif command == "scannet":
            if not running_scannet.is_set():
                running_scannet.clear()
                scannet_thread = threading.Thread(target=scan_net)
                scannet_thread.start()
                print(Fore.GREEN + "Comando 'scannet' iniciado. Presiona 'x' para detener.")
            else:
                print(Fore.GREEN + "El comando 'scannet' ya está en ejecución.")
        elif command == "ping":
            ping()
        elif command == "x":
            if not running_iponline.is_set():
                running_iponline.set()
                clear_screen()
                print_banner()
                show_menu()
                print(Fore.GREEN + "Comando 'iponline' detenido.")
            elif not running_scannet.is_set():
                running_scannet.set()  
                clear_screen()
                print_banner()
                show_menu()
                print(Fore.GREEN + "Comando 'scannet' detenido.")
        else:
            print(Fore.GREEN + "Comando no reconocido, mira el menu dado.")

def main():
    clear_screen()
    print_banner()
    show_menu()
    monitor_commands()

if __name__ == "__main__":
    main()
