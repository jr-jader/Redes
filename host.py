import socket
import threading

def receive_messages(client_socket, remote_user_name):
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Recebe mensagem do cliente remoto
            if not message:
                print(f"Conexão com {remote_user_name} perdida.")
                break
            print(f"{remote_user_name}: {message}")
        except:
            print(f"Conexão com {remote_user_name} perdida.")
            break

def main():
    listen_ip = "127.0.0.1"  # Endereço IP para escutar conexões
    listen_port = 3030  # Porta para escutar conexões

    user_name = input("Digite seu nome de usuário: ")  # Solicita nome de usuário

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria socket IPv4 e TCP
    client_socket.bind((listen_ip, listen_port))  # Associa o socket ao IP e porta
    client_socket.listen(1)  # Entra em modo de escuta para aceitar conexões

    print("Aguardando conexão do outro usuário...")
    remote_client_socket, remote_client_address = client_socket.accept()  # Aceita conexão do cliente remoto
    print(f"Conexão estabelecida com {remote_client_address}")

    remote_user_name = remote_client_socket.recv(1024).decode()  # Recebe o nome de usuário do cliente remoto
    remote_client_socket.send(user_name.encode())  # Envia o nome de usuário para o cliente remoto

    receive_thread = threading.Thread(target=receive_messages, args=(remote_client_socket, remote_user_name))
    receive_thread.start()  # Inicia thread para receber mensagens do cliente remoto

    while True:
        message = input()
        if message.lower() == "sair":
            remote_client_socket.send(message.encode())  # Envia comando de saída para o cliente remoto
            break
        remote_client_socket.send(message.encode())  # Envia mensagem para o cliente remoto

    remote_client_socket.close()
    client_socket.close()

if __name__ == "__main__":
    main()
