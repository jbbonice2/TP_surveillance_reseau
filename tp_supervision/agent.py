import psutil
import platform
import os
import time
import uuid

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
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    swap_usage = psutil.swap_memory().percent
    net_io = psutil.net_io_counters()
    net_bandwidth = {
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv
    }
    return {
        "cpu_usage_per_core": cpu_load_per_core,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "swap_usage": swap_usage,
        "net_bandwidth": net_bandwidth
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

def main():
    # Récupérer les informations initiales
    initial_info = gather_initial_system_info()
    print("Initial system information:")
    for key, value in initial_info.items():
        print(f"{key}: {value}")
    
    # Boucle pour récupérer la charge toutes les deux minutes
    while True:
        system_load = get_system_load()
        active_processes = get_active_processes_info()
        print("\nSystem load:")
        for key, value in system_load.items():
            print(f"{key}: {value}")
        print("\nActive processes:")
        for proc in active_processes:
            print(proc)
        time.sleep(10)  # Pause de 2 minutes

if __name__ == "__main__":
    main()
