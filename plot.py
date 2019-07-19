import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
from time import sleep



def make_plot(name):
    sys.stdin = open("./18jul/" + name + "/" + name +  " A(n).txt", "r")
    x = []
    y = []
    for i in range(200):
        s = input()
        s = s.split()
        x.append(int(s[0]))
        y.append(float(s[1]))
    # Data for plotting


    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='n', ylabel='A(n)',
           title='x = ' + name  + ';  t = 1/n')
    ax.grid()

    fig.savefig("./18jul/" + name + "/plot.png")
    #plt.show()
    #sleep(2)
    sys.stdin.close()

make_plot("0.(3)")
make_plot("[1; 2, 3, 4, ...]")
make_plot("cubic root(2)")
make_plot("e")
make_plot("phi")
make_plot("phi^-1")
make_plot("pi")
make_plot("sqrt(2)")
make_plot("sqrt(3)")
make_plot("sqrt(5)")