import pygame
import random
from enum import Enum
from collections import namedtuple
import tkinter as tk
from tkinter import messagebox

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BROWN = (118, 175, 60)
YELLOW = (255, 255, 0)
LIGHT_BLACK = (30, 30, 30)

BLOCK_SIZE = 20
SPEED = 5

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.best_score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

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
            self._game_over_dialog()
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # Update best score
        if self.score > self.best_score:
            self.best_score = self.score

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(LIGHT_BLACK)

        for i, pt in enumerate(self.snake):
            x, y = pt.x + BLOCK_SIZE // 2, pt.y + BLOCK_SIZE // 2
            outer_oval_rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

            
            pygame.draw.ellipse(self.display, BROWN, outer_oval_rect)
            
            if i == 0:
                eye_radius = 3
                pygame.draw.circle(self.display, WHITE, (x + BLOCK_SIZE // 4, y + BLOCK_SIZE // 4), eye_radius)
                pygame.draw.circle(self.display, WHITE, (x + 3 * BLOCK_SIZE // 4, y + BLOCK_SIZE // 4), eye_radius)

        pygame.draw.rect(self.display, RED, (self.food.x + BLOCK_SIZE // 2, self.food.y + BLOCK_SIZE // 2, BLOCK_SIZE // 2, BLOCK_SIZE // 2))
        

        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(self.score), True, WHITE)
        best_score_text = font.render("Best Score: " + str(self.best_score), True, WHITE)
        self.display.blit(best_score_text, [self.w - 180, 10])
        self.display.blit(text, [10, 10])
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

    def _game_over_dialog(self):
        # pygame.display.iconify()  
        tk.Tk().withdraw()
        messagebox.showinfo("Game Over", f"Your Score: {self.score}\nBest Score: {self.best_score}")
        pygame.quit()


if __name__ == '__main__':
    game = SnakeGame()

    # Game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over:
            break
