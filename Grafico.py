

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sys import argv
import time


import sys
import os
from tkinter import *
import tkinter
from tkinter import messagebox
import tkinter as tk
import re
from os.path import exists



colour = 'green3'

top = tkinter.Tk()
top.title("Deviation graph in Z (© F.Steven)")
top.geometry('550x150')
top.configure(bg= colour)


def reverse_colourmap(cmap, name = 'my_cmap_r'):
    """
    In:
    cmap, name
    Out:
    my_cmap_r

    Explanation:
    t[0] goes from 0 to 1
    row i:   x  y0  y1 -> t[0] t[1] t[2]
                   /
                  /
    row i+1: x  y0  y1 -> t[n] t[1] t[2]

    so the inverse should do the same:
    row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                   /
                  /
    row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
    """
    reverse = []
    k = []

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))

    LinearL = dict(zip(k,reverse))
    my_cmap_r = cm.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r



def grafico():
     cmap = cm.jet
     cmap_r = reverse_colourmap(cmap)

     filename = E1.get()
     if (exists(filename)):

          L3 = Label(top, text = "                                 ")
          L3.configure(bg = colour)
          L3.pack(padx = 5, pady = 5)
          L3.place(x = 190, y = 90)
          # print "no file input"
          x =[]
          y =[]
          z =[]
          count = 0
          lines = open(filename, "r").readlines()

          size = len(lines)
          for line in lines:
               if count > 175 and count < (size-1):
                    quota_x = float(line[10:19])
                    quota_y = float(line[21:31])
                    quota_z = float(line[109:118])
                    x.append(quota_x)
                    y.append(quota_y)
                    z.append(quota_z)

               count = count +1

          fig = plt.figure()
          ax = Axes3D(fig)
          surf = ax.plot_trisurf(x, y, z, cmap= cmap_r, linewidth=0.1)        # cm.hsv  vmin=-0.1, vmax=0.1
          fig.colorbar(surf, shrink=0.5, aspect=5)
          plt.savefig('teste.pdf')
          plt.show()
     else:
          L3 = Label(top, text = "File non esiste", fg = "red")
          L3.pack(padx = 50, pady = 5)
          L3.place(x = 190, y = 90)


#label
L1 = Label(top, text="Inserire nome file di input:")
L1.pack( padx = 50, pady = 5)
L1.configure(bg= colour)
L1.place ( x = 10, y = 5)
#entry
E1 = Entry(top, bd =4)
E1.insert(0, r"C:\Users\sat11\Documents\GitHub\Parpas_DR\Dronex_VXX\backend_app\output\speed14_3feb\output_complex_speed14_f2k_4000x3200_1.tab")
E1.pack(padx = 50, pady = 5)
E1.place(x = 10, y = 35,width=530)

#bottone
b = tkinter.Button(top, text= "Visualizza\n grafico",bd =4 , command = grafico)
b.pack(padx = 50, pady = 20)
b.place(x = 15, y = 80)


def quit():
    top.destroy()
    sys.exit()

#quit
top.protocol('WM_DELETE_WINDOW', quit)


#loop
top.mainloop()
