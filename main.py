import sys, pygame
#from geometry import VoronovCell
import sympy
from sympy import Point2D, Line2D, Segment2D
pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0
white = 255, 255, 255

phi = 0.61803
x = phi
step = 500
h = 0.02

screen = pygame.display.set_mode(size)


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)
    pygame.draw.line(screen, black, (500, 0), (500, 1000), 1)
    pygame.draw.line(screen, black, (0, 500), (1000, 500), 1)
    #cell = VoronovCell()
    for i in range(-3, 3 + 1):
        for j in range(-3, 3 + 1):
            a, b = i + x * j, j * h
            # a, b = i, j
            pygame.draw.circle(screen, black, (int(a*step + 500), int(b * step + 500)), 1)
            # point = Point2D(a, b)
            # print("point", point)
            # cell.updateCell(point)
            # shape = cell.shell.copy()
            # for k in range(len(shape)):
            #     shape[k] = (shape[k].x * step + 500, shape[k].y * step + 500)
            # pygame.draw.polygon(screen, black, shape, 1)


    pygame.display.flip()
    h = h / 1.1
    print(h)
    pygame.time.delay(100)
    if h < 0.01:
        pygame.QUIT: sys.exit()

