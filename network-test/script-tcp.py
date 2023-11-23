import socket, time, locale

locale.setlocale(locale.LC_ALL, '')

PEER1_IP = '127.0.0.1'
PEER2_IP = '127.0.0.1'
PORT1 = 8000
PORT2 = 8001

STRING = 'teste de rede *2023*' * 100

PACKET_SIZE = 500

TIMER = 5

class tcp_upload:
    def start_upload(self, data, dest):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(dest)
            print('Now connected to Upload on ', dest)
            start_time = time.time()
            end_time = 0
            while time.time() - start_time < TIMER:
                self.upload(data, dest)
                end_time = time.time()
            print(f'START TIME: {start_time} | END TIME: {end_time}')
        except Exception as e:
            print(f"Error during upload: {e}")

    def send_message(self, message, dest):
        self.sock.sendto(message.encode('utf-8'), dest)

    def upload(self, data, dest): #sender
        chunks = [data[i: i + PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
        for chunk in chunks:
            self.send_message(chunk, dest)
        
class tcp_download: 
    def __init__(self, dest):
        self.sock = socket.socket(socket.AF_INET, #Internet
                            socket.SOCK_STREAM) #TCP
        self.sock.bind(dest)
        self.sock.listen(1)  # Listen for incoming connections
        self.received_bytes = 0
        self.received_packets = 0
    
    def start_download(self, dest):
        try:
            conn, addr = self.sock.accept()
            print('Now connected to Download from ', dest)
            start_time = time.time()
            while time.time() - start_time < TIMER + 1:
                self.download(conn)
        except Exception as e:
            print(f"Error during download: {e}")

    def download(self, conn): #receiver
        data = ''
        while(True):
            chunk = conn.recv(PACKET_SIZE)  # Receive data from the connection
            chunk = chunk.decode('utf-8')
            data += ''.join(chunk)
            self.received_packets += 1
            if len(chunk) < PACKET_SIZE:
                break
        self.received_bytes = self.received_packets * PACKET_SIZE

def main():
    routine = input("Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    while routine != '0' and routine != '1':
        routine = input("ERROR: invalid routine. Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    if routine == '0':
        print('\n===TCP UPLOAD ROUTINE===\n')
        obj = tcp_upload()
        obj.start_upload(STRING, (PEER1_IP, PORT1))
        obj.sock.close()
        print('\n===TCP DOWNLOAD ROUTINE AFTER UPLOAD===\n')
        obj = tcp_download((PEER2_IP, PORT2))
        obj.start_download((PEER2_IP, PORT2))
        obj.sock.close()
        print(f"Total of bytes: {locale.format_string('%d', obj.received_bytes, grouping=True)}\nTotal of packets: {locale.format_string('%d', obj.received_packets, grouping=True)}")
    else:
        print('\n===TCP DOWNLOAD ROUTINE===\n')
        obj = tcp_download((PEER1_IP, PORT1))
        obj.start_download((PEER1_IP, PORT1))
        obj.sock.close()  # Close the connection when done
        print(f"Total of bytes: {locale.format_string('%d', obj.received_bytes, grouping=True)}\nTotal of packets: {locale.format_string('%d', obj.received_packets, grouping=True)}")
        print('\n===TCP UPLOAD ROUTINE AFTER DOWNLOAD===\n')
        obj = tcp_upload()
        obj.start_upload(STRING, (PEER2_IP, PORT2))
        obj.sock.close()

if __name__ == "__main__":
    main()