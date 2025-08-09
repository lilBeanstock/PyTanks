from ctypes import CDLL
from socket import socket
from os import path
from typing import Any, Dict
from common import HOST, PORT, Player, BUFFER_SIZE
import Tank
import asyncio

# Import C functions
cFunctions = CDLL(path.join(path.dirname(__file__), "lib.so"))
# cFunctions.myFunction.argtypes = [ctypes.c_int]

# Track connected clients and the current map
clients: Dict[socket, Player] = {}

curr_map = 0 # TODO, MAKE FUNCTION FOR CHANGING MAP AFTER MATCH END

# Function for handling client data
async def handle_client(loop: asyncio.AbstractEventLoop, client_sock: socket, client_addr: Any):
    print(f"[+] Connection from {client_addr}")
    clients[client_sock] = Tank.randomPlayer() # add client to client list

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
        del clients[client_sock]
        client_sock.close()

# handle collision, movement, and the broadcasting of information to the clients
async def handle_game(loop: asyncio.AbstractEventLoop):
    return 0

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
        loop.create_task(handle_game(loop))

async def main():
    await create_socket()

# run server function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")