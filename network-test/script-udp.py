import socket
import time
import locale
import threading

locale.setlocale(locale.LC_ALL, '')

PEER1_IP = '127.0.0.1'
PEER2_IP = '127.0.0.1'
PORT1 = 2023
PORT2 = 2024

STRING = 'teste de rede *2023*' * 100

PACKET_SIZE = 500

TIMER = 5

class udp_upload:
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
            return start_time, end_time  # Return start_time and end_time

        except Exception as e:
            print(f"Error during upload: {e}")
        finally:
            self.sock.close()  # Close the socket after upload is complete

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
            time.sleep(0.01)  # Add a small delay to avoid packet loss

class udp_download:
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
            return start_time, end_time  # Return start_time and end_time

        except Exception as e:
            print(f"Error during download: {e}")
        finally:
            self.sock.close()  # Close the socket after download is complete

    def download(self):
        try:
            data, _ = self.sock.recvfrom(PACKET_SIZE)
            self.received_packets += 1
            self.received_bytes += len(data)
        except Exception as e:
            print(f"Error receiving message: {e}")

def main():
    routine = input("Please select your routine\n0 - upload | 1 - download\nYour choice: ")
    while not routine.isdigit() or routine not in ['0', '1']:
        routine = input("ERROR: invalid routine. Please select your routine\n0 - upload | 1 - download\nYour choice: ")

    if routine == '0':
        print('===UDP UPLOAD ROUTINE===\n')
        upload_obj = udp_upload()
        start_time, end_time = upload_obj.start_upload(STRING, (PEER1_IP, PORT1))
        upload_obj.sock.close()
        print(f"Total of bytes sent: {locale.format_string('%d', upload_obj.sent_bytes, grouping=True)} \nTotal of packets sent: {locale.format_string('%d', upload_obj.sent_packets, grouping=True)}")
        print(f'START TIME: {start_time} | END TIME: {end_time}')

        print('\n===UDP DOWNLOAD ROUTINE AFTER UPLOAD===\n')
        download_obj = udp_download((PEER2_IP, PORT2))
        start_time, end_time = download_obj.start_download()
        download_obj.sock.close()
        print(f"Total of bytes received: {locale.format_string('%d', download_obj.received_bytes, grouping=True)} \nTotal of packets received: {locale.format_string('%d', download_obj.received_packets, grouping=True)}")
        print(f'START TIME: {start_time} | END TIME: {end_time}')

    else:
        print('===UDP DOWNLOAD ROUTINE===\n')
        download_obj = udp_download((PEER1_IP, PORT1))
        start_time, end_time = download_obj.start_download()
        download_obj.sock.close()
        print(f"Total of bytes received: {locale.format_string('%d', download_obj.received_bytes, grouping=True)} \nTotal of packets received: {locale.format_string('%d', download_obj.received_packets, grouping=True)}")
        print(f'START TIME: {start_time} | END TIME: {end_time}')
        

        time.sleep(2)

        print('\n===UDP UPLOAD ROUTINE AFTER DOWNLOAD===\n')
        upload_obj = udp_upload()
        start_time, end_time = upload_obj.start_upload(STRING, (PEER2_IP, PORT2))
        upload_obj.sock.close()
        print(f"Total of bytes sent: {locale.format_string('%d', upload_obj.sent_bytes, grouping=True)} \nTotal of packets sent: {locale.format_string('%d', upload_obj.sent_packets, grouping=True)}")
        print(f'START TIME: {start_time} | END TIME: {end_time}')

if __name__ == "__main__":
    main()
