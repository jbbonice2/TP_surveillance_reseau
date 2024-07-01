# import socket
# import json
# import mysql.connector
# from mysql.connector import Error

# # Fonction pour créer une connexion à la base de données
# def create_connection():
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             passwd="",
#             database="supervisionpc"
#         )
#         print("Connexion à MySQL DB réussie")
#     except Error as e:
#         print(f"Erreur '{e}'")
#     return connection

# # Fonction pour insérer les données de la machine dans la table Machine
# def insert_machine_data(connection, machine_data):
#     cursor = connection.cursor(dictionary=True)
    
#     # Vérifier si la machine existe déjà
#     query_check = "SELECT id FROM Machine WHERE mac_address = %s"
#     cursor.execute(query_check, (machine_data['mac_address'],))
#     result = cursor.fetchone()
    
#     if result:
#         return result['id']
    
#     # Insérer une nouvelle machine si elle n'existe pas
#     query_insert = """
#     INSERT INTO Machine (machine_type, mac_address, system, node_name, machine_architecture, processor, cores, logical_cores, cpu_frequency, total_memory, total_disk, version, releases)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     cursor.execute(query_insert, (
#         machine_data['machine_type'],
#         machine_data['mac_address'],
#         machine_data['os']['system'],
#         machine_data['os']['node_name'],
#         machine_data['os']['machine'],
#         machine_data['os']['processor'],
#         machine_data['processor']['cores'],
#         machine_data['processor']['logical_cores'],
#         machine_data['processor']['frequency'],
#         machine_data['memory']['total_memory'],
#         machine_data['disk']['total_disk'],
#         machine_data['os']['version'],
#         machine_data['os']['release']
#     ))
#     connection.commit()
#     return cursor.lastrowid

# # Fonction pour insérer les données dans la table Donnees
# def insert_donnees_data(connection, donnees_data):
#     cursor = connection.cursor(dictionary=True)
    
#     # Vérifier si la machine existe déjà
#     query_check = "SELECT id FROM Machine WHERE mac_address = %s"
#     cursor.execute(query_check, (donnees_data['mac_address'],))
#     result = cursor.fetchone()
    
#     if result:
#         machine_id = result['id']
#     else:
#         print("La machine n'existe pas dans la base de données")
#         return

#     query = """
#     INSERT INTO Donnees (machine_id, used_memory, memory_percentage, cached_memory, swap_total, swap_used, swap_percentage, used_disk, disk_percentage, cpu_load_per_core, net_bytes_sent, net_bytes_recv, active_processes)
#     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """
#     try:
#         cursor.execute(query, (
#             machine_id,
#             donnees_data['used_memory'],
#             donnees_data['memory_usage'],
#             donnees_data['cache'],
#             donnees_data['swap_total'],
#             donnees_data['swap_used'],
#             donnees_data['swap_percentage'],
#             donnees_data['used_disk'],
#             donnees_data['disk_percentage'],
#             json.dumps(donnees_data['cpu_usage_per_core']),
#             donnees_data['net_bandwidth']['bytes_sent'],
#             donnees_data['net_bandwidth']['bytes_recv'],
#             json.dumps(donnees_data['active_processes'])
#         ))
#         connection.commit()
#         print("Données insérées dans la base de données")
#     except Error as e:
#         print(f"Erreur lors de l'insertion des données: {e}")

# # Fonction pour gérer la connexion client
# def handle_client_connection(connection, client_socket):
#     buffer = ""
#     while True:
#         data = client_socket.recv(4096).decode('utf-8')
#         if not data:
#             break
#         buffer += data
#         while '\n' in buffer:
#             message, buffer = buffer.split('\n', 1)
#             try:
#                 system_info = json.loads(message)
#                 print(f"Fichier reçu: {system_info}")
#                 if isinstance(system_info, list):
#                     for item in system_info:
#                         if 'initial_info' in item:
#                             insert_machine_data(connection, item['initial_info'])
#                         if 'system_load' in item:
#                             insert_donnees_data(connection, item['system_load'])
#                 else:
#                     print(f"Structure de message inattendue: {system_info}")
#             except json.JSONDecodeError as e:
#                 print(f"Erreur de décodage JSON: {e}")

