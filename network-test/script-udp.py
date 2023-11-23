import socket, time, locale

locale.setlocale(locale.LC_ALL, '')

PEER1_IP = '127.0.0.1'
PEER2_IP = '127.0.0.1'
PORT1 = 8000
PORT2 = 8001

STRING = "teste de rede *2023*" * 100

PACKET_SIZE = 500

TIMER = 20
TIMEOUT = 2  # Timeout for ACKs

class udp_upload:
    def start_upload(self, data, dest):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.settimeout(TIMEOUT)  # Set timeout for ACKs
            print('Now connected to Upload on ', dest)
            start_time = time.time()
            end_time = 0
            packets_sent = 0
            while time.time() - start_time < TIMER:
                packets_sent += self.upload(data, dest)
                end_time = time.time()
            print(f'START TIME: {start_time} | END TIME: {end_time}')
            print(f'Packets sent: {packets_sent}')
            print(f'Bytes sent: {packets_sent * PACKET_SIZE}')
            print(f'Speed: {packets_sent * PACKET_SIZE * 8 / (end_time - start_time)} bits per second')
            print(f'Packet rate: {packets_sent / (end_time - start_time)} packets per second')
        except Exception as e:
            print(f"Error during upload: {e}")

    def send_message(self, message, dest):
        while True:
            self.sock.sendto(message.encode('utf-8'), dest)
            try:
                data, addr = self.sock.recvfrom(1024)  # Wait for ACK
                if data.decode('utf-8') == 'ACK':
                    break  # Break the loop if ACK received
            except socket.timeout:
                continue  # Resend the packet if no ACK received within the timeout

    def upload(self, data, dest): #sender
        chunks = [data[i: i + PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
        for chunk in chunks:
            self.send_message(chunk, dest)
        return len(chunks)
        
class udp_download: 
    def __init__(self, dest):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(dest)
        self.received_bytes = 0
        self.received_packets = 0
    
    def start_download(self, dest):
        try:
            print('Now connected to Download from ', dest)
            start_time = time.time()
            while time.time() - start_time < TIMER + 1:
                self.download()
            print(f'Total of bytes: {locale.format_string("%d", self.received_bytes, grouping=True)}')
            print(f'Total of packets: {locale.format_string("%d", self.received_packets, grouping=True)}')
        except Exception as e:
            print(f"Error during download: {e}")

    def download(self): #receiver
        data = ''
        while(True):
            chunk, addr = self.sock.recvfrom(PACKET_SIZE)  # Receive data from the connection
            chunk = chunk.decode('utf-8')
            data += ''.join(chunk)
            self.received_packets += 1
            self.sock.sendto('ACK'.encode('utf-8'), addr)  # Send ACK
            if len(chunk) < PACKET_SIZE:
                break
        self.received_bytes = self.received_packets * PACKET_SIZE

def main():
    routine = input("Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    while routine != '0' and routine != '1':
        routine = input("ERROR: invalid routine. Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    if routine == '0':
        print('\n===UDP UPLOAD ROUTINE===\n')
        obj = udp_upload()
        obj.start_upload(STRING, (PEER1_IP, PORT1))
        print('\n===UDP DOWNLOAD ROUTINE AFTER UPLOAD===\n')
        obj = udp_download((PEER2_IP, PORT2))
        obj.start_download((PEER2_IP, PORT2))
    else:
        print('\n===UDP DOWNLOAD ROUTINE===\n')
        obj = udp_download((PEER1_IP, PORT1))
        obj.start_download((PEER1_IP, PORT1))
        print('\n===UDP UPLOAD ROUTINE AFTER DOWNLOAD===\n')
        obj = udp_upload()
        obj.start_upload(STRING, (PEER2_IP, PORT2))

if __name__ == "__main__":
    main()
