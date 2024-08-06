import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_SPEED = 4
BIRD_START_X = 50
BIRD_START_Y = SCREEN_HEIGHT // 2
BIRD_SIZE = 34

# Load bird image
BIRD_IMAGE = pygame.transform.scale(pygame.image.load('bird.png'), (BIRD_SIZE, BIRD_SIZE))

# Load font
FONT = pygame.font.SysFont('Arial', 32)

# Function to create pipes
def create_pipe():
    pipe_y = random.randint(200, SCREEN_HEIGHT - 200)
    pipe = {
        'x': SCREEN_WIDTH,
        'y': pipe_y,
        'rect_up': pygame.Rect(SCREEN_WIDTH, pipe_y - PIPE_GAP - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT),
        'rect_down': pygame.Rect(SCREEN_WIDTH, pipe_y + PIPE_GAP, PIPE_WIDTH, PIPE_HEIGHT),
        'passed': False
    }
    return pipe

# Function to draw pipes
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(SCREEN, BLACK, pipe['rect_up'])
        pygame.draw.rect(SCREEN, BLACK, pipe['rect_down'])

# Function to draw score
def draw_score(score):
    score_surface = FONT.render(f'Score: {score}', True, BLACK)
    SCREEN.blit(score_surface, (10, 10))

# Main game function
def main():
    clock = pygame.time.Clock()
    bird_y = BIRD_START_Y
    bird_speed = 0
    pipes = []
    score = 0

    # Game loop
    running = True
    while running:
        SCREEN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = BIRD_JUMP

        # Bird physics
        bird_speed += GRAVITY
        bird_y += bird_speed
        bird_rect = pygame.Rect(BIRD_START_X, bird_y, BIRD_SIZE, BIRD_SIZE)

        # Pipe movement
        for pipe in pipes:
            pipe['x'] -= PIPE_SPEED
            pipe['rect_up'].x = pipe['x']
            pipe['rect_down'].x = pipe['x']

            # Check if bird passed the pipe
            if pipe['x'] + PIPE_WIDTH < BIRD_START_X and not pipe['passed']:
                pipe['passed'] = True
                score += 1

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['x'] > -PIPE_WIDTH]

        # Add new pipes
        if len(pipes) == 0 or pipes[-1]['x'] < SCREEN_WIDTH - 200:
            pipes.append(create_pipe())

        # Draw pipes
        draw_pipes(pipes)

        # Check for collisions
        for pipe in pipes:
            if bird_rect.colliderect(pipe['rect_up']) or bird_rect.colliderect(pipe['rect_down']):
                running = False

        # Check for out of bounds
        if bird_y > SCREEN_HEIGHT or bird_y < 0:
            running = False

        # Draw bird
        SCREEN.blit(BIRD_IMAGE, (BIRD_START_X, bird_y))

        # Draw score
        draw_score(score)

        # Update display
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()