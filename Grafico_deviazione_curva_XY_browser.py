
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sys import argv
import time
import sys, os, re
from tkinter import *
from tkinter import messagebox, scrolledtext
import tkinter as tk
from os.path import exists
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from scipy.interpolate import griddata
import threading
import plotly.graph_objects as go
from plotly.colors import make_colorscale
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import webbrowser
import asyncio
from websockets import serve


terminate_thread = threading.Event()

colour = 'green2'

top = tk.Tk()
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

port = 8050

def grafico():
    global terminate_thread
    global port
    port = port+1

    try:
        app.server.stop()
    except:
        print("no server")

    terminate_thread.clear()

    dash_thread = threading.Thread(target = grafico2)
    dash_thread.setDaemon(True)
    dash_thread.start()

    webbrowser.open(f'http://127.0.0.1:{port}/')

    try:
        app.server.stop()
    except:
        print("no server")




def grafico2():
    global port

    cmap = cm.jet
    cmap_r = reverse_colourmap(cmap)
    scelta = var.get()

    filename = E1.get()

    if (exists(filename)):

        #Funzione visulizza lista numeri
        def show_point_list(x, y, err):
            point_list = 'x(mm)\t\ty(mm)\t\terr(°)\n'
            for xi, yi, zi in zip(x, y, z):
                point_list += f'{xi:.1f}\t\t{yi:.1f}\t\t{zi:.6f}\n'

            root = tk.Tk()
            root.title('Lista dei punti')

            # Aggiungi un widget di testo scorrevole
            text_widget = scrolledtext.ScrolledText(root, width = 45, height = 40)
            text_widget.insert(tk.INSERT, point_list)
            text_widget.pack()

            root.mainloop()

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
        print("nuovo")
        print(z)

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

        # Creazione di una griglia 2D per l'interpolazione
        grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
        # Interpolazione dei dati
        grid_angle = griddata((x, y), z, (grid_x, grid_y), method = 'cubic')  # cubic, linear or nearest


        def get_point_list(x, y, z):
            point_list = 'x(mm)\t\ty(mm)\t\terr(°)\n'
            for xi, yi, zi in zip(x, y, z):
                point_list += f'{xi:.1f}\t\t{yi:.1f}\t\t{zi:.6f}\n'
            return point_list


        colors = ['red', 'yellow', 'lime', 'yellow', 'red']

        fig = go.Figure(data = [go.Surface(z = grid_angle, x = grid_x, y = grid_y, cmax = 0.003, cmin = -0.003, colorscale = colors, reversescale= True)])

        # Aggiungi etichette ai punti
        hover_text = []

        for i in range(len(grid_x)):
            hover_text.append([])
            for j in range(len(grid_x[i])):
                val = str(grid_angle[i][j])
                hover_text[i].append(val)

        fig.update_traces(hoverinfo = 'z', text = hover_text)

        fig.update_layout(scene = dict(
            xaxis_title = 'Asse X (mm)',
            yaxis_title = 'Asse Y (mm)',
            zaxis_title = 'Err (°)',
            zaxis = dict(range = [-0.006, 0.006])
        ))

        # Crea un'applicazione Dash
        app = dash.Dash(__name__)
        app.config.suppress_callback_exceptions = True
        # Layout dell'applicazione
        app.layout = html.Div(children = [
            html.Div([
                dcc.Textarea(
                    id = 'point-list',
                    value = get_point_list(x, y, z),
                    style = {'width': 360, 'height': 900}
                )
            ], style = {'float': 'right', 'margin-right': '60px'}),
            dcc.Graph(
                id = '3d-graph',
                figure = fig,
                style = {'width': '75%', 'height': 900}
            )
        ])

        # Funzione callback per aggiornare l'elenco dei punti
        '''@app.callback(
            Output('3d-graph', 'figure'),
            [Input('dropdown-selector', 'value'),  # Sostituisci con il tuo input
             Input('another-input', 'value')]
        )



        def update_graph(value,figure):
            global fig
            # Aggiorna i dati x, y, z in base agli input
            # Ad esempio, usa i nuovi valori di selected_value e another_value per generare nuovi dati x, y, z

            # Crea il nuovo grafico
            fig = go.Figure()
            # Aggiungi traccia 3D con i nuovi dati x, y, z
            fig.add_trace(go.Surface(z = new_z, x = new_x, y = new_y))
            value = get_point_list(z = new_z, x = new_x, y = new_y)
            # Aggiorna il layout o altre configurazioni se necessario
            fig.update_layout(scene = dict(
                xaxis_title = 'Asse X',
                yaxis_title = 'Asse Y',
                zaxis_title = 'Asse Z',
                zaxis = dict(range = [-2, 2])
            ))

            return fig,value'''
        # Esegui l'applicazione Dash
        app.run_server(debug = False, port = port, use_reloader = False)
        print("SIIIIIIIIIIIII")
        #fig.show()



    else:
        L3 = Label(top, text = "File not exist", fg = "red")
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
b = tk.Button(top, text = "View  \n graph  ", bd = 4, command = grafico)
b.pack(padx = 50, pady = 20)
b.place(x = 15, y = 80)

b2 = tk.Button(top, text = "Choose path from PC", bd = 4, command = select_file)
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
    global terminate_thread
    terminate_thread.set()
    top.destroy()
    sys.exit()


# quit
top.protocol('WM_DELETE_WINDOW', quit)

# loop
top.mainloop()
