import socket
import json
import mysql.connector
from mysql.connector import Error

# Connexion à la base de données
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="supervisionpc"
        )
        print("Connexion à MySQL DB réussie")
    except Error as e:
        print(f"Erreur '{e}'")
    return connection

def insert_machine_data(connection, machine_data):
    cursor = connection.cursor(dictionary=True)
    
    # Vérifier si la machine existe déjà
    query_check = "SELECT id FROM Machine WHERE mac_address = %s"
    cursor.execute(query_check, (machine_data['mac_address'],))
    result = cursor.fetchone()
    
    if result:
        return result['id']
    
    # Insérer une nouvelle machine si elle n'existe pas
    query_insert = """
    INSERT INTO Machine (machine_type, mac_address, system, node_name, machine_architecture, processor, cores, logical_cores, cpu_frequency, total_memory, total_disk, version, releases)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_insert, (
        machine_data['machine_type'],
        machine_data['mac_address'],
        machine_data['os']['system'],
        machine_data['os']['node_name'],
        machine_data['os']['machine'],
        machine_data['os']['processor'],
        machine_data['processor']['cores'],
        machine_data['processor']['logical_cores'],
        machine_data['processor']['frequency'],
        machine_data['memory']['total_memory'],
        machine_data['disk']['total_disk'],
        machine_data['os']['version'],
        machine_data['os']['release']
    ))
    connection.commit()
    return cursor.lastrowid

def insert_donnees_data(connection, machine_id, donnees_data):
    query = """
    INSERT INTO Donnees (machine_id, used_memory, memory_percentage, cached_memory, swap_total, swap_used, swap_percentage, used_disk, disk_percentage, cpu_load_per_core, net_bytes_sent, net_bytes_recv, active_processes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, (
            machine_id,
            donnees_data['used_memory'],
            donnees_data['memory_usage'],
            donnees_data['cache'],
            donnees_data['swap_total'],
            donnees_data['swap_used'],
            donnees_data['swap_percentage'],
            donnees_data['used_disk'],
            donnees_data['disk_percentage'],
            json.dumps(donnees_data['cpu_usage_per_core']),
            donnees_data['net_bandwidth']['bytes_sent'],
            donnees_data['net_bandwidth']['bytes_recv'],
            json.dumps(donnees_data['active_processes'])
        ))
        connection.commit()
        print("\n\n ===========================\n\n Données insérées dans la base de données\n\n =====================================\n\n")
    except Error as e:
        print(f"Erreur lors de l'insertion des données: {e}")

def handle_client_connection(connection, client_socket):
    buffer = ""
    machine_id = None
    while True:
        data = client_socket.recv(4096).decode('utf-8')
        if not data:
            break
        buffer += data
        if '\n' in buffer:
            message, buffer = buffer.split('\n', 1)
            try:
                system_info = json.loads(message)
                print(system_info)
                if 'initial_info' in system_info and machine_id is None:
                    machine_id = insert_machine_data(connection, system_info['initial_info'])
                    if machine_id:
                        print(f"Machine ID: {machine_id}")
                    else:
                        print("Erreur lors de l'insertion de la machine")
                if 'system_load' in system_info and machine_id:
                    insert_donnees_data(connection, machine_id, system_info['system_load'])
                else:
                    print("\n\n ===========================\n\n Données non insérées dans la base de données {}\n\n =====================================\n\n".format(machine_id))
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON: {e}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Serveur en attente de connexions...")

    connection = create_connection()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connexion établie avec {client_address}")
        handle_client_connection(connection, client_socket)
        client_socket.close()

if __name__ == "__main__":
    start_server()
