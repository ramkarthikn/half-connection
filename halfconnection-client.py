import socket
import time

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to server {HOST}:{PORT}")

    # 1. Client receives initial message from server
    data = s.recv(1024)
    print(f"Received from server: {data.decode('utf-8')}")

    # 2. Server is expected to have sent a FIN and shut down its write half.
    # The client can still send data.

    messages_to_send = ["Hi server, I got your message!", "Are you still listening?", "One more message before I close."]
    for msg in messages_to_send:
        s.sendall(msg.encode('utf-8'))
        print(f"Sent to server: '{msg}'")
        time.sleep(1) # Small delay

    print("Client finished sending messages.")
    # The client will eventually close its connection, sending its own FIN.
    # The server will then receive an empty 'data' in its recv loop and close.

print("Client connection closed.")