import socket
import struct
import time
import json

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        self.video = ALProxy('ALVideoDevice')
        self.running = True

    def onUnload(self):
        self.running = False

    def onInput_onStart(self):
        SERVER_IP = "193.48.125.69"  # IP du PC serveur
        SERVER_PORT = 9558

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER_IP, SERVER_PORT))
            print("Connexion au serveur réussie !")
        except Exception as e:
            print("Erreur de connexion : {0}".format(e))
            return

        # S'abonner à la caméra de profondeur
        resolution = 2  # 640x480
        colorSpace = 11  # AL::kDepthCamera
        fps = 5

        try:
            nameId = self.video.subscribeCamera("DepthViewer", 2, resolution, colorSpace, fps)
        except Exception as e:
            print("Erreur d'abonnement caméra : {0}".format(e))
            sock.close()
            return

        try:
            while self.running:
                image = self.video.getImageRemote(nameId)

                if image is not None:
                    depth_data = image[6]  # Image buffer
                    width = image[0]
                    height = image[1]

                    # Transformation du buffer en points (simple normalisation pour le test)
                    points = []
                    for i in range(0, len(depth_data), 2):
                        depth = (ord(depth_data[i]) + (ord(depth_data[i+1]) << 8)) * 0.001  # en mètres
                        x = (i // 2) % width
                        y = (i // 2) // width
                        points.append((float(x), float(y), float(depth)))

                    # Préparation à l'envoi
                    payload = json.dumps(points)
                    payload = struct.pack('>I', len(payload)) + payload
                    sock.sendall(payload)

                time.sleep(1)

        except Exception as e:
            print("Erreur d'envoi : {0}".format(e))
        finally:
            self.video.unsubscribe(nameId)
            sock.close()
            self.onStopped()

    def onInput_onStop(self):
        self.running = False
        self.onUnload()
        self.onStopped()