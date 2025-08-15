from socket import socket
from typing import Any, Dict, Callable, Awaitable
from common import HOST, PORT, Player, ServerClientPayload, BUFFER_SIZE, ClientServerPayload, MAPS
import Tank
import asyncio
import json
import ctypes
from cLib import PlayerC, lib, makePlayerArr, makePlayerList, translateMapC

# Track connected clients and the current map
clients: Dict[socket, Player] = {}

# define game state
gameState: ServerClientPayload = {
    "map": 0,
    "players": [],
    "timeRemaining": 0
} # TODO, MAKE FUNCTION FOR CHANGING MAP AFTER MATCH END

# Function for handling client data
async def handle_client(loop: asyncio.AbstractEventLoop, client_sock: socket, client_addr: Any):
    print(f"[+] Connection from {client_addr}")
    clients[client_sock] = Tank.randomPlayer() # add client to client list, alongside their player state
    player = clients[client_sock]

    try:
        buffer = b""

        while True:
            while b"\n" not in buffer:
                buffer += await loop.sock_recv(client_sock, BUFFER_SIZE)
                if not buffer:
                    print(f"[-] Client {client_addr} disconnected")
                    break
            if not buffer:
                break

            # Only keep one JSON object, considering that recv() likes to take in too much info
            data, buffer = buffer.split(b"\n", 1)

            # get info from client to process
            payload: ClientServerPayload = json.loads(data.decode())
            print(f"[{client_addr}] {payload}")

            player['turret']['mouse'] = payload['mouse']
            player['directions'] = payload['directions']

    except ConnectionResetError:
        print(f"[!] Connection reset by {client_addr}")
    finally:
        # del player
        client_sock.close()
        del clients[client_sock]

# handle collision, movement, and the broadcasting of information to the clients
async def handle_game(loop: asyncio.AbstractEventLoop) -> None:
    # set gameState's "players" as equal to that of the client list's "players"
    players = list(clients.values())
    players_arr = makePlayerArr(players)
    _returnedPlayers: ctypes.Array[PlayerC] = lib.handle_all(translateMapC(MAPS[gameState['map']]), players_arr, len(players))
    gameState['players'] = makePlayerList(players_arr,players) # will use python's list because of the turret information

    # and send renewed information to users/clients
    for i,sock in enumerate(clients):
        # update client dictionary
        clients[sock] = gameState["players"][i]

        # send game state and player states to all clients (i never knew that)
        # need not specify who is who, player only needs 2 neurons for that.

        await loop.sock_sendall(sock, f"{json.dumps(gameState)}\n".encode())
            

    pass

async def create_socket(loop: asyncio.AbstractEventLoop):
    server = socket()
    server.bind((HOST, PORT))
    server.setblocking(False) # needed for async
    server.listen(5)

    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        try:
            client_sock, client_addr = await loop.sock_accept(server)
            client_sock.setblocking(False)
            loop.create_task(handle_client(loop, client_sock, client_addr))
        except:
            server.close()
            break

async def set_interval(interval: float, func: Callable[..., Awaitable[None]], *args: Any, **kwargs: Any):
    while True:
        await func(*args, **kwargs)
        await asyncio.sleep(interval)

async def main():
    loop = asyncio.get_running_loop()

    asyncio.create_task(create_socket(loop))
    asyncio.create_task(set_interval(1 / 60, handle_game, loop))
    await asyncio.Event().wait() # Keeps the main coroutine alive

# run server function
if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("\n[SERVER] Shutting down, main function quit.")
    except KeyboardInterrupt:
        print("\n[SERVER] Interrupted: Shutting down.")