import socket
import os

HOST = "0.0.0.0"  # Accepte les connexions de n'importe quelle adresse
PORT = 9558      # Port d'écoute

# Création du socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Attend une connexion

print("Serveur en attente de connexion pour camera record...")
client_socket, addr = server_socket.accept()
print(f"Connecté à : {addr}")


f = open('..\\data\\est_video.avi','wb') #open in binary   
l = client_socket.recv(1024)
i = 0
while (l):
    f.write(l)
    l = client_socket.recv(1024)
f.close()
client_socket.close()

server_socket.close()