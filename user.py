import socket
import struct
import threading
import time

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
NOTIFY_PORT = 5008  # Porta de notificação do servidor
SERVER_IP = '127.0.0.1'  # Altere se o servidor estiver em outro IP

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    pass  # Ignora se o SO_REUSEPORT não for suportado

sock.bind(('', PORT)) 

# Notifica o servidor sobre nova conexão
notify_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
notify_sock.sendto(b"NEW_USER", (SERVER_IP, NOTIFY_PORT))

# Junta-se ao grupo multicast
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def receive_messages():
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Recebido de {addr}: {data.decode()}")
    except Exception as e:
        print(f"Erro ao receber mensagem: {e}")


print("Cliente multicast iniciado. Aguardando mensagens...")

# Inicia thread para receber mensagens
threading.Thread(target=receive_messages, daemon=True).start()

while True:
    key = input("Pressione 's' para sair\n")
    if key.lower() == 's':
        notify_sock.sendto(b"USER_LEFT", (SERVER_IP, NOTIFY_PORT))  # Notifica saída
        print("Saindo do servidor")
        break

print("Cliente encerrado.")
