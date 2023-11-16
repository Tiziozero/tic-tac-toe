import pygame
import sys

def draw_grid(surface):
    # Define grid parameters
    grid_size = 3
    cell_size = 100  # Adjusted to fit within a 300x300 square
    cell_spacing = 1

    # Calculate total grid size
    total_size = grid_size * cell_size + (grid_size - 1) * cell_spacing

    # Calculate the starting position for the grid to be centered
    start_x = (surface.get_width() - total_size) // 2
    start_y = (surface.get_height() - total_size) // 2

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            cell_x = start_x + col * (cell_size + cell_spacing)
            cell_y = start_y + row * (cell_size + cell_spacing)
            pygame.draw.rect(surface, (0, 0, 0), (cell_x, cell_y, cell_size, cell_size))

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (800, 450)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Centered Grid Example")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the background with white
    window.fill((255, 255, 255))

    # Draw the centered grid
    draw_grid(window)

    # Update the display
    pygame.display.flip()

