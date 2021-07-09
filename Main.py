from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import csv


class Application():
    def __init__(self):
        #super(Application, self).__init__()
        self.root = Tk()
        self.root.geometry("800x600")
        self.root.title("Base expansion predictions")

        self.root.geometry("900x700")
        self.root.resizable(0,0)

        self.boton1=ttk.Button(self.root, text = "Buscar un archivo", command = self.fileDialog)
        self.boton1.place(x=20, y=20, width=150, height=30)

        self.text = StringVar()
        self.text.set("Ruta")
        self.path = ttk.Label(self.root, textvariable=self.text)
        self.path.place(x=20, y=60, width=150, height=30)

        self.boton2 = ttk.Button(self.root, text="Función a trozos constante", command=self.fileDialog)
        self.boton2.place(x=20, y=100, width=250, height=30)

        self.boton3 = ttk.Button(self.root, text="Función a trozos con regresión", command=self.fileDialog)
        self.boton3.place(x=20, y=140, width=250, height=30)

        self.boton4 = ttk.Button(self.root, text="Spline lineal", command=self.fileDialog)
        self.boton4.place(x=20, y=180, width=250, height=30)

        self.boton5 = ttk.Button(self.root, text="Spline cúbico", command=self.fileDialog)
        self.boton5.place(x=20, y=220, width=250, height=30)

        self.boton6 = ttk.Button(self.root, text="Spline cúbico natural", command=self.fileDialog)
        self.boton6.place(x=20, y=260, width=250, height=30)

        self.slider = ttk.Scale(self.root, from_=1, to = 30, orient=HORIZONTAL, command=self.fileDialog)
        self.slider.place(x=20, y=260, width=250, height=30)

        # Graficos de matplotlib
        self.data = []
        self.f = Figure( figsize=(100, 100), dpi=80 )
        self.ax0 = self.f.add_axes((0.1, .1, .90, .90), facecolor=(.75, .75, .75), frameon=False)
        self.ax0.set_xlabel('Y')
        self.ax0.set_ylabel('X')
        self.ax0.plot(self.data)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.root)
        self.canvas.get_tk_widget().place(x=300, y=50, width=500, height=500)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.place(x=300, y=550, width=400, height=100)
        self.toolbar.update()
        self.root.mainloop()

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/Universidad/Materias/Modelos estocasticos/Proyecto", title = "Seleccione un archivo")
        self.text.set(self.filename.split("/")[-1]) #ttk.Label(self.root, text=self.filename.name).grid(pady=0, row=1, column =0, columnspan=4)

        x = []
        y = []
        with open(self.filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    x.append(float(row[0]))
                    y.append((float(row[1])))
                except:
                    pass
            #data =  list(reader)
            #self.data = data
            self.ax0.clear()
            self.ax0.scatter(x,y)
            self.canvas.draw()


app = Application()
