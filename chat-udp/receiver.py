import socket, locale
from fpdf import FPDF

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

RECV_IP = '127.0.0.1'
RECV_PORT = 3031

PACKET_SIZE = 1500

HEADER_SIZE = 2
CHECKSUM_SIZE = 4
PAYLOAD_SIZE = PACKET_SIZE - HEADER_SIZE - CHECKSUM_SIZE

class Receiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
        self.sock.bind((RECV_IP, RECV_PORT))
        self.received_packets = 0

    def receive_message(self):
        data = ''
        while True:
            chunk, addr = self.sock.recvfrom(PACKET_SIZE)
            chunk = chunk.decode('utf-8')
            
            header = chunk[:HEADER_SIZE] # Extract header of size 2
            print(f"\nReceived packet number {int(header)}")
            self.received_packets += 1
            
            checksum_received = chunk[len(chunk) - CHECKSUM_SIZE :]
            checksum_calculated = str(hash(chunk[: -CHECKSUM_SIZE]))[-CHECKSUM_SIZE :]
            print(f"CHECKSUM received: {checksum_received} \tCHECKSUM calculated: {checksum_calculated}")
            
            data += ''.join(chunk[HEADER_SIZE : len(chunk) - CHECKSUM_SIZE]) # Join remaining parts of chunk
            if len(chunk) < PACKET_SIZE:
                break
        # print(f"\nReceived string: {data}")
        self.sock.close()

    def receive_report(self):
        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        tcp_sock.bind((RECV_IP, RECV_PORT))
        tcp_sock.listen(1)
        sender_socket, sender_address = tcp_sock.accept()
        print('\nConnected to ', sender_address)

        r = sender_socket.recv(1024).decode()
        report = r.split('|')
        report[0] = 'Tamanho do arquivo: ' + report[0] + ' bytes'
        packets_sent = report[1]
        report[1] = 'Número de pacotes enviados: ' + report[1]
        rate = report[2]
        report[2] = 'Número de pacotes recebidos: ' + str(self.received_packets)
        report.append('Número de pacotes perdidos: ' + str(int(packets_sent) - self.received_packets))
        report.append('Taxa de transmissão: ' +  locale.format_string('%.3f', float(rate), grouping=True) + ' b/s')
        report.append('Tamanho do(s) pacote(s) transmitido(s): ' + str(PACKET_SIZE))

        print('Received report: ', report)

        tcp_sock.close()

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'TRAB-03-RELATÓRIO', 0, 1, 'C')
        pdf.ln(10)

        pdf.set_font('Arial', '', 12)
        for i in range(len(report)):
            pdf.cell(200, 10, txt='- ' + report[i], ln=i+1, align='L')
        pdf.output('TRAB-03-RELATORIO')

recv = Receiver()
recv.receive_message()
recv.receive_report()