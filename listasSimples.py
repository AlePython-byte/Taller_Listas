import tkinter as tk
from tkinter import messagebox


class Cancion:
    def __init__(self, codigo, titulo, artista):
        self.codigo = codigo
        self.titulo = titulo
        self.artista = artista
        self.estado = "En cola"


class Nodo:
    def __init__(self, cancion):
        self.cancion = cancion
        self.siguiente = None


class ListaSimple:
    def __init__(self):
        self.inicio = None
        self.codigo = 1

    def agregar(self, titulo, artista):
        cancion = Cancion("C" + str(self.codigo), titulo, artista)
        self.codigo += 1
        nuevo = Nodo(cancion)

        if self.inicio is None:
            self.inicio = nuevo
            return

        actual = self.inicio
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def buscar(self, codigo):
        actual = self.inicio
        while actual is not None:
            if actual.cancion.codigo == codigo:
                return actual.cancion
            actual = actual.siguiente
        return None

    def reproducir(self):
        actual = self.inicio
        while actual is not None:
            if actual.cancion.estado == "Reproduciendo":
                return actual.cancion
            actual = actual.siguiente

        actual = self.inicio
        while actual is not None:
            if actual.cancion.estado != "Reproducida":
                actual.cancion.estado = "Reproduciendo"
                return actual.cancion
            actual = actual.siguiente
        return None

    def siguiente(self):
        actual = self.inicio
        while actual is not None:
            if actual.cancion.estado == "Reproduciendo":
                actual.cancion.estado = "Reproducida"
                sig = actual.siguiente
                while sig is not None:
                    if sig.cancion.estado != "Reproducida":
                        sig.cancion.estado = "Reproduciendo"
                        return sig.cancion
                    sig = sig.siguiente
                return None
            actual = actual.siguiente

        return self.reproducir()

    def mostrar(self):
        texto = ""
        actual = self.inicio
        pos = 1

        if actual is None:
            return "No hay canciones registradas."

        while actual is not None:
            c = actual.cancion
            texto += (
                "Nodo " + str(pos) +
                " | " + c.codigo +
                " | " + c.titulo +
                " | " + c.artista +
                " | " + c.estado + "\n"
            )
            actual = actual.siguiente
            pos += 1

        return texto


class App:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Reproductor Musical - Lista Simple")
        self.ventana.geometry("760x500")
        self.ventana.config(bg="#f8fafc")

        self.lista = ListaSimple()

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(
            self.ventana,
            text="Mini Reproductor Musical",
            font=("Arial", 18, "bold"),
            bg="#f8fafc",
            fg="#1e3a8a"
        ).pack(pady=10)

        tk.Label(
            self.ventana,
            text="Lista simple enlazada de canciones",
            font=("Arial", 10),
            bg="#f8fafc",
            fg="#475569"
        ).pack()

        panel = tk.Frame(self.ventana, bg="#f8fafc")
        panel.pack(fill="both", expand=True, padx=15, pady=15)

        izq = tk.Frame(panel, bg="#e2e8f0", bd=1, relief="solid")
        izq.pack(side="left", fill="y", padx=(0, 10))

        der = tk.Frame(panel, bg="#e2e8f0", bd=1, relief="solid")
        der.pack(side="right", fill="both", expand=True)

        tk.Label(izq, text="Título", bg="#e2e8f0", font=("Arial", 11, "bold")).pack(pady=(15, 5))
        self.entry_titulo = tk.Entry(izq, width=25, font=("Arial", 11))
        self.entry_titulo.pack(pady=5, padx=15)

        tk.Label(izq, text="Artista", bg="#e2e8f0", font=("Arial", 11, "bold")).pack(pady=(10, 5))
        self.entry_artista = tk.Entry(izq, width=25, font=("Arial", 11))
        self.entry_artista.pack(pady=5, padx=15)

        tk.Button(
            izq, text="Agregar canción", command=self.agregar,
            bg="#93c5fd", fg="black", width=20
        ).pack(pady=10)

        tk.Button(
            izq, text="Reproducir", command=self.reproducir,
            bg="#86efac", fg="black", width=20
        ).pack(pady=5)

        tk.Button(
            izq, text="Siguiente", command=self.siguiente,
            bg="#fcd34d", fg="black", width=20
        ).pack(pady=5)

        tk.Label(izq, text="Buscar código", bg="#e2e8f0", font=("Arial", 11, "bold")).pack(pady=(15, 5))
        self.entry_codigo = tk.Entry(izq, width=25, font=("Arial", 11))
        self.entry_codigo.pack(pady=5, padx=15)

        tk.Button(
            izq, text="Buscar canción", command=self.buscar,
            bg="#c4b5fd", fg="black", width=20
        ).pack(pady=10)

        self.label_actual = tk.Label(
            der,
            text="Sonando: Nada",
            font=("Arial", 12, "bold"),
            bg="#e2e8f0",
            fg="#0f172a"
        )
        self.label_actual.pack(pady=15)

        self.area = tk.Text(
            der,
            width=55,
            height=20,
            font=("Consolas", 11),
            bg="white",
            fg="black"
        )
        self.area.pack(padx=15, pady=10)

        tk.Button(
            der, text="Actualizar lista", command=self.actualizar,
            bg="#bae6fd", fg="black", width=18
        ).pack(pady=8)

    def agregar(self):
        titulo = self.entry_titulo.get().strip()
        artista = self.entry_artista.get().strip()

        if titulo == "" or artista == "":
            messagebox.showwarning("Aviso", "Completa todos los campos.")
            return

        self.lista.agregar(titulo, artista)
        self.entry_titulo.delete(0, tk.END)
        self.entry_artista.delete(0, tk.END)
        self.actualizar()

    def reproducir(self):
        cancion = self.lista.reproducir()
        if cancion is None:
            messagebox.showwarning("Aviso", "No hay canciones disponibles.")
        self.actualizar()

    def siguiente(self):
        self.lista.siguiente()
        self.actualizar()

    def buscar(self):
        codigo = self.entry_codigo.get().strip()
        cancion = self.lista.buscar(codigo)

        if cancion is None:
            messagebox.showwarning("Aviso", "No se encontró la canción.")
            return

        mensaje = (
            "Código: " + cancion.codigo + "\n"
            "Título: " + cancion.titulo + "\n"
            "Artista: " + cancion.artista + "\n"
            "Estado: " + cancion.estado
        )
        messagebox.showinfo("Canción encontrada", mensaje)

    def actualizar(self):
        self.area.delete("1.0", tk.END)
        self.area.insert(tk.END, self.lista.mostrar())

        actual = self.lista.reproducir()
        if actual is None:
            self.label_actual.config(text="Sonando: Nada")
        else:
            self.label_actual.config(text="Sonando: " + actual.titulo + " - " + actual.artista)
            if actual.estado != "Reproduciendo":
                actual.estado = "Reproduciendo"


ventana = tk.Tk()
app = App(ventana)
ventana.mainloop()