import socket
import threading
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        # 1. Server sends data to the client
        message = "Hello from the server! I'm about to close my sending half."
        conn.sendall(message.encode('utf-8'))
        print(f"Sent: '{message}' to {addr}")
        time.sleep(1) # Give client a moment to receive

        # 2. Server initiates a half-close (SHUT_WR)
        # This sends a FIN packet to the client, indicating no more data will be sent from the server.
        conn.shutdown(socket.SHUT_WR)
        print(f"Server has shut down its writing half for {addr}.")
        print("Server can no longer send data to this client.")

        # 3. Server can still receive data from the client
        print(f"Server is now waiting to receive data from {addr}...")
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} has closed its connection or sent no more data.")
                break
            print(f"Received from {addr}: {data.decode('utf-8')}")

    except ConnectionResetError:
        print(f"Client {addr} forcibly closed the connection.")
    except Exception as e:
        print(f"An error occurred with client {addr}: {e}")
    finally:
        print(f"Closing connection with {addr}")
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            # Start a new thread to handle each client connection
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()