
import socket
import time

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

print("Servidor multicast iniciado...")

try:
    count = 0
    while True:
        key = input("Pressione 's' para enviar uma mensagem ou 'q' para sair: ")
        if key.lower() == 'q':
            print("Saindo do servidor multicast.")
            break
        if key.lower() == 's':
            count += 1
            message = f"Mensagem {count}"
            sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
            print(f"Enviado: {message}")
            time.sleep(1)

except KeyboardInterrupt:
        print("Servidor encerrado.")
