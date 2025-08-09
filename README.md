# PyTanks Information
A tank game that looks like the 2D tank game from the Wii Play game.

## Python
Python will be used for rendering and socket handling.

## C
C will be used for collision handling and movement updating for faster performance.

## Python + C configuration
Python will be running the client and server; however, all movement will be processed by the server using C, whereby positions of walls, borders, and players will be used as parameters alongside current movement, so that the C function(s) can update values accordingly

# Updates and Todo
- [ ] game state (maps, time limits, player health?, wins, etc)
- [ ] send payload information form server to client at 60(?) ticks per second to all clients
- [ ] render all walls present in the map
- [ ] render tanks with appropriate colour and position
- [ ] make turret attached to tank and rotate towards mouse
- [ ] player movement
	- [ ] collision against walls and other players
- [ ] add bullet objects
    - [ ] bullet collisions against walls
		- [ ] hit detection on players and other bullets
