import socket
import threading

def receive_messages(client_socket, remote_user_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Recebe mensagem do host remoto
            if not message:
                print(f"Conexão com {remote_user_name} perdida.")
                break
            print(f"{remote_user_name}: {message}")
        except:
            print(f"Conexão com {remote_user_name} perdida.")
            break

def main():
    user_name = input("Digite seu nome de usuário: ")  # Solicita nome de usuário
    remote_ip = input("Digite o IP do host: ")  # Solicita IP do host remoto
    remote_port = int(input("Digite a porta do host: "))  # Solicita porta do host remoto

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket IPv4 e TCP
    client_socket.connect((remote_ip, remote_port))  # Conecta ao host remoto

    client_socket.send(user_name.encode())  # Envia o nome de usuário para o host remoto

    remote_user_name = client_socket.recv(1024).decode()  # Recebe o nome de usuário do host remoto
    print(f"Conectado com {remote_user_name}")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, remote_user_name))
    receive_thread.start()  # Inicia thread para receber mensagens do host remoto

    while True:
        message = input()
        if message.lower() == "sair":
            client_socket.send(message.encode())  # Envia comando de saída para o host remoto
            break
        client_socket.send(message.encode())  # Envia mensagem para o host remoto

    client_socket.close()

if __name__ == "__main__":
    main()
