import socket
import os
from dotenv import load_dotenv

# Load .env from parent directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# Fallbacks
SERVER_HOST = os.getenv("SERVER_HOST", "localhost")
SERVER_PORT = int(os.getenv("SERVER_PORT", "5001"))
CHUNK_SIZE = 1024 * 1024
DOWNLOAD_DIR = os.path.expanduser("~")

def receive_file(sock, filename, filesize):
    filepath = os.path.join(DOWNLOAD_DIR, filename)
    received = 0
    part_num = 1

    with open(filepath, 'wb') as f:
        while received < filesize:
            chunk = sock.recv(min(CHUNK_SIZE, filesize - received))
            if not chunk:
                break
            f.write(chunk)
            received += len(chunk)
            percent = received * 100 // filesize
            print(f"Downloading {filename} part {part_num} .... {percent}%")
            part_num += 1 if len(chunk) == CHUNK_SIZE else 0

    print(f"Download complete: {filename}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        print(s.recv(1024).decode())

        while True:
            cmd = input("Enter command: ").strip()
            if cmd.upper() == "QUIT":
                s.sendall(b"QUIT")
                break

            s.sendall(cmd.encode())
            response = s.recv(4096).decode()

            if cmd.upper().startswith("GET") and response.startswith("FILES"):
                try:
                    num_files = int(response.split()[1])
                    s.sendall(b"READY")

                    for _ in range(num_files):
                        header = s.recv(1024).decode()
                        filename, filesize = header.split()
                        filesize = int(filesize)
                        s.sendall(b"READY")
                        receive_file(s, filename, filesize)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(response)

if __name__ == "__main__":
    main()

