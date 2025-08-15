# PyTanks Information
A tank game that looks like the 2D tank game from the Wii Play game.

## Python
Python will be used for rendering and socket handling.

## C
C will be used for collision handling and movement updating for faster performance.

## Python + C configuration
Python will be running the client and server; however, all movement will be processed by the server using C, whereby positions of walls, borders, and players will be used as parameters alongside current movement, so that the C function(s) can update values accordingly

## Client and Files
The client is defined only by client.py and the modules Tank.py and common.py; they need to be in the same folder. Everything except client.py is used by the folder, whereby server.py is the main file. The client file and its dependencies need not be in the same folder as the server and its dependencies.

# Updates and Todo
- [x] define game state (maps, time limits, player health?, wins, etc)
- [x] send payload information form server to client at 60(?) ticks per second to all clients
- [x] render all walls present in the map
- [x] render tanks with appropriate colour and position
- [x] make turret attached to tank and rotate towards mouse
- [x] run C functions from python
- [x] make translator for python to C
	- [x] for the Map
	- [x] for the players
- [x] player movement
	- [x] FIXME: bug where players remain after disconnect and fly off into the distance
	- [x] collision against walls
	- [x] collision against other players
- [ ] add bullet objects
	- [ ] bullet collisions against walls to bounce
	- [ ] hit detection on players and other bullets to despawn
- [ ] handle game mechanics
	- [ ] game time start and end
	- [ ] kills and wins update
	- [ ] create more maps and make it switch to a random one when match is over
	- [ ] render game time for client alongside wins and kills per round
