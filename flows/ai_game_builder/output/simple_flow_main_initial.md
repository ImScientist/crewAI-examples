```python
import pygame
import random

# Constants
GRID_SIZE = 20
CELL_SIZE = 20
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE // 2, GRID_SIZE // 2)]
        self.direction = (0, -1)
        self.grow_snake = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.grow_snake:
            self.body.insert(0, new_head)
            self.grow_snake = False
        else:
            self.body.insert(0, new_head)
            self.body.pop()

    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction

    def grow(self):
        self.grow_snake = True

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def collides_with_bounds(self):
        head_x, head_y = self.body[0]
        return head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE


class Food:
    def __init__(self, snake_body):
        self.position = self.spawn_food(snake_body)

    def spawn_food(self, snake_body):
        while True:
            position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if position not in snake_body:
                return position


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.body)

    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))

        snake.move()

        if snake.collides_with_self() or snake.collides_with_bounds():
            running = False

        if snake.body[0] == food.position:
            score += 10
            snake.grow()
            food = Food(snake.body)

        screen.fill(BLACK)
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        food_x, food_y = food.position
        pygame.draw.rect(screen, RED, (food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    print(f"Game Over! Your final score is: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()
```