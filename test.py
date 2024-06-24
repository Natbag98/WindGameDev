import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Tracker")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Get the position of the mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw a circle at the mouse position
    radius = 20
    pygame.draw.circle(screen, RED, (mouse_x, mouse_y), radius)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()