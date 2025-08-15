#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Define a structure for a point (x, y)
typedef struct {
    int x;
    int y;
} Point;

typedef struct {
    Point start;
    Point end;
} Wall;

typedef struct {
    Wall* walls;
    int wall_count;
} Map;

typedef struct {
    float x;
    float y;
} Velocity;

// Define a structure for the Direction
typedef struct {
    bool up;
    bool down;
    bool left;
    bool right;
} Direction;

// Define a structure for the Player
typedef struct {
    Point position;            // Player position
    Point dimensions;          // Player dimensions (width, height)
    unsigned char colour[3];   // Player colour (RGB)
    Direction directions;      // Player movement directions
    Velocity velocity;
    int kills;                 // Kills in each match
    int wins;                  // Wins
} Player;

typedef struct {
    int x;      // x-coordinate of the top-left corner
    int y;      // y-coordinate of the top-left corner
    int width;  // width of the rectangle
    int height; // height of the rectangle
} Rectangle;

// Function to check if two rectangles overlap
bool rectangles_overlap(Rectangle rect1, Rectangle rect2) {
    return (rect1.x < rect2.x + rect2.width &&
            rect1.x + rect1.width > rect2.x &&
            rect1.y < rect2.y + rect2.height &&
            rect1.y + rect1.height > rect2.y);
}

Point wall_dimensions(Point from, Point to) {
    Point dimensions;
    dimensions.x = to.x - from.x;  // Width
    dimensions.y = to.y - from.y;  // Height

    return dimensions;
}

bool player_wall_overlap(Wall wall, Player player) {
    Point wallDimensions = wall_dimensions(wall.start, wall.end);

    Rectangle wallRectangle;
    wallRectangle.x = wall.start.x;
    wallRectangle.y = wall.start.y;
    wallRectangle.width = wallDimensions.x;
    wallRectangle.height = wallDimensions.y;

    Rectangle playerRectangle;
    playerRectangle.x = player.position.x + (int)player.velocity.x;
    playerRectangle.y = player.position.y + (int)player.velocity.y;
    playerRectangle.width = player.dimensions.x;
    playerRectangle.height = player.dimensions.y;

    return rectangles_overlap(wallRectangle, playerRectangle);
}

void handle_player_walls_overlap(Map map, Player *player) {
    for (int i = 0; i < map.wall_count; i++) {
        bool isOverlapping = player_wall_overlap(map.walls[i], *player);
        if (!isOverlapping) continue;
    
        if ((*player).velocity.y > 0 && (*player).directions.down) (*player).velocity.y = 0;
        if ((*player).velocity.y < 0 && (*player).directions.up) (*player).velocity.y = 0;
        if ((*player).velocity.x > 0 && (*player).directions.right) (*player).velocity.x = 0;
        if ((*player).velocity.x < 0 && (*player).directions.left) (*player).velocity.x = 0;

        break;
    }
}

bool player_player_overlap(Player playerFocus, Player playerCheck) {
    // player identifies as a rectangle. happy pride 💖💖💖

    Rectangle playerFocusRectangle;
    playerFocusRectangle.x = playerFocus.position.x + (int)playerFocus.velocity.x;
    playerFocusRectangle.y = playerFocus.position.y + (int)playerFocus.velocity.y;
    playerFocusRectangle.width = playerFocus.dimensions.x;
    playerFocusRectangle.height = playerFocus.dimensions.y;

    Rectangle playerCheckRectangle;
    playerCheckRectangle.x = playerCheck.position.x;
    playerCheckRectangle.y = playerCheck.position.y;
    playerCheckRectangle.width = playerCheck.dimensions.x;
    playerCheckRectangle.height = playerCheck.dimensions.y;

    return rectangles_overlap(playerFocusRectangle, playerCheckRectangle);
}

void handle_player_player_overlap(Player *playerFocus, Player *playerCheck) {
    bool isOverlapping = player_player_overlap(*playerFocus, *playerCheck);
    if (!isOverlapping) return;

    if ((*playerFocus).velocity.y > 0 && (*playerFocus).directions.down) (*playerFocus).velocity.y = 0;
    if ((*playerFocus).velocity.y < 0 && (*playerFocus).directions.up) (*playerFocus).velocity.y = 0;
    if ((*playerFocus).velocity.x > 0 && (*playerFocus).directions.right) (*playerFocus).velocity.x = 0;
    if ((*playerFocus).velocity.x < 0 && (*playerFocus).directions.left) (*playerFocus).velocity.x = 0;
}

void handle_all(Map map, Player *players, size_t playerCount) {
    // give players velocity based on key presses

    for (size_t i = 0; i < playerCount; i++) {
        players[i].velocity.y = 0;
        players[i].velocity.x = 0;
        
        if (players[i].directions.up) players[i].velocity.y = -2;
        if (players[i].directions.down) players[i].velocity.y = 2;
        if (players[i].directions.left) players[i].velocity.x = -2;
        if (players[i].directions.right) players[i].velocity.x = 2;
    }

    // handle player to walls overlapping
    for (size_t i = 0; i < playerCount; i++) {
        handle_player_walls_overlap(map, &(players[i]));
    }

    // handle player to player overlapping
    for (size_t i = 0; i < playerCount; i++) {
        for (size_t j = 0; j < playerCount; j++) {
            if (i == j) continue;
            
            handle_player_player_overlap(&(players[i]), &(players[j]));
        }
    }

    // eventually handle bullet stuff...

    // update position based on remaining velocity
    for (size_t i = 0; i < playerCount; i++) {
        players[i].position.x += players[i].velocity.x;
        players[i].position.y += players[i].velocity.y;
    }
}
