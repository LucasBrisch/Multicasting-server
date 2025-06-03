
import socket
import struct

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1) 
sock.bind(('', PORT)) 



# Junta-se ao grupo multicast
mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Cliente multicast iniciado. Aguardando mensagens...")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Recebido de {addr}: {data.decode()}")

except KeyboardInterrupt:
        print("Cliente encerrado.")
