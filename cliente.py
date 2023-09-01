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
    user_name = input("Digite seu nome de usuário: ")
    remote_ip = input("Digite o IP do host: ")
    remote_port = int(input("Digite a porta do host: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remote_ip, remote_port))

    client_socket.send(user_name.encode())
    remote_user_name = client_socket.recv(1024).decode()

    print(f"Conectado com {remote_user_name}")

    chat = Chat(user_name, lambda message: send_message(client_socket, message))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, chat))
    receive_thread.start()

    chat.start()

    client_socket.close()

if __name__ == "__main__":
    main()
