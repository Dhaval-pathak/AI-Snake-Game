import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
# font = pygame.font.SysFont('arial', 25)
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 5

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y,
                                                              BLOCK_SIZE,
                                                              BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4,
                                                              12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x,
                                                        self.food.y,
                                                        BLOCK_SIZE,
                                                        BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

def table_driven_agent(percepts):
    # Define the rules for the agent
    
    # Rule 1: If there is an immediate obstacle in the current movement direction, turn right
    if percepts['immediate_obstacle']:
        return 'Turn Right'
    
    # Rule 2: If food is to the right, turn right
    if percepts['food_right']:
        return 'Turn Right'
    
    # Rule 3: If food is to the left, turn left
    if percepts['food_left']:
        return 'Turn Left'
    
    # Rule 4: If food is above, move up
    if percepts['food_above']:
        return 'Move Up'
    
    # Rule 5: If food is below, move down
    if percepts['food_below']:
        return 'Move Down'
    
    # Rule 6: If none of the above rules apply, continue straight
    return 'Continue Straight'

# Example percepts (replace with actual percept values):
percepts = {
    'immediate_obstacle': False,
    'food_right': True,
    'food_left': False,
    'food_above': False,
    'food_below': False
}

action = table_driven_agent(percepts)
# Get the action based on the percepts
# print(f"The agent's action is: {action}")

if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
                # Inside the game loop:
        percepts = {
            'immediate_obstacle': game._is_collision(),
            'food_right': game.food.x > game.head.x,
            'food_left': game.food.x < game.head.x,
            'food_above': game.food.y < game.head.y,
            'food_below': game.food.y > game.head.y
        }

        action = table_driven_agent(percepts)

        # Update the game state based on the action
        if action == 'Turn Right':
            game.direction = Direction.RIGHT
        elif action == 'Turn Left':
            game.direction = Direction.LEFT
        elif action == 'Move Up':
            game.direction = Direction.UP
        elif action == 'Move Down':
            game.direction = Direction.DOWN

      
        # game loop
        game_over, score = game.play_step()

    
    

        if game_over == True:
            break

    print('Final Score', score)
    pygame.quit()


