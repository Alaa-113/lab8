import pygame
import random #to add randomly appearing food on the screen

pygame.init()#initialozong pygame
#constant sof the game
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 10#size of each snake segment and food
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))#building th escreen
clock = pygame.time.Clock()#clock to control speed

snake = [(100, 100), (90, 100), (80, 100)]#list of tuples representing the segments of the body
snake_dir = (CELL_SIZE, 0)#initial movement direction
score = 0 #score counter
level = 1 #level counter
speed = 10 #initial speed

#borders of th screen(left,right,top. bottom)
walls = [(0, i) for i in range(0, HEIGHT, CELL_SIZE)] + [(WIDTH - CELL_SIZE, i) for i in range(0, HEIGHT, CELL_SIZE)] + \
        [(i, 0) for i in range(0, WIDTH, CELL_SIZE)] + [(i, HEIGHT - CELL_SIZE) for i in range(0, WIDTH, CELL_SIZE)]

def generate_food():
    while True:
        x = random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE
        y = random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
        if (x, y) not in snake and (x, y) not in walls:#to avoid the snake and the walls
            return (x, y)

food = generate_food()# Initialize food position

running = True#game loop
while running:
    screen.fill(BLACK) #clearing the screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False#exiting the game
        elif event.type == pygame.KEYDOWN: #detecting key movements
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
    
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])# adding a head and moving the body
    # Check for collisions with walls or itself
    if new_head in walls or new_head in snake:
        running = False
        continue
    # Add new head position
    snake.insert(0, new_head)
    
      # Check if food is eaten
    if new_head == food:
        score += 1  # Increase score
        food = generate_food()  # Generate new food position
        
        # Increase level and speed every 3 points
        if score % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  # Remove tail segment if no food eaten
    
    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Draw the food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    
    # Draw the walls
    for wall in walls:
        pygame.draw.rect(screen, WHITE, (wall[0], wall[1], CELL_SIZE, CELL_SIZE))
    
    # Display score and level
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    
    pygame.display.flip()  # Update the screen
    clock.tick(speed)  # Control game speed

pygame.quit()  # Quit pygame after the game loop ends
