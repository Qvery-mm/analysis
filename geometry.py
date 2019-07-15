import sympy
from sympy import Point2D, Line2D, Segment2D

class VoronovCell:
    def __init__(self):
        self.shell = [Point2D(-1, 1), Point2D(1, 1), Point2D(1, -1), Point2D(-1, -1)]
        self.sizeOfShell = 4
        self.maxBorderDist = 2**(1/2)
        self.minBorderDist = 1


    def __getIntersections(self, point):
        center = Point2D(0, 0)
        line = Line2D(center, point)
        midpoint = Point2D(point.x / 2, point.y / 2)
        self.perpendicular = line.perpendicular_line(midpoint)

        sectionIntersections = []
        vertexIntersections = []
        for i in range(self.sizeOfShell - 1):
            section = Segment2D(self.shell[i], self.shell[i+1])
            intersection = self.perpendicular.intersection(section)
            if intersection:
                sectionIntersections.append((i, self.perpendicular.intersection(section))) #add number of previous vertex and intersection point
                if self.shell[i] in self.perpendicular:
                    vertexIntersections.append(i)

        section = Segment2D(self.shell[0], self.shell[self.sizeOfShell-1])
        intersection = self.perpendicular.intersection(section)
        if intersection:
            sectionIntersections.append((self.sizeOfShell-1, self.perpendicular.intersection(section)))  # add number of previous vertex and intersection point
        if self.shell[self.sizeOfShell - 1] in self.perpendicular:
            vertexIntersections.append(self.sizeOfShell - 1)
        #print(sectionIntersections)
        #print(vertexIntersections)
        self.__sections = sectionIntersections
        self.__vertex = vertexIntersections


    def updateCell(self, point):
        self.__getIntersections(point)
        if not self.__sections:
            print("No intersections")
            return

        for i in self.__sections:
            if str(type(i[1][0])) == "<class 'sympy.geometry.line.Segment2D'>":
                print("Segment intersection")
                return

        shell1 = []
        shell2 = []
        # найдено 2 вершины
        if len(self.__vertex) == 2:
            for i in range(self.__vertex[0], self.__vertex[1] + 1):
                shell1.append(self.shell[i])

            for i in range(self.__vertex[1], self.sizeOfShell):
                shell2.append(self.shell[i])
            for i in range(0, self.__vertex[0] + 1):
                shell2.append(self.shell[i])


        #найдена 1 вершина
        if len(self.__vertex) == 1:
            vertex = self.__vertex[0]
            section = -1
            for i in self.__sections:
                if self.shell[vertex] != i[1][0]:
                    section = i
            if section == -1:
                return
            print("debug", vertex)
            print("debug", section)

            if vertex < section[0]:
                for i in range(vertex, section[0]+1):
                    shell1.append(self.shell[i])
                shell1.append(section[1][0])

                shell2.append(section[1][0])
                for i in range(section[0]+1, self.sizeOfShell):
                    shell2.append(self.shell[i])
                for i in range(vertex + 1):
                    shell2.append(self.shell[i])
            else:
                shell1.append(section[1][0])
                for i in range(section[0] + 1, vertex + 1):
                    shell1.append(self.shell[i])


                for i in range(vertex, self.sizeOfShell):
                    shell2.append(self.shell[i])
                for i in range(section[0] + 1):
                    shell2.append(self.shell[i])
                shell2.append(section[1][0])

            print("debug", shell1)
            print("debug", shell2)


        #найдено 0 вершин
        if len(self.__vertex) == 0:
            firstV, lastV = self.__sections[0][0], self.__sections[1][0]
            firstP, lastP = self.__sections[0][1][0], self.__sections[1][1][0]
            shell1.append(firstP)

            for i in range(firstV+1, lastV + 1):
                shell1.append(self.shell[i])
            shell1.append(lastP)

            shell2.append(lastP)
            for i in range(lastV + 1, self.sizeOfShell):
                shell2.append(self.shell[i])
            for i in range(firstV + 1):
                shell2.append(self.shell[i])
            shell2.append(firstP)

        # print(shell1)
        # print(shell2)
        #выбираем нужную оболочку
        for i in shell1:
            #print("t", i)
            if i not in self.perpendicular:
                testSection = Segment2D(point, i)
                if testSection.intersection(self.perpendicular):
                    self.shell = shell1.copy()
                    self.sizeOfShell = len(shell1)
                    return
        self.shell = shell2.copy()
        self.sizeOfShell = len(shell2)

        #print(self.shell)


import sys, pygame
pygame.init()

size = width, height = 1000, 1000
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)


screen.fill(white)
pygame.draw.line(screen, black, (500, 0), (500, 1000), 1)
pygame.draw.line(screen, black, (0, 500), (1000, 500), 1)

x = 0.618
h = 0.2
cell = VoronovCell()
for i in range(-5, 5 + 1):
    for j in range(-5, 5 + 1):
        if(i != 0 and  j != 0):
            point = Point2D(i *x*j, j*h)
            cell.updateCell(point)


shape = cell.shell.copy()
for i in range(len(shape)):
    shape[i] = (shape[i].x * 200 + 500, shape[i].y * 200 + 500)

pygame.draw.polygon(screen, black, shape, 1)
pygame.display.flip()
pygame.time.delay(50000)

