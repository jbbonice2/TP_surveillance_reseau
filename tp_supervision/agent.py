

import socket
import json
import platform
import os
import time
import uuid
import psutil
from datetime import datetime
import subprocess

import requests

# Adresse IP et port du serveur
SERVER_HOST = '192.168.196.52'#192.168.244.43
SERVER_PORT = 12345

DATA_DIR = os.path.join(os.path.expanduser("~"), ".agent_collector/data")


# Vérifier si le répertoire existe, sinon le créer
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_processor_info():
    cpu_info = {
        
        "type": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "frequency": psutil.cpu_freq().max if psutil.cpu_freq() else "N/A"
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
    if platform.system() == "Windows":
        import wmi
        c = wmi.WMI()
        for system in c.Win32_ComputerSystem():
            if system.SystemType.lower().startswith('laptop'):
                return "Laptop"
            elif system.SystemType.lower().startswith('desktop'):
                return "Desktop"
        return "Unknown"
    elif platform.system() == "Linux":
        if os.path.exists('/sys/class/dmi/id/product_name'):
            with open('/sys/class/dmi/id/product_name', 'r') as file:
                product_name = file.read().strip()
            if 'laptop' in product_name.lower():
                return 'Laptop'
            elif 'desktop' in product_name.lower():
                return 'Desktop'
            else:
                return 'Unknown'
    elif platform.system() == "Darwin":
        # MacOS specific logic can be added here if required
        return "Mac"
    return 'Unknown'

def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent
    return -1

def get_uptime():
    return int(time.time() - psutil.boot_time())

def get_boot_time():
    return datetime.fromtimestamp(psutil.boot_time()).isoformat()


def est_connecte_internet(url='http://www.google.com/', timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except requests.ConnectionError:
        return False

def get_shutdown_time():
    if platform.system() == 'Windows':
        try:
            # Querying Windows event log for shutdown events
            cmd = 'wevtutil qe System /q:"*[System[(EventID=1074)]]" /rd:true /c:1 /f:text'
            output = subprocess.check_output(cmd, shell=True, text=True)
            for line in output.splitlines():
                if "TimeCreated" in line:
                    timestamp = line.split('>')[1].split('<')[0]
                    shutdown_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return shutdown_time.isoformat()
        except Exception as e:
            print(f"Erreur lors de la récupération de l'heure d'arrêt: {e}")
            return -1

    elif platform.system() == 'Linux':
        try:
            # Reading the shutdown time from system logs
            cmd = "last -x shutdown | head -1"
            output = subprocess.check_output(cmd, shell=True, text=True)
            parts = output.split()
            if parts:
                # Extracting the necessary parts for the datetime string
                shutdown_time = ' '.join(parts[4:8])
                year = parts[-1]  # Assuming the year is the last part of the log
                if year.isdigit():
                    shutdown_time = f"{shutdown_time} {year}"
                else:
                    year = datetime.now().year
                    shutdown_time = f"{shutdown_time} {year}"
                shutdown_time = datetime.strptime(shutdown_time, '%a %b %d %H:%M %Y')
                return shutdown_time.isoformat()  # Returning in ISO format
        except Exception as e:
            print(f"Erreur lors de la récupération de l'heure d'arrêt: {e}")
            return -1
    return -1

def get_gpu_usage():
    # This function works for systems with NVIDIA GPUs and nvidia-smi installed
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisation du GPU: {e}")
    # Placeholder for other GPUs
    return -1


def get_cpu_temperature():
    temps = psutil.sensors_temperatures()
    if 'coretemp' in temps:
        return temps['coretemp'][0].current
    return -1

def get_screen_resolution():
    if platform.system() == "Windows":
        from screeninfo import get_monitors
        monitors = get_monitors()
        if monitors:
            monitor = monitors[0]
            return f"{monitor.width}x{monitor.height}"
    elif platform.system() == "Linux":
        try:
            import subprocess
            result = subprocess.run(['xrandr'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if '*' in line:
                    resolution = line.split()[0]
                    return resolution
        except Exception as e:
            print(f"Error getting screen resolution: {e}")
    elif platform.system() == "Darwin":
        try:
            import Quartz
            main_monitor = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
            return f"{int(main_monitor.size.width)}x{int(main_monitor.size.height)}"
        except Exception as e:
            print(f"Error getting screen resolution: {e}")
    return "N/A"

def get_system_load():
    internet_enabled = est_connecte_internet()
    cpu_load_per_core = psutil.cpu_percent(interval=1, percpu=True)
    memory_info = psutil.virtual_memory()
    swap_info = psutil.swap_memory()
    disk_info = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    gpu_usage = get_gpu_usage()
    cpu_temp = get_cpu_temperature()

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
        "gpu_usage_percentage": gpu_usage,
        "cpu_temperature": cpu_temp,
        "timestamp": datetime.now().isoformat(),
        'internet_enabled' : internet_enabled
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
        "mac_address": get_mac_address(),
        "screen_resolution": get_screen_resolution(),
        "timestamp": datetime.now().isoformat()
    }
    return system_info

def gather_variable_data():
    variable_data = {
        "battery_percentage": get_battery_info(),
        "uptime": get_uptime(),
        "boot_time": get_boot_time(),
        "shutdown_time": get_shutdown_time(),
        "timestamp": datetime.now().isoformat()
    }
    return variable_data

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


import re

def get_next_file_index(data_dir):
    # Pattern to match filenames with numeric indices
    pattern = re.compile(r"(\d+)\.json$")
    
    # List all files in the data directory
    files = os.listdir(data_dir)
    
    # Extract indices from filenames
    indices = []
    for file in files:
        match = pattern.search(file)
        if match:
            indices.append(int(match.group(1)))
    
    # Determine the next index
    if indices:
        return max(indices) + 1
    else:
        return 1


def main():
    last_sent_time = time.time()
    file_index = get_next_file_index(DATA_DIR)
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
        variable_data = gather_variable_data()
        variable_data["mac_address"] = get_mac_address()
        data = {
            "system_load": system_load,
            "variable_data": variable_data
        }
        save_data_to_file(data, file_path)
        print(f"\n\nEnregistré: Charge du système: {data}")
        print("Pause de 30 secondes")
        time.sleep(5)  # Pause de 30 secondes

        current_time = time.time()
        if current_time - last_sent_time >= 30:  # 2 * 3600 Toutes les deux heures
            last_sent_time = current_time
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    print(f"Tentative de connexion au serveur {SERVER_HOST}:{SERVER_PORT}")
                    s.connect((SERVER_HOST, SERVER_PORT))
                    print("Connexion établie")

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
