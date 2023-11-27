import socket
import time
import locale

locale.setlocale(locale.LC_ALL, '')

PEER1_IP = '127.0.0.1'
PEER2_IP = '127.0.0.1'
PORT1 = 2023
PORT2 = 2024

STRING = 'teste de rede *2023*' * 100

PACKET_SIZE = 500

TIMER = 5  # Adjusted the timer

class UDPUpload:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sent_bytes = 0
        self.sent_packets = 0

    def start_upload(self, data, dest):
        try:
            print(f'Now connected to Upload on {dest}\n')
            start_time = time.time()
            while time.time() - start_time < TIMER:
                self.upload(data, dest)
            end_time = time.time()
            return start_time, end_time

        except Exception as e:
            print(f"Error during upload: {e}")
        finally:
            self.sock.close()

    def send_message(self, message, dest):
        try:
            self.sock.sendto(message.encode('utf-8'), dest)
            self.sent_packets += 1
            self.sent_bytes += len(message)
        except Exception as e:
            print(f"Error sending message: {e}")

    def upload(self, data, dest):
        chunks = [data[i: i + PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
        for chunk in chunks:
            self.send_message(chunk, dest)
            time.sleep(0.001)

class UDPDownload:
    def __init__(self, dest):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(dest)
        self.received_bytes = 0
        self.received_packets = 0
        
    def start_download(self):
        try:
            print(f'Now connected to Download on {self.sock.getsockname()}\n')
            start_time = time.time()
            while time.time() - start_time < TIMER:
                self.download()
            end_time = time.time()
            return start_time, end_time

        except Exception as e:
            print(f"Error during download: {e}")
        finally:
            self.sock.close()

    def download(self):
        try:
            data, _ = self.sock.recvfrom(PACKET_SIZE)
            self.received_packets += 1
            self.received_bytes += len(data)

        except Exception as e:
            print(f"Error receiving message: {e}")

def main():
    routine = input("Por favor, escolha sua rotina\n0 - upload | 1 - download\nSua escolha: ")
    while not routine.isdigit() or routine not in ['0', '1']:
        routine = input("ERRO: rotina inválida. Por favor, escolha sua rotina\n0 - upload | 1 - download\nSua escolha: ")

    if routine == '0':
        print('=== ROTINA DE UPLOAD UDP ===\n')
        upload_obj = UDPUpload()
        start_time_upload, end_time_upload = upload_obj.start_upload(STRING, (PEER1_IP, PORT1))
        print(f"Total de bytes enviados: {locale.format_string('%d', upload_obj.sent_bytes, grouping=True)} \nTotal de pacotes enviados: {locale.format_string('%d', upload_obj.sent_packets, grouping=True)}")
        print(f'START TIME: {start_time_upload} | END TIME: {end_time_upload}')


        print('\n=== ROTINA DE DOWNLOAD UDP APÓS O UPLOAD ===\n')
        download_obj = UDPDownload((PEER2_IP, PORT2))
        start_time_download, end_time_download = download_obj.start_download()
        print(f"Total de bytes recebidos: {locale.format_string('%d', download_obj.received_bytes, grouping=True)} \nTotal de pacotes recebidos: {locale.format_string('%d', download_obj.received_packets, grouping=True)}")
        print(f'START TIME: {start_time_download} | END TIME: {end_time_download}')

    else:
        print('=== ROTINA DE DOWNLOAD UDP ===\n')
        download_obj = UDPDownload((PEER1_IP, PORT1))
        start_time_download, end_time_download = download_obj.start_download()
        print(f"Total de bytes recebidos: {locale.format_string('%d', download_obj.received_bytes, grouping=True)} \nTotal de pacotes recebidos: {locale.format_string('%d', download_obj.received_packets, grouping=True)}")
        print(f'START TIME: {start_time_download} | END TIME: {end_time_download}')

        time.sleep(2)

        print('\n=== ROTINA DE UPLOAD UDP APÓS O DOWNLOAD ===\n')
        upload_obj = UDPUpload()
        start_time_upload, end_time_upload = upload_obj.start_upload(STRING, (PEER2_IP, PORT2))
        print(f"Total de bytes enviados: {locale.format_string('%d', upload_obj.sent_bytes, grouping=True)} \nTotal de pacotes enviados: {locale.format_string('%d', upload_obj.sent_packets, grouping=True)}")
        print(f'START TIME: {start_time_upload} | END TIME: {end_time_upload}')

if __name__ == "__main__":
    main()