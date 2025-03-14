import socket
import csv
import os

dirname = os.path.dirname(__file__)

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
filename_front = os.path.join(dirname, "../data/laser/laser_data_front.csv")
filename_left = os.path.join(dirname, "../data/laser/laser_data_left.csv")
filename_right = os.path.join(dirname, "../data/laser/laser_data_right.csv")
with open(filename_front, mode="w", newline="") as file_front, open(filename_left, mode="w", newline="") as file_left, open(filename_right, mode="w", newline="") as file_right:
    front_writer = csv.writer(file_front)
    left_writer = csv.writer(file_left)
    right_writer = csv.writer(file_right)
    
    header = ["Timestamp"]
    for i in range(1,16):
        header.append(f"Seg0{i}X")
        header.append(f"Seg0{i}Y")
    front_writer.writerow(header)
    left_writer.writerow(header)
    right_writer.writerow(header)

    while True:
        try:
            data = client_socket.recv(1024).decode()  # Réception des données
            if not data:
                break  # Arrêt si la connexion est fermée

            list = data.split(",")
            
            if (str(list[0]) == "front"):
                print(f"Données reçues : front")
                list.pop(0)
                front_writer.writerow(list)
                file_front.flush()  # Forcer l'écriture immédiate
            elif (str(list[0]) == "left"):
                print(f"Données reçues : left")
                list.pop(0)
                left_writer.writerow(list)
                file_left.flush()
            else:
                print(f"Données reçues : right")
                list.pop(0)
                right_writer.writerow(list)
                file_right.flush()
            
        except Exception as e:
            print(f"Erreur : {e}")
            break

client_socket.close()
server_socket.close()
print("Connexion fermée.")