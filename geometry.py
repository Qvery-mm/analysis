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
        self.minBorderDist = min(self.minBorderDist, distToZero(midpoint.x, midpoint.y))
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
            #print("No intersections")
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
        flag = False
        for i in shell1:
            #print("t", i)
            if i not in self.perpendicular:
                testSection = Segment2D(point, i)
                if testSection.intersection(self.perpendicular):
                    self.shell = shell1.copy()
                    self.sizeOfShell = len(shell1)
                    flag = True
        if not flag:
            self.shell = shell2.copy()
            self.sizeOfShell = len(shell2)
        ans = 0
        for i in self.shell:
            ans = max(ans, distToZero(i.x, i.y))
        self.maxBorderDist = ans

        #print(self.shell)

def distToZero(a, b):
    return (a*a + b*b)**(1/2)

def insertText(screen, x, n, AV):
    textsurface = myfont.render(' x = ' + str(x), False, (0, 0, 0))
    screen.blit(textsurface, (width, 50))

    textsurface = myfont.render(' h = ' + str(H) + '/' + str(n), False, (0, 0, 0))
    screen.blit(textsurface, (width, 150))


    textsurface = myfont.render(' A(V) = ' + str(format(AV, '.10g')), False, (0, 0, 0))
    screen.blit(textsurface, (width, 250))

import sys, pygame
pygame.init()

width, height = 1000, 1000
size = width + 300, height
black = 0, 0, 0
gray = 127, 127, 127
white = 255, 255, 255

screen = pygame.display.set_mode(size)




#x = 0.61803398875
#x = 3.1415926
#x = 1.4331274267223
x = 2**(1/2)
#x = 1/3
H, h = 1, 1
STEP = 500

cell = VoronovCell()
A = []
for i in range(-1000, 1000 + 1):
    for j in range(-1000, 1000 + 1):
        a, b = i + x * j, j
        r = distToZero(a, b)
        if abs(a) <= 2:
            A.append([r, a, b, 0])
A.sort()

for n in range(1, 50, 1):
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
        A[i][0] = distToZero(A[i][1], A[i][3])
    A.sort()

    for i in A:
        if(abs(i[1] * step) <= width / 2 and abs(i[3] * step) < height / 2):
            pygame.draw.circle(screen, black, (int(i[1] * step + width / 2), height - int(i[3] * step + height / 2)), 1)
        if i[0] <= 2 * cell.maxBorderDist:
            if(i[1] != 0 or i[3] != 0):
                point = Point2D(i[1], i[3])
                cell.updateCell(point)
        #else:
            #break




    AV = cell.maxBorderDist / cell.minBorderDist
    shape = cell.shell.copy()
    for i in range(len(shape)):
        shape[i] = (shape[i].x * step + 500, height - (shape[i].y * step + 500))
    pygame.draw.polygon(screen, black, shape, 1)

    pygame.draw.rect(screen, gray, ((width, 0),(width + 200, height)), 0)
    insertText(screen, x, n, AV)
    pygame.display.flip()
    #pygame.image.save(screen, "./sqrt(2)/screenshot" + str(n) + ".jpeg")


