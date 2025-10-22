import pygame

HEIGHT = 1000
WIDTH = 800

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255, 0, 0)

MARGIN = 5

#Create Grid
grid = []

for row in range(10):
    grid.append([])

    for column in range(10):
        grid[row].append(0)

#grid = [[10 for x in range(10) for col]]

#set row 1, cell 5 to one
grid[1][5] = 1

pygame.init()

WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.set.display.set_caption("Array Backed Grid")
pygame.time.Clock()

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    screen.fill(BLACK)

    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN, 
                             WIDTH,
                             HEIGHT])
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
