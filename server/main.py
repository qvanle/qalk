import socket
import threading
import os
from dotenv import load_dotenv

# Load .env variables from parent directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# Use defaults if env vars not set
HOST = os.getenv("SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("SERVER_PORT", "5001"))
CHUNK_SIZE = 1024 * 1024
DEFAULT_DIR = os.path.expanduser("~")

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    conn.sendall(
        "Welcome to the File Server.\nCommands:\nLIST\nGET <file1> <file2> ...\nCD <dir>\nPWD\nQUIT\n".encode()
    )
    current_dir = DEFAULT_DIR

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        if data.upper() == "LIST":
            try:
                items = os.listdir(current_dir)
                if not items:
                    response = "No files available."
                else:
                    response_lines = []
                    for item in items:
                        full_path = os.path.join(current_dir, item)
                        if os.path.isdir(full_path):
                            response_lines.append(f"\033[1;34m{item}/\033[0m")
                        else:
                            response_lines.append(item)
                    response = "\n".join(response_lines)
            except Exception as e:
                response = f"ERROR: {str(e)}"
            conn.sendall(response.encode())

        elif data.upper().startswith("GET"):
            try:
                parts = data.split()[1:]
                if not parts:
                    conn.sendall(b"ERROR: No files specified.")
                    continue

                valid_files = []
                for filename in parts:
                    filepath = os.path.join(current_dir, filename)
                    if os.path.isfile(filepath):
                        filesize = os.path.getsize(filepath)
                        valid_files.append((filename, filepath, filesize))

                conn.sendall(f"FILES {len(valid_files)}".encode())
                ack = conn.recv(1024).decode()
                if ack != "READY":
                    continue

                for filename, filepath, filesize in valid_files:
                    conn.sendall(f"{filename} {filesize}".encode())
                    ack = conn.recv(1024).decode()
                    if ack != "READY":
                        continue
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(CHUNK_SIZE):
                            conn.sendall(chunk)
            except Exception as e:
                conn.sendall(f"ERROR: {str(e)}".encode())

        elif data.upper().startswith("CD"):
            try:
                _, new_dir = data.split(maxsplit=1)
                new_path = os.path.abspath(os.path.join(current_dir, new_dir))
                if os.path.isdir(new_path):
                    current_dir = new_path
                    conn.sendall(f"Changed directory to {current_dir}".encode())
                else:
                    conn.sendall(f"ERROR: Directory '{new_dir}' not found.".encode())
            except Exception as e:
                conn.sendall(f"ERROR: {str(e)}".encode())

        elif data.upper() == "PWD":
            conn.sendall(current_dir.encode())

        elif data.upper() == "QUIT":
            break

        else:
            conn.sendall("Invalid command.".encode())

    conn.close()
    print(f"Connection closed: {addr}")

def start_server():
    print(f"Server base directory: {DEFAULT_DIR}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()

