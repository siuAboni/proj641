import socket
import csv
import os
import time
import traceback

import matplotlib.pyplot as plt
import numpy as np

dirname = os.path.dirname(__file__)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



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


    #to plot received data
    #plt.ion() #turning interactive mode on

    #X, Y = [1, 2], [1, 2]

    # plot
    #fig, ax = plt.subplots()
    #fig.set_figheight(10)
    #fig.set_figwidth(10)

    #plot1 = ax.scatter(X, Y)

    #ax.set(xlim=(-20, 20), xticks=np.arange(1, 8),
        #ylim=(-20, 20), yticks=np.arange(1, 8))

    #ax.set_aspect('equal')
    #ax.grid(True, which='both')

    #ax.axhline(y=0, color='red')
    #ax.axvline(x=0, color='blue')

    #plt.draw()

    while True:
        try:
            data = client_socket.recv(2048).decode()  # Réception des données
            if not data:
                break  # Arrêt si la connexion est fermée

            list = data.split(",")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            sorted_data = {
                "front": [timestamp],
                "left": [timestamp],
                "right": [timestamp],
            }

            write_in = list[0]
            cpt = 1 #use this variable to differienciate x var from y var
            for elt in list:
                if not is_number(elt):
                    write_in = elt
                    cpt = 1
                else:
                    sorted_data[write_in].append(elt)
                    #if cpt % 2 == 1:
                        # this is an x var
                        #X.append(float(elt))
                        #X = np.concatenate([X, np.array([float(elt)])])
                    #else:
                        #Y.append(float(elt))
                        #Y = np.concatenate([Y, np.array([float(elt)])])
                        #plot1.set_xdata(X)
                        #plot1.set_ydata(Y)
                        #sizes = np.random.uniform(15, 80, len(X))
                        #colors = np.random.uniform(15, 80, len(X))
                        #ax.scatter(X, Y, s=sizes, c=colors, vmin=0, vmax=100)
                        #plot1.set_offsets(np.c_[X,Y])
                        #fig.canvas.draw_idle()
                        #plt.pause(0.1)
                        #cpt+=1
            
            front_writer.writerow(sorted_data["front"])
            left_writer.writerow(sorted_data["left"])
            right_writer.writerow(sorted_data["right"])
            
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            print(traceback.format_exc())
            break

client_socket.close()
server_socket.close()
print("Connexion fermée.")