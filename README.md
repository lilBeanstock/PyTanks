# Wii Tanks
A tank game that looks like the 2D tank game from the Wii Play game.

## Python
Python will be used for rendering and socket handling.

## C
C will be used for collision handling and movement updating for faster performance.

## Python + C configuration
Python will be running the client and server; however, all movement will be processed by the server using C, whereby positions of walls, borders, and players will be used as parameters alongside current movement, so that the C function(s) can update values accordingly