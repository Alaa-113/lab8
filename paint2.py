import pygame

def drawing_app(screen, clock):
    # Initialize brush settings and drawing mode
    brush_size = 5
    mode = "pencil"
    color = (0, 0, 255)  # Default color: blue
    
    # Define available colors
    colors = {
        "blue": (0, 0, 255),
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "white": (255, 255, 255),
        "black": (0, 0, 0)
    }
    
    # Create a canvas surface
    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))  # Black background
    
    drawing = False
    start_pos = None

    while True:
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(canvas, (0, 0))  # Draw canvas on screen
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                # Handle key inputs for mode and color changes
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                elif event.key == pygame.K_TAB:
                    return "switch"
                elif event.key == pygame.K_r:
                    mode = "rectangle"
                elif event.key == pygame.K_t:
                    color = colors["red"]
                elif event.key == pygame.K_g:
                    color = colors["green"]
                elif event.key == pygame.K_b:
                    color = colors["blue"]
                elif event.key == pygame.K_1:
                    color = colors["yellow"]
                elif event.key == pygame.K_2:
                    color = colors["orange"]
                elif event.key == pygame.K_p:
                    mode = "pencil"
                elif event.key == pygame.K_c:
                    mode = "circle"
                elif event.key == pygame.K_e:
                    mode = "eraser"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    drawing = True
                    start_pos = event.pos  # Store starting position
                    # Draw initial point for pencil and eraser modes
                    if mode == "pencil" or mode == "eraser":
                        pygame.draw.circle(canvas, color if mode == "pencil" else colors["black"], event.pos, brush_size)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos
                    if mode == "rectangle":
                        # Draw a rectangle from start to end position
                        rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        pygame.draw.rect(canvas, color, rect, 2)
                    elif mode == "circle":
                        # Draw a circle based on the distance from start to end position
                        radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, radius, 2)
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == "pencil" or mode == "eraser":
                    pygame.draw.circle(canvas, color if mode == "pencil" else colors["black"], event.pos, brush_size)
        
        pygame.display.flip()
        clock.tick(60)

def line_drawing_app(screen, clock):
    radius = 15  # Initial line width
    mode = 'blue'  # Default color mode
    points = []  # List of drawn points
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                # color mode changes
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_TAB:
                    return "switch"
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    radius = min(200, radius + 1)  # Increase radius
                elif event.button == 3:
                    radius = max(1, radius - 1)  # Decrease radius
            
            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                points.append(position)
                points = points[-256:]  # Keep last 256 points only
        
        screen.fill((0, 0, 0))
        for i in range(len(points) - 1):
            draw_line_between(screen, i, points[i], points[i + 1], radius, mode)
        
        pygame.display.flip()
        clock.tick(60)

def draw_line_between(screen, index, start, end, width, color_mode):
    #  gradient color based on index
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    color = (c1, c1, c2) if color_mode == 'blue' else (c2, c1, c1) if color_mode == 'red' else (c1, c2, c1)
    
    # Draw smooth line between two points
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))  # Determine the number of steps for smooth interpolation
    for i in range(iterations):
        progress = i / iterations  # Compute progress ratio
        aprogress = 1 - progress  # Compute inverse progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)  # Draw small circles to create a smooth line

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    mode = "drawing"
    
    while True:
        if mode == "drawing":
            result = drawing_app(screen, clock)
        else:
            result = line_drawing_app(screen, clock)
        
        if result == "quit":
            break
        elif result == "switch":
            mode = "lines" if mode == "drawing" else "drawing"

main()
