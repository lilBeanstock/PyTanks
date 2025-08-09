from ctypes import CDLL
from socket import socket
from common import HOST, PORT
import asyncio
from os import path

# Import C functions
cFunctions = CDLL(path.join(path.dirname(__file__), "lib.so"))
# cFunctions.myFunction.argtypes = [ctypes.c_int]

# Track connected clients
clients: set[socket] = set()

# Function for handling client data
async def handle_client(loop: asyncio.AbstractEventLoop, client_sock: socket, client_addr: str):
    print(f"[+] Connection from {client_addr}")
    clients.add(client_sock) # add client to client list
    BUFFER_SIZE = 1024

    try:
        while True:
            data = await loop.sock_recv(client_sock, BUFFER_SIZE)
            if not data:
                print(f"[-] Client {client_addr} disconnected")
                break

            message = data.decode().strip()
            print(f"[{client_addr}] {message}")

            # # Echo to the same client
            # await loop.sock_sendall(client_sock, f"You said: {message}\n".encode())

    except ConnectionResetError:
        print(f"[!] Connection reset by {client_addr}")
    finally:
        clients.remove(client_sock)
        client_sock.close()

async def create_socket():
    server = socket()
    server.bind((HOST, PORT))
    server.setblocking(False)
    server.listen(5)

    loop = asyncio.get_running_loop()
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        client_sock, client_addr = await loop.sock_accept(server)
        client_sock.setblocking(False)
        loop.create_task(handle_client(loop, client_sock, client_addr))

async def main():
    await create_socket()

# run server function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")