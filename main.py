import sys
import pygame
import geometry
import sympy
from math import log, sin
import datetime


def insertText(screen, font, x, n, AV):
    textsurface = font.render(' x = ' + str(x), False, (0, 0, 0))
    screen.blit(textsurface, (width, 50))

    textsurface = font.render(' h = ' + str(H) + '/' + str(n), False, (0, 0, 0))
    screen.blit(textsurface, (width, 150))


    textsurface = font.render(' A(V) = ' + str(format(AV, '.10g')), False, (0, 0, 0))
    screen.blit(textsurface, (width, 250))



#globals
width, height = 1000, 1000
size = width + 300, height
black = 0, 0, 0
gray = 127, 127, 127
white = 255, 255, 255



#x = pi #main number

H, h = 1, 1
N = 1000
STEP = 500


def processNumber(x, name):
    sys.stdout = open("./19jul/" + name + "/"+ name + " A(n).txt", "w")
    A = []
    for i in range(-4000, 4000 + 1):
        for j in range(-4000, 4000 + 1):
            a, b = i + x * j, j
            r = geometry.distToZero(a, b)
            if abs(a) <= 2:
                A.append([r, a, b, 0])
    A.sort()
    for t in range(1, N + 1, 1):
        n = t * t
        cell = geometry.VoronovCell()
        step = STEP * (n**(1/2)) / 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(white)
        pygame.draw.line(screen, black, (500, 0), (500, 1000), 1)
        pygame.draw.line(screen, black, (0, 500), (1000, 500), 1)
        pygame.font.init()
        myfont = pygame.font.SysFont('Arial', 30)

        h = H / n

        for i in A:
            if abs(i[1])*step > width / 2:
                A.remove(i)

        for i in range(len(A)):
            #print(A[i])
            A[i][3] = A[i][2] * h
            A[i][0] = geometry.distToZero(A[i][1], A[i][3])
        A.sort()

        for i in A:
            if(abs(i[1] * step) <= width / 2 and abs(i[3] * step) < height / 2):
                pygame.draw.circle(screen, black, (int(i[1] * step + width / 2), height - int(i[3] * step + height / 2)), 1)
            if i[0] <= 2 * cell.maxBorderDist:
                if(i[1] != 0 or i[3] != 0):
                    point = sympy.Point2D(i[1], i[3])
                    cell.updateCell(point)
            if i[0] > sqrt2 * width:
                break




        AV = cell.maxBorderDist / cell.minBorderDist
        shape = cell.shell.copy()
        for i in range(len(shape)):
            shape[i] = (shape[i].x * step + 500, height - (shape[i].y * step + 500))
        pygame.draw.polygon(screen, black, shape, 1)

        pygame.draw.rect(screen, gray, ((width, 0),(width + 200, height)), 0)
        insertText(screen, myfont, x, n, AV)
         pygame.display.flip()
        print(n, AV)
        pygame.image.save(screen, "./19jul/" + name + "/screenshot" + str(n) + ".jpeg")
    sys.stdout.close()


garmonic = 1.4331274267223 #[1; 2, 3, 4, 5, 6, 7, ...]
rationale = 1/3
cubic2 = 2 ** (1/3)
cubic3 = 3 ** (1/3)
e = 2.71828182846
phi = 0.61803398875 #golden ratio
pi = 3.14159265358979323
sqrt2 = 2**(1/2)
sqrt3 = 3 ** (1/2)
sqrt5 = 5 ** (1/2)
ln_pi = log(pi)
sin1 = sin(1)


pygame.init()
screen = pygame.display.set_mode(size)
print("start")

# processNumber(garmonic, "[1; 2, 3, 4, ...]")
# #processNumber(rationale, "0.(3)")
# processNumber(cubic2, "cubic root(2)")
# processNumber(cubic3, "cubic root(3)")
# processNumber(e, "e")
# processNumber(phi, "phi")

# processNumber(pi, "pi")
# processNumber(sqrt2, "sqrt(2)")
# processNumber(sqrt3, "sqrt(3)")
# processNumber(sqrt5, "sqrt(5)")
# processNumber(ln_pi, "ln(pi)")
processNumber(sin1, "sin(1)")


