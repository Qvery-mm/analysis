import sympy
from sympy import Point2D, Line2D, Segment2D

class VoronovCell:
    def __init__(self):
        self.shell = [Point2D(-1, 1), Point2D(1, 1), Point2D(1, -1), Point2D(-1, -1)]
        self.sizeOfShell = 4
        self.maxBorderDist = 2**(1/2)
        self.minBorderDist = 1

    def updateCell(self, point):
        center = Point2D(0, 0)
        line = Line2D(center, point)
        midpoint = Point2D(point.x / 2, point.y / 2)
        perpendicular = line.perpendicular_line(midpoint)

        intersections = []

        for i in range(self.sizeOfShell - 1):
            section = Segment2D(self.shell[i], self.shell[i+1])
            if perpendicular.intersection(section):
                intersections.append((i, perpendicular.intersection(section)))

        section = Segment2D(self.shell[0], self.shell[self.sizeOfShell - 1])
        if perpendicular.intersection(section):
            intersections.append((self.sizeOfShell - 1, perpendicular.intersection(section)))
        print(intersections)

        for i in intersections: #если перпендикуляр пересекается с границей ячейки по отрезку
            if (str(type(i[1][0])) == "<class 'sympy.geometry.line.Segment2D'>"):
                return


        if intersections: #если серединный перпендикуляр пересекает ранее построенную ячейку:
            nextPoint = self.shell[intersections[0][0]+1]
            testSegment = Segment2D(point, nextPoint)
            newShell = []
            if perpendicular.intersection(testSegment): #если новая точка и узел ячейки лежат по разные стороны от перпендикуляра:
                print("???")
                pygame.draw.circle(screen, black, (point.x * 200 + 500, point.y * 200 + 500), 5, 1)
                newShell.append(intersections[0][1][0])
                for i in range(intersections[0][0]+1, intersections[1][0] + 1):
                    if(self.shell[i] != intersections[0][1][0] and self.shell[i] != intersections[1][1][0]):
                        newShell.append(self.shell[i])
                newShell.append(intersections[1][1][0])
            # если новая точка и узел ячейки лежат по одну сторону от перпендикуляра:
            else:
                print("!!!")

                pygame.draw.circle(screen, black, (point.x * 200 + 500, point.y*200 + 500), 5, 1)
                newShell = []
                for i in range(intersections[0][0]+1):
                    if (self.shell[i] != intersections[0][1][0] and self.shell[i] != intersections[1][1][0]):
                        newShell.append(self.shell[i])
                newShell.append(intersections[0][1][0])
                newShell.append(intersections[1][1][0])
                for i in range(intersections[1][0]+1, self.sizeOfShell):
                    if (self.shell[i] != intersections[0][1][0] and self.shell[i] != intersections[1][1][0]):
                        newShell.append(self.shell[i])
            self.shell = newShell



import sys, pygame
pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)


screen.fill(white)
pygame.draw.line(screen, black, (500, 0), (500, 1000), 1)
pygame.draw.line(screen, black, (0, 500), (1000, 500), 1)

cell = VoronovCell()
point1 = Point2D(-1, 1)
point2 = Point2D(1, 1)
point3 = Point2D(0, -2)

cell.updateCell(point1)
cell.updateCell(point2)
cell.updateCell(point3)

shape = cell.shell.copy()
for i in range(len(shape)):
    shape[i] = (shape[i].x * 200 + 500, shape[i].y * 200 + 500)

pygame.draw.polygon(screen, black, shape, 1)
pygame.display.flip()
pygame.time.delay(50000)