# # Fonction pour démarrer le serveur
# def start_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('0.0.0.0', 12345))
#     server_socket.listen(5)
#     print("Serveur en attente de connexions...")

#     connection = create_connection()

#     while True:
#         client_socket, client_address = server_socket.accept()
#         print(f"Connexion établie avec {client_address}")
#         handle_client_connection(connection, client_socket)
#         client_socket.close()

# if __name__ == "__main__":
#     start_server()
  
# timestamp TIMESTAMP DEFAULT current_timestamp,


from datetime import datetime
import socket
import json
import psycopg2
from psycopg2 import Error

# Fonction pour créer une connexion à la base de données
def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            user="root",
            password="root",
            database="supervisionpc"
        )
        print("Connexion à PostgreSQL DB réussie")
    except Error as e:
        print(f"Erreur '{e}'")
    return connection

# Fonction pour créer les tables si elles n'existent pas
def create_tables(connection):
    cursor = connection.cursor()
    
    # Création de la table api_machine
    create_table_machine = """
    CREATE TABLE IF NOT EXISTS api_machine (
        id SERIAL PRIMARY KEY,
        machine_type VARCHAR(50),
        mac_address VARCHAR(17) UNIQUE,
        system VARCHAR(50),
        node_name VARCHAR(100),
        machine_architecture VARCHAR(20),
        processor VARCHAR(100),
        cores INT,
        logical_cores INT,
        cpu_frequency FLOAT,
        total_memory BIGINT,
        total_disk BIGINT,
        version VARCHAR(100) NOT NULL,
        releases VARCHAR(200) NOT NULL,
        collected_at TIMESTAMP NOT NULL DEFAULT current_timestamp
    );
    """
    
    # Création de la table api_data
    create_table_data = """
    CREATE TABLE IF NOT EXISTS api_data (
        id SERIAL PRIMARY KEY,
        machine_id INT REFERENCES Machine(id) ON DELETE CASCADE ON UPDATE CASCADE,
        used_memory BIGINT,
        memory_percentage FLOAT,
        cached_memory BIGINT,
        swap_total BIGINT,
        swap_used BIGINT,
        swap_percentage FLOAT,
        used_disk BIGINT,
        disk_percentage FLOAT,
        cpu_load_per_core JSONB,
        net_bytes_sent BIGINT,
        net_bytes_recv BIGINT,
        active_processes INT,
        gpu_usage_percentage FLOAT,
        cpu_temperature FLOAT,
        timestamp TIMESTAMP DEFAULT current_timestamp,
        internet_enabled BOOLEAN DEFAULT FALSE,
        collected_at TIMESTAMP NOT NULL DEFAULT current_timestamp
    );
    """
    
    # Création de la table api_variabledata
    create_table_variable_data = """
    CREATE TABLE IF NOT EXISTS api_variabledata (
        id SERIAL PRIMARY KEY,
        mac_address VARCHAR(17) NOT NULL,
        battery_percentage FLOAT NOT NULL,
        uptime BIGINT NOT NULL,
        boot_time TIMESTAMP NOT NULL,
        shutdown_time TIMESTAMP,
        timestamp TIMESTAMP DEFAULT current_timestamp,
        ip VARCHAR(17),
        collected_at TIMESTAMP NOT NULL DEFAULT current_timestamp
    );
    """
    
    try:
        cursor.execute(create_table_machine)
        cursor.execute(create_table_data)
        cursor.execute(create_table_variable_data)
        connection.commit()
        print("Tables créées ou existent déjà")
    except Error as e:
        print(f"Erreur lors de la création des tables: {e}")

