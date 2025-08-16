from socket import socket
from typing import Any, Dict, Callable, Awaitable, List
from common import HOST, PORT, Player, ServerClientPayload, BUFFER_SIZE, ClientServerPayload, MAPS, Bullet
import Tank
import asyncio
import json
import ctypes
from math import cos, sin
from cLib import lib, makePlayerArr, makePlayerList, translateMapC, makeBulletArr, makeBulletList

# Track connected clients and the current map
clients: Dict[socket, Player] = {}
bullets: Dict[int, List[Bullet]] = {}

# define game state
gameState: ServerClientPayload = {
    "map": 0,
    "timeRemaining": 0,
    "players": [],
    "bullets": []
} # TODO, MAKE FUNCTION FOR CHANGING MAP AFTER MATCH END

# Function for handling client data
async def handle_client(loop: asyncio.AbstractEventLoop, client_sock: socket, client_addr: Any):
    player_id = client_sock.fileno()
    print(f"[+] Connection from {client_addr} with ID {player_id}")
    clients[client_sock] = Tank.randomPlayer(player_id) # add client to client list, alongside their player state
    bullets[player_id] = [] # add client to client list, alongside their player state

    try:
        buffer = b""
        prevShooting = False

        while True:
            while b"\n" not in buffer:
                buffer += await loop.sock_recv(client_sock, BUFFER_SIZE)
                if not buffer:
                    print(f"[-] Client {client_addr} disconnected")
                    break
            if not buffer:
                break

            player = clients.get(client_sock)
            if player is None:
                break

            # Only keep one JSON object, considering that recv() likes to take in too much info
            data, buffer = buffer.split(b"\n", 1)

            # get info from client to process
            payload: ClientServerPayload = json.loads(data.decode())

            player['turret']['mouse'] = payload['mouse']
            player['turret']['isShooting'] = payload['isShooting']
            player['directions'] = payload['directions']

            if payload["isShooting"] and len(bullets[player_id]) < 5 and not prevShooting:
                prevShooting = True
                bullet: Bullet = {
                    "bounces": 0,
                    "colour": player['colour'],
                    "player_id": player_id,
                    "position": Tank.bulletInitPosition(player),
                    "radius": 5,
                    "velocity": {
                        "x": 5*cos(Tank.calculateMouseAngle(player)),
                        "y": -5*sin(Tank.calculateMouseAngle(player))
                    }
                }

                bullets[player_id].append(bullet)
            if not payload["isShooting"]: 
                prevShooting = False

            clients[client_sock] = player

    except ConnectionResetError:
        print(f"[!] Connection reset by {client_addr} with ID {player_id}")
    finally:
        # del player
        client_sock.close()
        del clients[client_sock]
        if bullets[player_id]: del bullets[player_id]

# handle collision, movement, and the broadcasting of information to the clients
async def handle_game(loop: asyncio.AbstractEventLoop) -> None:
    # set gameState's "players" as equal to that of the client list's "players"
    players = list(clients.values())
    players_arr = makePlayerArr(players)
    playersLen = ctypes.c_size_t(len(players))
    gameMap = translateMapC(MAPS[gameState['map']])

    bulletsList = list(bullets.values())
    bulletsListFlattened = [bull for sublist in bulletsList for bull in sublist]
    gameBullets = makeBulletArr(bulletsListFlattened)
    gameBulletsLen = ctypes.c_size_t(len(gameBullets))

    # handle all collisions, bullets, and deaths
    lib.handle_all(gameMap, players_arr, playersLen, gameBullets, gameBulletsLen)
    gameState['players'] = makePlayerList(players_arr,players) # will use python's list because of the turret information
    gameState['bullets'] = makeBulletList(gameBullets)
    
    currId = 0
    for i in clients:
        bullets[i.fileno()] = []

    for i in gameState["bullets"]:
        if currId != i["player_id"]: currId = i["player_id"]
        
        # check for despawn conditions
        if i["bounces"] >= 4: continue

        bullets[currId].append(i) # add bullet back into its appropriate id group
    
    # and send renewed information to users/clients
    for i,sock in enumerate(clients):
        # update client dictionary
        clients[sock] = gameState["players"][i]

        # send game state and player states to all clients (i never knew that)
        # need not specify who is who, player only needs 2 neurons for that.

        await loop.sock_sendall(sock, f"{json.dumps(gameState)}\n".encode())
    

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