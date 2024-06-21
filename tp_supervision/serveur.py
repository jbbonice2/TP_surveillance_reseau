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

# Fonction pour insérer les données de la machine dans la table Machine
def insert_machine_data(connection, machine_data):
    cursor = connection.cursor()
    
    # Vérifier si la machine existe déjà
    query_check = "SELECT id FROM Machine WHERE mac_address = %s"
    cursor.execute(query_check, (machine_data['mac_address'],))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Insérer une nouvelle machine si elle n'existe pas
    query_insert = """
    INSERT INTO Machine (machine_type, mac_address, system, node_name, machine_architecture, processor, cores, logical_cores, cpu_frequency, total_memory, total_disk, version, releases)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        machine_data['os']['release']
    ))
    connection.commit()
    machine_id = cursor.fetchone()[0]
    return machine_id

# Fonction pour insérer les données dans la table Donnees
def insert_donnees_data(connection, donnees_data):
    cursor = connection.cursor()
    
    # Vérifier si la machine existe déjà
    query_check = "SELECT id FROM Machine WHERE mac_address = %s"
    cursor.execute(query_check, (donnees_data['mac_address'],))
    result = cursor.fetchone()
    
    if result:
        machine_id = result[0]
    else:
        print("La machine n'existe pas dans la base de données")
        return

    query = """
    INSERT INTO Donnees (machine_id, used_memory, memory_percentage, cached_memory, swap_total, swap_used, swap_percentage, used_disk, disk_percentage, cpu_load_per_core, net_bytes_sent, net_bytes_recv, active_processes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
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
        print("Données insérées dans la base de données")
    except Error as e:
        print(f"Erreur lors de l'insertion des données: {e}")

# Fonction pour gérer la connexion client
def handle_client_connection(connection, client_socket):
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
                            insert_donnees_data(connection, item['system_load'])
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

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connexion établie avec {client_address}")
        handle_client_connection(connection, client_socket)
        client_socket.close()

if __name__ == "__main__":
    start_server()
