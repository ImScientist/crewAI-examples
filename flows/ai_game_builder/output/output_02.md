```python
import pygame
import random

# initialize pygame
pygame.init()

# constants
width, height = 600, 400
grid_size = 20
grid_width = width // grid_size
grid_height = height // grid_size
snake_color = (0, 255, 0)
food_color = (255, 0, 0)
background_color = (0, 0, 0)
fps = 10

# initialize game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake game")

# directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(grid_width // 2, grid_height // 2)]
        self.direction = right
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        opposite_direction = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_direction:
            self.direction = new_direction
    
    def eat(self):
        self.grow = True

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:] or head[0] < 0 or head[0] >= grid_width or head[1] < 0 or head[1] >= grid_height

class Food:
    def __init__(self, snake_body):
        self.position = self.spawn_food(snake_body)
    
    def spawn_food(self, snake_body):
        while True:
            position = (random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
            if position not in snake_body:
                return position

def draw_snake(snake):
    for segment in snake.body:
        pygame.draw.rect(screen, snake_color, (segment[0] * grid_size, segment[1] * grid_size, grid_size, grid_size))

def draw_food(food):
    pygame.draw.rect(screen, food_color, (food.position[0] * grid_size, food.position[1] * grid_size, grid_size, grid_size))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake.body)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(up)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(down)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(left)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(right)

        snake.move()

        if snake.check_collision():
            pygame.quit()
            return

        if snake.body[0] == food.position:
            snake.eat()
            score += 10
            food = Food(snake.body)

        screen.fill(background_color)
        draw_snake(snake)
        draw_food(food)
        pygame.display.flip()

        clock.tick(fps)

if __name__ == "__main__":
    main()
```