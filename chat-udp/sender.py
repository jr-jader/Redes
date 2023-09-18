import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 3030

STRING = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' * 3

class Sender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sent_packets = 0

    def send_message(self, message, checksum, dest):
        print('\nSending packet ' + message[0:2] + '\tCHECKSUM: ' + checksum)
        self.sock.sendto(message.encode('utf-8'), dest)
        self.sent_packets += 1
        print(message[2:len(message) - 4])

    def send(self, data, dest):
        chunks = [data[i: i + 494] for i in range(0, len(data), 494)] # 500bytes chunk (HEADER (2) + PAYLOAD + CHECKSUM(4))
        for chunk in chunks:
            header = str(self.sent_packets).zfill(2) # 2: HEADER size
            checksum = str(hash(header + chunk))
            checksum = checksum[-4:] # CHECKSUM: last 4 bytes of hash
            chunk = header + chunk + checksum
            self.send_message(chunk, checksum, dest)
        print("\nDone sending {!r} packet(s)" .format(self.sent_packets), '\nString sent: ', STRING)   
        self.send

Adam = Sender()
Adam.send(STRING, (UDP_IP, UDP_PORT))