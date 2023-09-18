import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 3030

class Receiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))

    def receive_message(self):
        data = ''
        while True:
            chunk, addr = self.sock.recvfrom(500) # Receive 500-byte chunks
            chunk = chunk.decode('utf-8')
            header = chunk[0:2] # Extract header of size 2
            print(f"\nReceived packet number (HEADER) {int(header)}")
            print(chunk[2:len(chunk) - 4])
            checksum_received = chunk[len(chunk) - 4:]
            checksum_calculated = str(hash(chunk[:-4]))[-4:]
            print(f"CHECKSUM received: {checksum_received}")
            print(f"CHECKSUM calculated: {checksum_calculated}")
            data += ''.join(chunk[2:len(chunk) - 4]) # Join remaining parts of chunk
            if len(chunk) < 500:
                break
        print('\nReceived string: ', data)

recv = Receiver()
recv.receive_message()