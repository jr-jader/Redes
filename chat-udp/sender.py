import socket, time, locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

RECV_IP = '127.0.0.1'
RECV_PORT = 3030

STRING = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.' * 5

PACKET_SIZE = 500

HEADER_SIZE = 2
CHECKSUM_SIZE = 4
PAYLOAD_SIZE = PACKET_SIZE - HEADER_SIZE - CHECKSUM_SIZE

class Sender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sent_packets = 0

    def send_message(self, message, checksum, dest):
        print('\nSending packet ' + message[:HEADER_SIZE] + '\tCHECKSUM: ' + checksum)
        self.sock.sendto(message.encode('utf-8'), dest)
        self.sent_packets += 1

    def send(self, data, dest):
        start_time = time.time()
        end_time = 0
        chunks = [data[i: i + PAYLOAD_SIZE] for i in range(0, len(data), PAYLOAD_SIZE)]
        for chunk in chunks:
            header = str(self.sent_packets).zfill(HEADER_SIZE)
            checksum = str(hash(header + chunk))
            checksum = checksum[-CHECKSUM_SIZE:] # CHECKSUM: last 4 bytes of hash
            chunk = header + chunk + checksum
            self.send_message(chunk, checksum, dest)
        end_time = time.time()
        rate = len(data) * 8 / (end_time - start_time)
        print('\nDone sending ', self.sent_packets, ' packet(s)\nTransmission rate: ', locale.format_string('%.3f', rate, grouping=True), 'b/s')
        self.sock.close()

        report_data = str(len(data)) + '|' + str(self.sent_packets) + '|' + str(rate)
        time.sleep(1)
        print('\nSending report to ', dest)
        self.send_report(report_data, dest)
    
    def send_report(self, data, dest):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.connect(dest)
        tcp_sock.send(data.encode())
        tcp_sock.close()
        print('Done sending report')

Adam = Sender()
Adam.send(STRING, (RECV_IP, RECV_PORT))