# Fonction pour insérer les données de la machine dans la table api_machine
def insert_machine_data(connection, machine_data):
    cursor = connection.cursor()
    
    # Vérifier si la machine existe déjà
    query_check = "SELECT id FROM api_machine WHERE mac_address = %s"
    cursor.execute(query_check, (machine_data['mac_address'],))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Insérer une nouvelle machine si elle n'existe pas
    query_insert = """
    INSERT INTO api_machine (machine_type, mac_address, system, node_name, machine_architecture, processor, cores, logical_cores, cpu_frequency, total_memory, total_disk, version, releases, collected_at, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
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
        machine_data['os']['release'],
        machine_data['timestamp'],
        datetime.now().isoformat()
    ))
    connection.commit()
    machine_id = cursor.fetchone()[0]
    return machine_id

# Fonction pour insérer les données dans la table api_machine
def insert_data(connection, data):
    cursor = connection.cursor()
    
    # Vérifier si la machine existe déjà
    query_check = "SELECT id FROM api_machine WHERE mac_address = %s"
    cursor.execute(query_check, (data['mac_address'],))
    result = cursor.fetchone()
    
    if result:
        machine_id = result[0]
    else:
        print("La machine n'existe pas dans la base de données")
        return

    query = """
    INSERT INTO api_data (machine_id, used_memory, memory_percentage, cached_memory, swap_total, swap_used, swap_percentage, used_disk, disk_percentage, cpu_load_per_core, net_bytes_sent, net_bytes_recv, active_processes, gpu_usage_percentage, cpu_temperature, collected_at,  timestamp, internet_enabled)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (
            machine_id,
            data['used_memory'],
            data['memory_usage'],
            data['cache'],
            data['swap_total'],
            data['swap_used'],
            data['swap_percentage'],
            data['used_disk'],
            data['disk_percentage'],
            json.dumps(data['cpu_usage_per_core']),
            data['net_bandwidth']['bytes_sent'],
            data['net_bandwidth']['bytes_recv'],
            data['active_processes'],
            data['gpu_usage_percentage'],
            data['cpu_temperature'],
            data['timestamp'],
            datetime.now().isoformat(),
            data['internet_enabled']            
        ))
        connection.commit()
        print("Données insérées dans la base de données")
    except Error as e:
        print(f"Erreur lors de l'insertion des données: {e}")

# Fonction pour insérer les données variables dans la table api_variabledata
def insert_variable_data(connection, variable_data):
    cursor = connection.cursor()
    

    query_check = "SELECT id FROM api_machine WHERE mac_address = %s"
    cursor.execute(query_check, (variable_data['mac_address'],))
    result = cursor.fetchone()
    
    if result:
        machine_id = result[0]
    else:
        print("La machine n'existe pas dans la base de données")
        return
    query = """
    INSERT INTO api_variabledata (machine_id, mac_address, battery_percentage, uptime, boot_time, shutdown_time, collected_at, timestamp, ip)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        shutdown_time = datetime.now().isoformat() if variable_data['shutdown_time'] == -1 else variable_data['shutdown_time']

        cursor.execute(query, (
            machine_id,
            variable_data['mac_address'],
            variable_data['battery_percentage'],
            variable_data['uptime'],
            variable_data['boot_time'],
            shutdown_time,  
            variable_data['timestamp'],
            datetime.now().isoformat(),
            variable_data['ip'][0]
        ))
        connection.commit()
        print("Données variables insérées dans la base de données")
    except Error as e:
        print(f"Erreur lors de l'insertion des données variables: {e}")

# Fonction pour gérer la connexion client
def handle_client_connection(connection, client_socket, client_address):
    buffer = ""
    while True:
        data = client_socket.recv(4096).decode('utf-8')
        if not data:
            break
        buffer += data
        while '\n' in buffer:
            message, buffer = buffer.split('\n', 1)
            try:
                system_info = json.loads(message)
                print(f"Fichier reçu: {system_info}")
                if isinstance(system_info, list):
                    for item in system_info:
                        if 'initial_info' in item:
                            insert_machine_data(connection, item['initial_info'])
                        if 'system_load' in item:
                            item['system_load']['ip'] = client_address
                            insert_data(connection, item['system_load'])
                        if 'variable_data' in item:
                            item['variable_data']['ip'] = client_address
                            insert_variable_data(connection, item['variable_data'])
                else:
                    print(f"Structure de message inattendue: {system_info}")
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON: {e}")

# Fonction pour démarrer le serveur
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Serveur en attente de connexions...")

    connection = create_connection()
    create_tables(connection)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connexion établie avec {client_address}")
        handle_client_connection(connection, client_socket, client_address)
        client_socket.close()

if __name__ == "__main__":
    start_server()
