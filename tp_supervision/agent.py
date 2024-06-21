import socket
import json
import platform
import os
import time
import uuid
import psutil
from datetime import datetime

# Adresse IP et port du serveur
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

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
        "timestamp": datetime.now().isoformat()
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

def save_data_to_file(data, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r+') as f:
            existing_data = json.load(f)
            existing_data.append(data)
            f.seek(0)
            json.dump(existing_data, f)
    else:
        with open(file_path, 'w') as f:
            json.dump([data], f)
    print(f"Données enregistrées dans {file_path}")

def send_data_to_server(socket_conn, data):
    try:
        message = json.dumps(data) + '\n'
        print(f"Envoi des données: {message}")
        socket_conn.sendall(message.encode('utf-8'))
        print("Données envoyées au serveur")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données: {e}")
        return False
    return True

def main():
    last_sent_time = time.time()
    file_index = 1
    file_path = os.path.join(DATA_DIR, f"{file_index}.json")

    # Récupérer les informations initiales
    print("Récupération des informations initiales du système")
    initial_info = gather_initial_system_info()
    save_data_to_file({"initial_info": initial_info}, file_path)
    print("\n\nInformations initiales enregistrées.")

    while True:
        print("Récupération de la charge du système")
        system_load = get_system_load()
        active_processes = get_active_processes_info()
        system_load["active_processes"] = len(active_processes)
        system_load["mac_address"] = get_mac_address()
        data = {
            "system_load": system_load,
        }
        save_data_to_file(data, file_path)
        print(f"\n\nEnregistré: Charge du système: {system_load}")
        print("Pause de 30 secondes")
        time.sleep(5)  # Pause de 30 secondes

        current_time = time.time()
        if current_time - last_sent_time >=  2 *3600:  #2 *3600 Toutes les deux heures
            last_sent_time = current_time
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # print(f"Tentative de connexion au serveur {SERVER_HOST}:{SERVER_PORT}")
                    s.connect((SERVER_HOST, SERVER_PORT))
                    # print("Connexion établie")

                    for filename in sorted(os.listdir(DATA_DIR)):
                        file_path = os.path.join(DATA_DIR, filename)
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                        if send_data_to_server(s, data):
                            os.remove(file_path)
                            print(f"Fichier {file_path} supprimé après envoi réussi")
                        else:
                            print(f"Échec de l'envoi du fichier {file_path}")
                            break
            except Exception as e:
                print(f"Erreur lors de la connexion au serveur: {e}")

            # Mise à jour du chemin de fichier pour les prochaines deux heures
            file_index += 1
            file_path = os.path.join(DATA_DIR, f"{file_index}.json")

if __name__ == "__main__":
    main()
