# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
width=1000
height=750
linewidth=3
screen = pygame.display.set_mode([width, height])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (width // 2, height // 2), 75)

    w1 = width // 3
    w2 = 2 * width // 3
    h1 = height // 3
    h2 = 2 * height // 3

    pygame.draw.line(screen, (0, 0, 0), (w1, h1), (w2, h2), linewidth)
    pygame.draw.line(screen, (0, 0, 0), (w1, h2), (w2, h1), linewidth)
    pygame.draw.lines(screen, (0, 0, 0), True, [(w1, h1), (w1, h2), (w2, h2), (w2, h1)], linewidth)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
