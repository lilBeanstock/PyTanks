# Example file showing a circle moving on screen
from socket import socket
from os import system, name
from math import degrees
from pygame.math import Vector2
from common import HOST, PORT, PYGAME_WINDOW, MAPS, FLOOR, WALL, BUFFER_SIZE, ServerClientPayload, ClientServerPayload
from sys import exit
import Tank
import pygame
import json

def draw_rotated_rectangle(
    screen: pygame.Surface,
    rect_surf: pygame.Surface,
    center_pos: Vector2,
    angle_rad: float
) -> None:
    """
    Rotates a rectangle (Surface) by a given angle in radians and blits it onto the screen.

    Parameters:
        screen (pygame.Surface): The target surface to blit onto (e.g., the main display).
        rect_surf (pygame.Surface): The surface representing the rectangle to rotate.
        center_pos (Vector2): The center position to place the rotated rectangle.
        angle_rad (float): The rotation angle in radians (counterclockwise).

    Returns:
        None
    """

    angle_deg = degrees(angle_rad)  # Convert radians to degrees
    rotated_surf = pygame.transform.rotate(rect_surf, angle_deg)
    new_rect = rotated_surf.get_rect(center=center_pos)
    screen.blit(rotated_surf, new_rect.topleft)

def main():
    # Connect to the server
    client = socket()

    # initial clear of console because of prints...
    system('cls' if name == 'nt' else 'clear')

    try:
        client.connect((HOST, PORT))
        print("Connected!")
    except ConnectionRefusedError:
        print("Unable to connect! Server might be down or have rejected your connnection attempt, please try again.")
        exit(1)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(PYGAME_WINDOW)
    clock = pygame.time.Clock()
    running = True

    # load default payload
    payload: ClientServerPayload = { 
        "mouse": (0,0), 
        "directions": {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        },
        "isShooting": False
    }

    buffer = b""

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case _:
                    pass

        payload["mouse"] = pygame.mouse.get_pos()

        # get keys pressed for processing movement on the server side
        keys = pygame.key.get_pressed()
        payload["directions"]["up"] = keys[pygame.K_w] or keys[pygame.K_UP]
        payload["directions"]["down"] = keys[pygame.K_s] or keys[pygame.K_DOWN]
        payload["directions"]["left"] = keys[pygame.K_a] or keys[pygame.K_LEFT]
        payload["directions"]["right"] = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        payload["isShooting"] = keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(FLOOR)

        # wait for server info about players, map, etc
        while b"\n" not in buffer:
            buffer += client.recv(BUFFER_SIZE)

        # Only keep one JSON object, considering that recv() likes to take in too much info
        serverDataRaw, buffer = buffer.split(b"\n", 1)
        serverData: ServerClientPayload = json.loads(serverDataRaw.decode())

        serverMap = MAPS[serverData["map"]]
        players = serverData["players"]
        bullets = serverData["bullets"]
        # timeRemaining = serverData["timeRemaining"]

        # Render the walls
        for wall in serverMap['walls']:
            x1, y1 = wall[0]
            x2, y2 = wall[1]

            pygame.draw.rect(screen, WALL, pygame.rect.Rect(x1, y1, x2-x1, y2-y1))

        # render tanks
        for tank in players:
            position = tank['position']
            dimensions = tank['dimensions']
            colour = tank['colour']
            turret = tank["turret"]
            cannonDimensions = turret["dimensions"]
            radius = turret["radius"]
            
            hull: pygame.Rect = pygame.rect.Rect(position[0], position[1], dimensions[0], dimensions[1])
            pygame.draw.rect(screen, colour, hull) # hull

            cannon = pygame.Surface(cannonDimensions, pygame.SRCALPHA)
            cannon.fill(turret['cannonColour'])

            pygame.draw.circle(screen, colour, Tank.middle(tank), radius) # turret case

            angle = Tank.calculateMouseAngle(tank)
            draw_rotated_rectangle(screen, cannon, Vector2(Tank.translateCannonPosition(tank)), angle)        

        for bullet in bullets:
            pygame.draw.circle(screen, bullet['colour'], bullet['position'], bullet['radius'])

        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)

        client.sendall(f"{json.dumps(payload)}\n".encode())

    client.close()
    pygame.quit()

if __name__ == "__main__":
    main()