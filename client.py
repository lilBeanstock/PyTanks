# Example file showing a circle moving on screen
import pygame
from socket import socket
from common import HOST, PORT

# connect
client = socket()
client.connect((HOST, PORT))
print("connected!")

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
            case _:
                pass

    # get keys pressed for processing movement on the server side
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        client.send("w".encode())
    if keys[pygame.K_s]:
        client.send("s".encode())
    if keys[pygame.K_a]:
        client.send("a".encode())
    if keys[pygame.K_d]:
        client.send("d".encode())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((249, 210, 109))

    # wait for server info about players, map, etc
    # serverDataRaw = client.recv(BUFFER_SIZE) # encoded JSON data
    # serverData: ServerClientPayload = json.loads(serverDataRaw.decode())

    # serverMap = serverData["map"]
    # players = serverData["players"]
    # TODO: make server send info to clients

    # Render the walls
    wall = pygame.rect.Rect(0, 0, 50, 50)
    pygame.draw.rect(screen, (188, 140, 64), wall)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60

client.close()
pygame.quit()



# pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0


# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")

#     pygame.draw.circle(screen, "red", player_pos, 40)

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         player_pos.y -= 300 * dt
#     if keys[pygame.K_s]:
#         player_pos.y += 300 * dt
#     if keys[pygame.K_a]:
#         player_pos.x -= 300 * dt
#     if keys[pygame.K_d]:
#         player_pos.x += 300 * dt

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000

