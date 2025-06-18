import socket
import time
import threading

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
NOTIFY_PORT = 5008  # Nova porta para notificações de conexão
START = False

chosen = int(input("Escolha o número de usuários para iniciar o servidor (mínimo 1): "))
quantity = int(input("Quantas mensagens deseja enviar? "))
if chosen < 1:
    print("Número de usuários inválido. O servidor não será iniciado.")
    exit()

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
            if cont == chosen:
                global START
                START = True
        elif msg == "USER_LEFT":
            print(f"Um usuário saiu! Total de usuários: {cont - 1}")
            cont -= 1
            

threading.Thread(target=listen_new_users, daemon=True).start()

print("Servidor multicast iniciado...")

while True:
    try:
        count = 0
        if START:
            while True:
                    count += 1
                    message = f"Atualização {count}"
                    sock.sendto(message.encode(), (MULTICAST_GROUP, PORT))
                    print(f"Enviado: {message}")
                    time.sleep(1)
                    if count >= quantity:
                        print("Quantidade de mensagens enviada atingida.")
                        exit()
                    
                    

    except KeyboardInterrupt:
            print("Servidor encerrado.")
