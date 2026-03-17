import tkinter as tk
from tkinter import messagebox


class Actividad:
    def __init__(self, codigo, nombre, materia):
        self.codigo = codigo
        self.nombre = nombre
        self.materia = materia
        self.estado = "Pendiente"


class Nodo:
    def __init__(self, actividad):
        self.actividad = actividad
        self.siguiente = None


class ListaSimple:
    def __init__(self):
        self.inicio = None
        self.codigo_actual = 1

    def agregar(self, nombre, materia):
        actividad = Actividad(self.codigo_actual, nombre, materia)
        self.codigo_actual += 1

        nuevo = Nodo(actividad)

        if self.inicio is None:
            self.inicio = nuevo
        else:
            actual = self.inicio
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def mostrar(self):
        texto = ""
        actual = self.inicio

        if actual is None:
            return "No hay actividades registradas."

        while actual is not None:
            a = actual.actividad
            texto += (
                "Código: " + str(a.codigo) +
                " | Actividad: " + a.nombre +
                " | Materia: " + a.materia +
                " | Estado: " + a.estado + "\n"
            )
            actual = actual.siguiente

        return texto

    def marcar_realizada(self, codigo):
        actual = self.inicio

        while actual is not None:
            if actual.actividad.codigo == codigo:
                actual.actividad.estado = "Realizada"
                return True
            actual = actual.siguiente

        return False

    def siguiente_pendiente(self):
        actual = self.inicio

        while actual is not None:
            if actual.actividad.estado == "Pendiente":
                return actual.actividad
            actual = actual.siguiente

        return None


class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Plan de Estudio - Lista Simple")
        self.ventana.geometry("700x500")

        self.lista = ListaSimple()

        tk.Label(ventana, text="Actividad").pack()
        self.entry_nombre = tk.Entry(ventana, width=40)
        self.entry_nombre.pack()

        tk.Label(ventana, text="Materia").pack()
        self.entry_materia = tk.Entry(ventana, width=40)
        self.entry_materia.pack()

        tk.Button(ventana, text="Agregar actividad", command=self.agregar_actividad).pack(pady=5)

        tk.Label(ventana, text="Código a marcar como realizada").pack()
        self.entry_codigo = tk.Entry(ventana, width=20)
        self.entry_codigo.pack()

        tk.Button(ventana, text="Marcar realizada", command=self.marcar_actividad).pack(pady=5)
        tk.Button(ventana, text="Mostrar lista", command=self.mostrar_lista).pack(pady=5)
        tk.Button(ventana, text="Ver siguiente pendiente", command=self.ver_siguiente).pack(pady=5)

        self.area_texto = tk.Text(ventana, width=80, height=15)
        self.area_texto.pack(pady=10)

    def agregar_actividad(self):
        nombre = self.entry_nombre.get()
        materia = self.entry_materia.get()

        if nombre == "" or materia == "":
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return

        self.lista.agregar(nombre, materia)
        self.entry_nombre.delete(0, tk.END)
        self.entry_materia.delete(0, tk.END)
        self.mostrar_lista()

    def marcar_actividad(self):
        codigo_texto = self.entry_codigo.get()

        if codigo_texto == "":
            messagebox.showwarning("Aviso", "Ingresa un código.")
            return

        if not codigo_texto.isdigit():
            messagebox.showwarning("Aviso", "El código debe ser numérico.")
            return

        codigo = int(codigo_texto)
        encontrado = self.lista.marcar_realizada(codigo)

        if encontrado:
            messagebox.showinfo("Éxito", "Actividad marcada como realizada.")
        else:
            messagebox.showwarning("Aviso", "No se encontró el código.")

        self.entry_codigo.delete(0, tk.END)
        self.mostrar_lista()

    def mostrar_lista(self):
        self.area_texto.delete("1.0", tk.END)
        self.area_texto.insert(tk.END, self.lista.mostrar())

    def ver_siguiente(self):
        actividad = self.lista.siguiente_pendiente()

        if actividad is None:
            messagebox.showinfo("Información", "No hay actividades pendientes.")
        else:
            mensaje = (
                "Siguiente actividad pendiente:\n\n"
                "Código: " + str(actividad.codigo) + "\n"
                "Actividad: " + actividad.nombre + "\n"
                "Materia: " + actividad.materia
            )
            messagebox.showinfo("Pendiente", mensaje)


ventana = tk.Tk()
app = App(ventana)
ventana.mainloop()