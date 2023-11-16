
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

from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from scipy.interpolate import griddata




colour = 'green3'

top = tkinter.Tk()
top.title("Deviation graph (© F.Steven)")
top.geometry('550x150')
top.configure(bg= colour)



def reverse_colourmap(cmap, name = 'my_cmap_r'):
    reverse = []
    k = []

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append(( 1 -t[0] ,t[2] ,t[1]))
        reverse.append(sorted(data))

    LinearL = dict(zip(k ,reverse))
    my_cmap_r = cm.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r



def grafico():
    cmap = cm.jet
    cmap_r = reverse_colourmap(cmap)
    scelta = var.get()

    filename = E1.get()
    if (exists(filename)):

        L3 = Label(top, text = "                                 ")
        L3.configure(bg = colour)
        L3.pack(padx = 5, pady = 5)
        L3.place(x = 190, y = 90)
        # print "no file input"
        x =[]
        y = []
        z = []

        count = 0
        lines = open(filename, "r").readlines()
        size = len(lines)

        lenght_x = lines[172].split()[1].strip()
        step_x = lines[173].split()[1].strip()
        result = int((float(lenght_x) / float(step_x)) + 1)

        for line in lines:
            if count > 175 and count < (size - 1):
                quota_x = float(line[10:19])
                quota_y = float(line[21:31])
                if scelta == 1:
                    errx = float(line[74:84])  # err x  87:97   # angolo 74:84
                elif scelta == 2:
                    errx = float(line[61:71])

                if checkbox_var.get() and errx < 0:
                    errx = -errx

                errx = -errx

                x.append(quota_x)
                y.append(quota_y)
                z.append(round(errx, 6))

            count = count + 1

        def manipola_lista(lista):
            # Dividi la lista in intervalli di dimensione 17
            intervalli = [lista[i:i + result] for i in range(0, len(lista), result)]

            # Manipola gli intervalli dispari
            for i, intervallo in enumerate(intervalli):
                if i % 2 != 0:  # Verifica se l'indice dell'intervallo è dispari
                    intervalli[i] = intervallo[::-1]  # Inverti l'ordine degli elementi

            # Concatena gli intervalli per ottenere la lista finale
            lista_finale = [numero for intervallo in intervalli for numero in intervallo]

            return lista_finale

        def divide_lista(lista):
            # Dividi la lista per 17
            intervalli = [lista[i:i + result] for i in range(0, len(lista), result)]

            # Inverti gli intervalli dispari
            for i in range(1, len(intervalli), 2):
                intervalli[i] = intervalli[i][::-1]

            return intervalli

        def somma_intervalli(intervalli):
            # Calcola la somma degli intervalli
            risultato = []
            for intervallo in intervalli:
                nuova_lista = [intervallo[0]]
                for i in range(1, len(intervallo)):
                    nuova_lista.append(round((nuova_lista[-1] + intervallo[i]), 6))
                risultato.extend(nuova_lista)

            return risultato

        def attenua_variazione(lista_numeri, fattore_attenuazione):
            lista_attenuata = [lista_numeri[0]]

            for i in range(1, len(lista_numeri)):
                valore_attuale = lista_attenuata[-1]
                valore_successivo = lista_numeri[i]

                # Calcola il nuovo valore attenuato
                nuovo_valore = valore_attuale + fattore_attenuazione * (valore_successivo - valore_attuale)

                lista_attenuata.append(nuovo_valore)

            return lista_attenuata

        if checkbox_var.get():
            fattore_attenuazione = 0.5  # 0.3
            z = attenua_variazione(z, fattore_attenuazione)
        else:
            fattore_attenuazione = 0.5  # 0.3
            z = attenua_variazione(z, fattore_attenuazione)

        # Esempio di utilizzo
        x = manipola_lista(x)
        intervalli_divisi = divide_lista(z)

        #######################

        lista_singola = []
        for lista in intervalli_divisi:
            lista_singola.extend(lista)

        z = lista_singola  ######################   somma_intervalli(intervalli_divisi)

        ##  z = somma_intervalli(intervalli_divisi)

        print(z)

        # Creazione di una griglia 2D per l'interpolazione
        grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

        # Interpolazione dei dati
        grid_angle = griddata((x, y), z, (grid_x, grid_y), method = 'cubic')  # cubic, linear or nearest

        # Creazione del grafico 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = '3d')

        # Disegno della superficie interpolata
        surf = ax.plot_surface(grid_x, grid_y, grid_angle, cmap = cmap_r, edgecolor = 'k')
        fig.colorbar(surf, shrink = 0.5, aspect = 5)
        # Aggiunta di etichette
        ax.set_xlabel('Asse X (mm)')
        ax.set_ylabel('Asse Y (mm)')
        ax.set_zlabel('error (°)')  # Millesimi di grado
        if not checkbox_var.get():
            ax.set_zlim(-0.006, 0.006)
        # Mostra il grafico
        plt.show()

    else:
        L3 = Label(top, text = "File non esiste", fg = "red")
        L3.pack(padx = 50, pady = 5)
        L3.place(x = 190, y = 90)


# scelta percorso da interfaccia
def select_file():
    filetypes = (('text files', '*.tab'), ('All files', '*.*'))
    filename2 = fd.askopenfilename(title = 'Open a file',
                                   initialdir = r'C:\Users\sat11\Documents\GitHub\Parpas_DR\DroneXPairingSoftware - Sorgente\backend_app\src\states\output',
                                   filetypes = filetypes)
    E1.delete(0, "end")
    E1.insert(0, filename2)


var = tk.IntVar()
radio_a = tk.Radiobutton(top, text = "Variation in X", variable = var, value = 1)
radio_b = tk.Radiobutton(top, text = "Variation in Y  ", variable = var, value = 2)
var.set(1)

checkbox_var = tk.BooleanVar()
checkbox = tk.Checkbutton(top, text = "View type 2", variable = checkbox_var)
# label
L1 = Label(top, text = "Enter file path of input:")
L1.pack(padx = 50, pady = 5)
L1.configure(bg = colour)
L1.place(x = 10, y = 5)
# entry
E1 = Entry(top, bd = 4)
E1.insert(0,
          r"C:\Users\sat11\Desktop\Dronex\SCANSIONI_MACCHINA_INCLINOMETRO\XXXXXXXXX____SCANSIONI_DroneX\XS167_scan\20231115_105316_XS167_XY_10000.0.tab")
E1.pack(padx = 50, pady = 5)
E1.place(x = 10, y = 35, width = 530)

# bottone
b = tkinter.Button(top, text = "View  \n graph  ", bd = 4, command = grafico)
b.pack(padx = 50, pady = 20)
b.place(x = 15, y = 80)

b2 = tkinter.Button(top, text = "Choose path from PC", bd = 4, command = select_file)
b2.pack(padx = 50, pady = 20)
b2.place(x = 400, y = 80)

radio_a.pack(padx = 50, pady = 5)
radio_a.configure(bg = colour)
radio_a.place(x = 90, y = 80)
radio_b.pack(padx = 50, pady = 5)
radio_b.configure(bg = colour)
radio_b.place(x = 90, y = 101)

checkbox.pack()
checkbox.configure(bg = colour)
checkbox.place(x = 90, y = 121)


def quit():
    top.destroy()
    sys.exit()


# quit
top.protocol('WM_DELETE_WINDOW', quit)

# loop
top.mainloop()