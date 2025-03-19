import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X = 50
GRAVITY = 0.5
JUMP_STRENGTH = -8
PIPE_WIDTH = 70
PIPE_GAP = 180
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def main():
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = [(WIDTH, random.randint(150, 450))]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = JUMP_STRENGTH

        # Apply gravity
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Draw Bird
        pygame.draw.circle(screen, BLUE, (BIRD_X, int(bird_y)), 15)

        # Pipe Logic
        for i in range(len(pipes)):
            pipes[i] = (pipes[i][0] - PIPE_SPEED, pipes[i][1])
        if pipes[0][0] < -PIPE_WIDTH:
            pipes.pop(0)
            pipes.append((WIDTH, random.randint(150, 450)))
            score += 1

        for pipe_x, pipe_y in pipes:
            pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_y - PIPE_GAP // 2))
            pygame.draw.rect(screen, GREEN, (pipe_x, pipe_y + PIPE_GAP // 2, PIPE_WIDTH, HEIGHT - pipe_y))

        # Collision Detection
        if bird_y >= HEIGHT or bird_y <= 0:
            running = False
        for pipe_x, pipe_y in pipes:
            if BIRD_X + 15 > pipe_x and BIRD_X - 15 < pipe_x + PIPE_WIDTH:
                if bird_y - 15 < pipe_y - PIPE_GAP // 2 or bird_y + 15 > pipe_y + PIPE_GAP // 2:
                    running = False

        # Score Display
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
