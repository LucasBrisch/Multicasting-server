import socket
import time
import threading

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
NOTIFY_PORT = 5008  # Nova porta para notificações de conexão

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

# Socket para receber notificações de novos usuários
notify_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
notify_sock.bind(('', NOTIFY_PORT))

def listen_new_users():
    cont = 0
    # Thread para escutar notificações de novos usuários
    while True:
        data, addr = notify_sock.recvfrom(1024)
        msg = data.decode()
        if msg == "NEW_USER":
            print(f"Novo usuário conectado! Total de usuários: {cont + 1}")
            cont += 1
            print("Pressione 's' para enviar uma mensagem ou 'q' para sair: ", end="", flush=True)
        elif msg == "USER_LEFT":
            print(f"Um usuário saiu! Total de usuários: {cont - 1}")
            cont -= 1
            print("Pressione 's' para enviar uma mensagem ou 'q' para sair: ", end="", flush=True)

threading.Thread(target=listen_new_users, daemon=True).start()

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
