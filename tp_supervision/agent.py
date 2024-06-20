import socket
import json
import platform
import os
import time
import uuid
import psutil

# Adresse IP et port du serveur
SERVER_HOST = 'localhost'
SERVER_PORT = 12345

def get_processor_info():
    cpu_info = {
        "type": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "frequency": psutil.cpu_freq().max
    }
    return cpu_info

def get_memory_info():
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()
    return {
        "total_memory": memory_info.total,
        "used_memory": memory_info.used,
        "percentage": memory_info.percent,
        "cache": memory_info.cached,
        "swap_total": swap_info.total,
        "swap_used": swap_info.used,
        "swap_percentage": swap_info.percent
    }

def get_disk_info():
    disk_info = psutil.disk_usage('/')
    return {
        "total_disk": disk_info.total,
        "used_disk": disk_info.used,
        "percentage": disk_info.percent
    }

def get_os_info():
    return {
        "system": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def determine_machine_type():
    if os.path.exists('/sys/class/dmi/id/product_name'):
        with open('/sys/class/dmi/id/product_name', 'r') as file:
            product_name = file.read().strip()
        if 'laptop' in product_name.lower():
            return 'Laptop'
        elif 'desktop' in product_name.lower():
            return 'Desktop'
        else:
            return 'Unknown'
    return 'Unknown'

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

def get_system_load():
    cpu_load_per_core = psutil.cpu_percent(interval=1, percpu=True)
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()
    disk_info = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()

    return {
        "used_memory": memory_info.used,
        "memory_usage": memory_info.percent,
        "cache": memory_info.cached,
        "swap_total": swap_info.total,
        "swap_used": swap_info.used,
        "swap_percentage": swap_info.percent,
        "used_disk": disk_info.used,
        "disk_percentage": disk_info.percent,
        "cpu_usage_per_core": cpu_load_per_core,
        "net_bandwidth": {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv
        },
    }

def get_active_processes_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

def gather_initial_system_info():
    system_info = {
        "processor": get_processor_info(),
        "memory": get_memory_info(),
        "disk": get_disk_info(),
        "os": get_os_info(),
        "machine_type": determine_machine_type(),
        "mac_address": get_mac_address()
    }
    return system_info

def send_data_to_server(socket_conn, data):
    try:
        message = json.dumps(data) + '\n'
        print(f"Envoi des données: {message}")
        socket_conn.sendall(message.encode('utf-8'))
        print("Données envoyées au serveur")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données: {e}")

def main():
    # Établir la connexion socket une fois
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"Tentative de connexion au serveur {SERVER_HOST}:{SERVER_PORT}")
        s.connect((SERVER_HOST, SERVER_PORT))
        print("Connexion établie")

        # Récupérer les informations initiales
        print("Récupération des informations initiales du système")
        initial_info = gather_initial_system_info()
        data = {"initial_info": initial_info}
        send_data_to_server(s, data)
        print("\n\nInformations initiales envoyées au serveur : {}".format(data))

        # Boucle pour récupérer la charge toutes les 30 secondes
        while True:
            print("Récupération de la charge du système")
            system_load = get_system_load()
            active_processes = get_active_processes_info()
            system_load["active_processes"] = len(active_processes)
            data = {
                "system_load": system_load,
            }
            send_data_to_server(s, data)
            print(f"\n\nEnvoyée au serveur: Charge du système: {system_load}")
            print("Pause de 30 secondes")
            time.sleep(5)  # Pause de 30 secondes

if __name__ == "__main__":
    main()
