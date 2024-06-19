import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Connexion à la base de données
connection = create_connection("localhost", "root", "", "supervisionpc")

# Exemple de requête pour créer une table
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY, 
  nom VARCHAR(255) NOT NULL, 
  prenom VARCHAR(255) NOT NULL, 
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
) ENGINE = InnoDB
"""
execute_query(connection, create_users_table)

# Exemple de requête pour insérer des données
create_user = """
INSERT INTO users (nom, prenom, email, password) VALUES ('James', 'bonice', 'bonicetok904@gmail.com', 'bonjour')
"""
execute_query(connection, create_user)

# Exemple de requête pour lire des données
select_users = "SELECT * FROM users"
users = execute_read_query(connection, select_users)

if users:
    for user in users:
        print(user)
else:
    print("Aucun utilisateur trouvé")

# Fermer la connexion
if connection.is_connected():
    connection.close()
    print("Connexion à MySQL fermée")

