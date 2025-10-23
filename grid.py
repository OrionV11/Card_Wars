import pygame

HEIGHT = 100
WIDTH = 100

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255, 0, 0)

MARGIN = 5

#Create Grid
grid = []

for row in range(4):
    grid.append([])

    for column in range(4):
        grid[row].append(0)

#grid = [[10 for x in range(10) for col]]

#set row 1, cell 5 to one

#Active Board Cells: Cards can be placed here
'''
for row in range(1,4):
    for col in range(1,4):
        grid[row][col] = 1 '''

pygame.init()

WINDOW_SIZE = [450, 450]
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Array Backed Grid")
pygame.time.Clock()

clock = pygame.time.Clock()

done = False

key_map = {
    pygame.K_1: (0, 3),
    pygame.K_2: (1, 3),
    pygame.K_3: (2, 3),
    pygame.K_4: (3, 3)
}

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

        elif event.type == pygame.KEYDOWN:
            if event.key in key_map:
                column, row = key_map[event.key]
                grid[row][column] = 3
        
    screen.fill(BLACK)

    for row in range(4):
        for column in range(4):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            if grid[row][column] == 3:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN, 
                             WIDTH,
                             HEIGHT])
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
