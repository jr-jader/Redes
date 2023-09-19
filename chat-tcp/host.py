import socket
import threading
from interface import Chat

def receive_messages(client_socket, chat_gui):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Conexão perdida.")
                break
            chat_gui.insert_message(message)
        except:
            print("Conexão perdida.")
            break

def send_message(client_socket, message):
    client_socket.send(message.encode())

def main():
    listen_ip = "127.0.0.1"
    listen_port = 3031

    user_name = input("Digite seu nome de usuário: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((listen_ip, listen_port))
    client_socket.listen(1)

    print("Aguardando conexão do outro usuário...")
    remote_client_socket, remote_client_address = client_socket.accept()
    print(f"Conexão estabelecida com {remote_client_address}")

    remote_user_name = remote_client_socket.recv(1024).decode()
    remote_client_socket.send(user_name.encode())

    chat = Chat(user_name, lambda message: send_message(remote_client_socket, message))

    receive_thread = threading.Thread(target=receive_messages, args=(remote_client_socket, chat))
    receive_thread.start()

    chat.start()

    remote_client_socket.close()
    client_socket.close()

if __name__ == "__main__":
    main()
