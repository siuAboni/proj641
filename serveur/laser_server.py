import socket
import csv

HOST = "0.0.0.0"  # Accepte les connexions de n'importe quelle adresse
PORT = 9558      # Port d'écoute

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Attend une connexion

print("Serveur en attente de connexion pour laser...")
client_socket, addr = server_socket.accept()
print(f"Connecté à : {addr}")

# Ouvrir un fichier CSV pour enregistrer les données
with open("E:\\Documents\\proj641\\sonar\\laser_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    #writer.writerow(["Timestamp", "Laser Value"])  # En-tête du fichier CSV
    writer.writerow(["Timestamp"] + [f"Seg0{i}" for i in range(1,16)])

    while True:
        try:
            data = client_socket.recv(1024).decode()  # Réception des données
            if not data:
                break  # Arrêt si la connexion est fermée
            print(f"Données reçues : {data}")

            writer.writerow(data.split(","))  # Enregistrement dans le fichier
            file.flush()  # Forcer l'écriture immédiate
        except Exception as e:
            print(f"Erreur : {e}")
            break

client_socket.close()
server_socket.close()
print("Connexion fermée.")