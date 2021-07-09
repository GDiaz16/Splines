from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox as MessageBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import math as mt

class Application():
    def __init__(self):
        self.x = []
        self.y = []
        self.knots = 1

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

        self.boton2 = ttk.Button(self.root, text="Función a trozos constante", command=self.piecewise_constant)
        self.boton2.place(x=20, y=100, width=250, height=30)

        self.boton3 = ttk.Button(self.root, text="Función a trozos con regresión", command=self.piecewise_linear)
        self.boton3.place(x=20, y=140, width=250, height=30)

        self.boton4 = ttk.Button(self.root, text="Spline lineal", command=self.linear_spline)
        self.boton4.place(x=20, y=180, width=250, height=30)

        self.boton5 = ttk.Button(self.root, text="Spline cúbico", command=self.cubic_spline)
        self.boton5.place(x=20, y=220, width=250, height=30)

        self.boton6 = ttk.Button(self.root, text="Spline cúbico natural", command=self.natural_cubic_spline)
        self.boton6.place(x=20, y=260, width=250, height=30)

        self.label1 = ttk.Label(self.root, text="Número de nudos:")
        self.label1.place(x=20, y=300, width=150, height=20)
        self.slider = ttk.Scale(self.root, from_=0.01, to = 1, orient=HORIZONTAL, command=self.setKnots)
        self.slider.place(x=20, y=320, width=250, height=30)

        # Labels del slider
        self.text2 = StringVar()
        self.text2.set("1")
        self.text3 = StringVar()
        self.text3.set("1")
        self.text4 = StringVar()
        self.text4.set("1")
        self.label2 = ttk.Label(self.root, textvariable=self.text2)
        self.label2.place(x=20, y=340, width=30, height=20)
        self.label3 = ttk.Label(self.root, textvariable=self.text3)
        self.label3.place(x=125, y=340, width=30, height=20)
        self.label4 = ttk.Label(self.root, textvariable=self.text4)
        self.label4.place(x=250, y=340, width=30, height=20)

        # Label residual sum of squares
        self.text6 = StringVar()
        self.text6.set("0")
        self.label5 = ttk.Label(self.root, text="Residual Sum of Squares:", font ="bold")
        self.label5.place(x=20, y=370, width=250, height=20)
        self.label6 = ttk.Label(self.root, textvariable=self.text6)
        self.label6.place(x=20, y=390, width=250, height=20)

        # Label Mean Squared Error
        self.text8 = StringVar()
        self.text8.set("0")
        self.label7 = ttk.Label(self.root,  text="Mean Squared Error", font ="bold")
        self.label7.place(x=20, y=420, width=250, height=20)
        self.label8 = ttk.Label(self.root, textvariable=self.text8)
        self.label8.place(x=20, y=440, width=250, height=20)

        # Boton para descargar
        self.boton6 = ttk.Button(self.root, text="Guardar resultados", command=self.save_results)
        self.boton6.place(x=80, y=500, width=130, height=30)

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

        self.x = []
        self.y = []
        with open(self.filename, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    self.x.append(float(row[0]))
                    self.y.append((float(row[1])))
                except:
                    pass
            #data =  list(reader)
            #self.data = data
            self.ax0.clear()
            self.ax0.scatter(self.x,self.y)
            self.canvas.draw()
            self.text4.set(len(self.x)-1)

    def setKnots(self, x_slider):
        try:
            self.knots = math.ceil((len(self.x)-1)*float(x_slider))
            self.text3.set(self.knots)
        except:
            pass

    """Funcion indicadora con 2 limites"""
    def I(self, x, k1, k2):
        if x > k1 and x < k2:
            return 1
        else:
            return 0

    """Funcion parte entera para los nudos"""
    def ind(self, x, k):
        if x <= k:
            return 0
        elif x > k:
            return x - k

    """Generamos una grafica scatter de los vectores de entrada y una plot del estimado"""
    def show_graph(self, x, y, y_est):
        rss, mse = self.residualSumOfSquares(y, y_est)
        self.y_est = y_est
        self.text6.set(rss)
        self.text8.set(mse)
        self.ax0.clear()
        self.ax0.scatter(x, y)
        self.ax0.plot(x, y_est, color='red', linewidth=3)
        self.canvas.draw()

    """
    X = np.linalg.inv(N.T.dot(N))
    Y = X.dot(N.T)
    theta = Y.dot(y)
    """

    """Regresion minimos cuadrados entre una Matriz X y un vector y"""
    def mult_reg(self, X, y):
        X = np.array(X)
        y = np.array(y)
        b = np.linalg.lstsq(X.T, y, rcond=None)[0]
        return b

    """Regresion minimos cuadrados con penalizacion entre una Matriz N y un vector y"""
    def pen_reg(self, N, x, y, k):
        N_omega = self.smooth_func(N, x)
        N = np.array(N)
        n = N.shape[1]
        y = np.array(y)
        X = N.T.dot(N) + (k * N_omega)
        y = N.T.dot(y)
        b = np.linalg.solve(X, y)
        return b

    """Obtener un Y estimado a partir de las funciones base"""
    def estimate(self, n, x, h, b):
        y_est = []
        for i in range(0, n):
            x_num = x[i]
            y_num = 0
            for j in range(0, len(h)):
                y_num += h[j][i] * b[j]
            y_est.append(y_num)
        return y_est

    """Funcion para el Spline Cubico Natural"""
    def dk(self, x, k, K):
        res = (self.ind(x, k) ** 3 - self.ind(x, K) ** 3) / (K - k)
        return res

    """Funcion que recibe un vector Y y su estimado Y_est y calcula su RSS"""
    def residualSumOfSquares(self, y, y_est):
        sum = 0
        for i in range(0, len(y)):
            sum += (y[i] - y_est[i]) ** 2
        mean = sum / len(y)
        return sum, mean

    """Derivada de 2do grado de un vector Y """
    def second_derivative(self, y, x):
        diff1 = np.diff(y, 2) / np.diff(x, 2)
        return diff1

    def smooth_func(self, N, x):
        n = len(N)
        smooth = np.zeros((n, n))
        for i in range(0, len(N)):
            for j in range(0, len(N)):
                dy1 = self.second_derivative(N[i], x)
                dy2 = self.second_derivative(N[j], x)
                dy = dy1 * dy2
                nx = np.delete(x, [0, 1])
                s = np.trapz(dy, nx)
                smooth[i][j] = s
        return smooth

    def piecewise_constant(self):
        try:
            h = []
            num_puntos = len(self.x)
            div = mt.floor(num_puntos / (self.knots + 1))

            """Obtener valores de las funciones base"""
            for m in range(0, self.knots + 1):
                first = m * div / num_puntos
                last = (m + 1) * div / num_puntos
                h_m = []
                for i in range(0, num_puntos):
                    h_x = self.I(self.x[i], first, last)
                    h_m.append(h_x)
                h.append(h_m)

            """Calculo Regresion Lineal Multiple"""
            b = self.mult_reg(h, self.y)

            """Generar valores f(x) para el estimado"""
            y_est = self.estimate(num_puntos, self.x, h, b)

            self.show_graph(self.x, self.y, y_est)

        except:
            print(sys.exc_info())
            MessageBox.showinfo("Error", "Debe cargar un dataset")

    def piecewise_linear(self):
        try:
            h, h2 = [], []
            y_est = []
            num_puntos = len(self.x)
            div = mt.floor(num_puntos / (self.knots + 1))

            """Obtener valores de las funciones base"""
            for m in range(0, (self.knots + 1) * 2):
                first = m * div / num_puntos
                last = (m + 1) * div / num_puntos
                h_m, h_m2 = [], []
                for i in range(0, num_puntos):
                    h_x = self.I(self.x[i], first, last)
                    h_x2 = self.I(self.x[i], first, last) * self.x[i]
                    h_m.append(h_x)
                    h_m2.append(h_x2)
                h.append(h_m)
                h2.append(h_m2)

            h = h + h2

            """Calculo Regresion Lineal Multiple"""
            b = self.mult_reg(h, self.y)

            """Generar valores f(x) para el estimado"""
            y_est = self.estimate(num_puntos, self.x, h, b)
            self.show_graph(self.x, self.y, y_est)

        except:
            print(sys.exc_info())
            MessageBox.showinfo("Error", "Debe cargar un dataset")

    def linear_spline(self):
        try:
            h = []
            y_est = []
            num_puntos = len(self.x)
            div = mt.floor(num_puntos / (self.knots + 1))

            """Obtener valores de funciones base para 4 parametros iniciales 1, x"""
            h_m, h_m2 = [], []
            for i in range(0, num_puntos):
                h_m.append(1.0)
                h_m2.append(self.x[i])
            h.append(h_m)
            h.append(h_m2)

            """Obtener valores de funciones base para parametros por cada nodo (x-k)+"""
            for m in range(1, self.knots + 1):
                h_m = []
                for i in range(0, num_puntos):
                    h_x = self.ind(self.x[i], m * div / num_puntos)
                    h_m.append(h_x)
                h.append(h_m)

            """Calculo Regresion Lineal Multiple"""
            b = self.mult_reg(h, self.y)

            """Generar valores f(x) para el estimado"""
            y_est = self.estimate(num_puntos, self.x, h, b)
            self.show_graph(self.x, self.y, y_est)

        except:
            print(sys.exc_info())
            MessageBox.showinfo("Error", "Debe cargar un dataset")

    def cubic_spline(self):
        try:
            h = []
            y_est = []
            num_puntos = len(self.x)
            div = mt.floor(num_puntos / (self.knots + 1))

            """Obtener valores de funciones base para 4 parametros iniciales 1, x , x^2, x^3"""
            h_m, h_m2, h_m3, h_m4 = [], [], [], []
            for i in range(0, num_puntos):
                h_m.append(1.0)
                h_m2.append(self.x[i])
                h_m3.append(self.x[i] ** 2)
                h_m4.append(self.x[i] ** 3)
            h.append(h_m)
            h.append(h_m2)
            h.append(h_m3)
            h.append(h_m4)

            """Obtener valores de funciones base para parametros por cada nodo (x-k)^3+"""
            for m in range(1, self.knots + 1):
                h_m = []
                for i in range(0, num_puntos):
                    h_x = self.ind(self.x[i], m * div / num_puntos) ** 3
                    h_m.append(h_x)
                h.append(h_m)

            """Calculo Regresion Lineal Multiple"""
            b = self.mult_reg(h, self.y)

            """Generar valores f(x) para el estimado"""
            y_est = self.estimate(num_puntos, self.x, h, b)
            self.show_graph(self.x, self.y, y_est)

        except:
            print(sys.exc_info())
            MessageBox.showinfo("Error", "Debe cargar un dataset")

    def natural_cubic_spline(self):
        try:
            h = []
            y_est = []
            num_puntos = len(self.x)
            div = mt.floor(num_puntos / (self.knots + 1))

            """Obtener valores de funciones base para 4 parametros iniciales 1, x"""
            h_m = []
            h_m2 = []
            for i in range(0, num_puntos):
                h_m.append(1.0)
                h_m2.append(self.x[i])
            h.append(h_m)
            h.append(h_m2)

            """Obtener valores de funciones base para parametros por cada nodo dk(x) - dK-1(x)"""
            for m in range(1, self.knots + 1):
                h_m = []
                for i in range(0, num_puntos):
                    h_x = self.dk(self.x[i], m * div / num_puntos, (self.knots + 1) * div / num_puntos) - self.dk(self.x[i], self.knots * div / num_puntos, (self.knots + 1) * div / num_puntos)
                    h_m.append(h_x)
                h.append(h_m)

            """Calculo Regresion Lineal Multiple"""
            b = self.mult_reg(h, self.y)

            """Generar valores f(x) para el estimado"""
            y_est = self.estimate(num_puntos, self.x, h, b)
            self.show_graph(self.x, self.y, y_est)

        except:
            print(sys.exc_info())
            MessageBox.showinfo("Error", "Debe cargar un dataset")

    def save_results(self):
        f = filedialog.asksaveasfile(mode="w", filetypes=[('csv', '.csv'),])
        if f is None:
            return

        fields = ['x', 'y_estimado']
        data = []

        for i in range(0, len(self.x)):
            data.append([self.x[i], self.y_est[i]])

        write = csv.writer(f)

        write.writerow(fields)
        write.writerows(data)

app = Application()
