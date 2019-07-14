import sys, pygame
pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0
white = 255, 255, 255

phi = 0.61803
x = phi
step = 500
h = 1

screen = pygame.display.set_mode(size)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)
    pygame.draw.line(screen, black, (500, 0), (500, 1000), 1)
    pygame.draw.line(screen, black, (0, 500), (1000, 500), 1)
    for i in range(-100, 100 + 1):
        for j in range(-100, 100 + 1):
            a, b = i + x * j, j * h
            pygame.draw.circle(screen, black, (int(a*step + 500), int(b * step + 500)), 1)
    pygame.display.flip()
    h = h / 1.1
    print(h)
    pygame.time.delay(100)
    if h < 0.01:
        pygame.QUIT: sys.exit()

