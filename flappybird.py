import streamlit as st
import pygame
import time
import threading
from streamlit_webrtc import webrtc_streamer

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
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
screen = pygame.Surface((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)

def flappy_bird():
    global BIRD_Y
    clock = pygame.time.Clock()
    bird_velocity = 0
    pipes = [(WIDTH, HEIGHT // 2)]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)
        bird_velocity += GRAVITY
        BIRD_Y += bird_velocity

        # Draw Bird
        pygame.draw.circle(screen, BLUE, (BIRD_X, int(BIRD_Y)), 15)

        # Pipe Logic
        for i in range(len(pipes)):
            pipes[i] = (pipes[i][0] - PIPE_SPEED, pipes[i][1])
        if pipes[0][0] < -PIPE_WIDTH:
            pipes.pop(0)
            pipes.append((WIDTH, HEIGHT // 2))
            score += 1
        
        for pipe_x, pipe_y in pipes:
            pygame.draw.rect(screen, GREEN, (pipe_x, 0, PIPE_WIDTH, pipe_y - PIPE_GAP // 2))
            pygame.draw.rect(screen, GREEN, (pipe_x, pipe_y + PIPE_GAP // 2, PIPE_WIDTH, HEIGHT - pipe_y))
        
        # Collision Detection
        if BIRD_Y >= HEIGHT or BIRD_Y <= 0:
            running = False
        for pipe_x, pipe_y in pipes:
            if BIRD_X + 15 > pipe_x and BIRD_X - 15 < pipe_x + PIPE_WIDTH:
                if BIRD_Y - 15 < pipe_y - PIPE_GAP // 2 or BIRD_Y + 15 > pipe_y + PIPE_GAP // 2:
                    running = False

        # Score Display
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(30)

# Streamlit App
def main():
    st.title("Flappy Bird in Streamlit")
    st.write("Press 'Space' to jump!")
    
    if st.button("Start Game"):
        thread = threading.Thread(target=flappy_bird)
        thread.start()
        time.sleep(0.5)
        webrtc_streamer(key="game")

if __name__ == "__main__":
    main()
