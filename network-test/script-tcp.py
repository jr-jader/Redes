import socket, time, locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

SELF_IP = '127.0.0.1'
PEER_IP = '127.0.0.1'
PORT = 3030
PORT2 = 3031

STRING = 'teste de rede *2023*' * 100

PACKET_SIZE = 500

class tcp_upload:
    def __init__(self, dest):
        self.sock = socket.socket(socket.AF_INET, #Internet
                            socket.SOCK_STREAM) #TCP
        self.sock.connect(dest)
        self.sent_packets = 0
        print('Now connected to Upload on ', dest)

    def send_message(self, message, dest):
        self.sock.sendto(message.encode('utf-8'), dest)

    def upload(self, data, dest): #sender
        chunks = [data[i: i + PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
        for chunk in chunks:
            self.send_message(chunk, dest)
            self.sent_packets += 1
        print(f'Done sending string: {data}')
        
class tcp_download:
    def __init__(self, dest):
        self.sock = socket.socket(socket.AF_INET, #Internet
                            socket.SOCK_STREAM) #TCP
        self.sock.bind(dest)
        self.sock.listen(1)  # Listen for incoming connections
        self.received_packets = 0

    def download(self, dest): #receiver
        conn, addr = self.sock.accept()  # Accept a connection
        print('Now connected to Download from ', dest)
        data = ''
        while(True):
            chunk = conn.recv(PACKET_SIZE)  # Receive data from the connection
            chunk = chunk.decode('utf-8')
            data += ''.join(chunk)
            self.received_packets += 1
            if len(chunk) < PACKET_SIZE:
                break
        print(f"Received string: {data}")
        conn.close()  # Close the connection when done

def main():
    routine = input("Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    while routine != '0' and routine != '1':
        routine = input("ERROR: invalid routine. Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    if routine == '0':
        print('\n===TCP UPLOAD ROUTINE===\n')
        obj = tcp_upload((SELF_IP, PORT))
        start_time = time.time()
        while time.time() - start_time < 20:
            obj.upload(STRING, (SELF_IP, PORT))
        obj.sock.close()
        print('\nWaiting...\n')
        print('\n===TCP DOWNLOAD ROUTINE AFTER UPLOAD===\n')
        obj = tcp_download((PEER_IP, PORT2))
        obj.download((PEER_IP, PORT2))
    else:
        print('\n===TCP DOWNLOAD ROUTINE===\n')
        obj = tcp_download((SELF_IP, PORT))
        obj.download((SELF_IP, PORT))
        time.sleep(21)
        print('\n===TCP UPLOAD ROUTINE AFTER DOWNLOAD===\n')
        start_time = time.time()
        while time.time() - start_time < 20:
            obj.upload(STRING, (PEER_IP, PORT2))
        obj.sock.close()

if __name__ == "__main__":
    main()