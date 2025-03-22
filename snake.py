import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 10
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = (CELL_SIZE, 0)
score = 0
level = 1
speed = 10

walls = [(0, i) for i in range(0, HEIGHT, CELL_SIZE)] + [(WIDTH - CELL_SIZE, i) for i in range(0, HEIGHT, CELL_SIZE)] + \
        [(i, 0) for i in range(0, WIDTH, CELL_SIZE)] + [(i, HEIGHT - CELL_SIZE) for i in range(0, WIDTH, CELL_SIZE)]

def generate_food():
    while True:
        x = random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE
        y = random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
        if (x, y) not in snake and (x, y) not in walls:
            return (x, y)

food = generate_food()

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
    
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    if new_head in walls or new_head in snake:
        running = False
        continue
    
    snake.insert(0, new_head)
    
    if new_head == food:
        score += 1
        food = generate_food()
        
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()
    
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    
    for wall in walls:
        pygame.draw.rect(screen, WHITE, (wall[0], wall[1], CELL_SIZE, CELL_SIZE))
    
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
