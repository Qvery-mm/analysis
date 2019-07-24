import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
from time import sleep



def make_plot(name):
    day = "23jul"
    sys.stdin = open("./%s/%s/%s A(n).txt" % (day, name, name), "r")
    x = []
    y = []
    for i in range(1000):
        s = input()
        s = s.split()
        x.append(int(s[0]))
        y.append(float(s[1]))
    # Data for plotting


    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='n', ylabel='A(n)',
           title='x = ' + name  + ';  t = 1/n^2')
    ax.grid()

    fig.savefig("./%s/%s/plot.png" % (day, name))
    #plt.show()
    #sleep(2)
    sys.stdin.close()

make_plot("p1")
make_plot("p2")
make_plot("p3")
make_plot("p4")
make_plot("p5")

make_plot("p7")
make_plot("p8")
make_plot("p9")
make_plot("p10")



