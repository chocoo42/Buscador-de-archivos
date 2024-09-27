import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import messagebox
import subprocess
import platform
import sys

def get_resource_path(relative_path):
    """ 
    Obtiene la ruta del archivo de configuración, ya sea cuando se ejecuta como .py o como .exe.
    """
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))  # Apunta a la carpeta del .exe o script
    return os.path.join(base_path, relative_path)


# Usa esta función para generar la ruta correcta del archivo de configuración
CONFIG_FILE = get_resource_path("config.json")

class FacturaChecker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Verificador de Facturas")
        self.geometry("400x500+100+200")

        # Inicializamos las variables para las tres carpetas
        self.descargadas_materia_prima_folder = None
        self.descargadas_generales_folder = None
        self.cargadas_folder = None

        # Botón para seleccionar la carpeta de facturas descargadas de materia prima
        self.descargadas_materia_prima_btn = tk.Button(self, text="Seleccionar carpeta de facturas descargadas (Materia Prima)", 
                                                       command=self.seleccionar_descargadas_materia_prima, 
                                                       font=("Comfortaa", 10), bd=2)
        self.descargadas_materia_prima_btn.pack(pady=10)
        self.descargadas_materia_prima_symbol = tk.Label(self, text="❌")  # Símbolo ❌ por defecto
        self.descargadas_materia_prima_symbol.pack()
        self.materia_prima_path_label = tk.Label(self, text="")
        self.materia_prima_path_label.pack()

        # Botón para seleccionar la carpeta de facturas descargadas generales
        self.descargadas_generales_btn = tk.Button(self, text="Seleccionar carpeta de facturas descargadas (Generales)", 
                                                   command=self.seleccionar_descargadas_generales, 
                                                   font=("Comfortaa", 10), bd=2)
        self.descargadas_generales_btn.pack(pady=10)
        self.descargadas_generales_symbol = tk.Label(self, text="❌")  # Símbolo ❌ por defecto
        self.descargadas_generales_symbol.pack()
        self.generales_path_label = tk.Label(self, text="")
        self.generales_path_label.pack()

        # Botón para seleccionar la carpeta de facturas cargadas
        self.cargadas_btn = tk.Button(self, text="Seleccionar carpeta de facturas cargadas", 
                                      command=self.seleccionar_cargadas, 
                                      font=("Comfortaa", 10), bd=2)
        self.cargadas_btn.pack(pady=10)
        self.cargadas_symbol = tk.Label(self, text="❌")  # Símbolo ❌ por defecto
        self.cargadas_symbol.pack()
        self.cargadas_path_label = tk.Label(self, text="")
        self.cargadas_path_label.pack()

        # Campo para el nombre de la factura
        self.factura_label = tk.Label(self, text="Nombre de la Factura:", font=("Comfortaa", 12))
        self.factura_label.pack(pady=5)
        self.factura_entry = tk.Entry(self, font=("Comfortaa", 12), width=40)
        self.factura_entry.pack(pady=5)

        # Botón para iniciar la verificación de la factura
        self.verificar_btn = tk.Button(self, text="Verificar", command=self.verificar_factura, 
                                       bg="green", fg="white", cursor="hand2", 
                                       font=("Comfortaa", 12, "bold"))
        self.verificar_btn.pack(pady=40)

          # Resultado
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=5)

        # Almacena las rutas de los archivos encontrados
        self.archivos_encontrados = []

        # Después de que todos los widgets han sido creados, cargamos la configuración
        self.cargar_configuracion()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def cargar_configuracion(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                self.descargadas_materia_prima_folder = config.get("descargadas_materia_prima_folder", None)
                self.descargadas_generales_folder = config.get("descargadas_generales_folder", None)
                self.cargadas_folder = config.get("cargadas_folder", None)
                self.actualizar_simbolos()
        else:
            print("No se encontró archivo de configuración.")

    def guardar_configuracion(self):
        config = {
            "descargadas_materia_prima_folder": self.descargadas_materia_prima_folder,
            "descargadas_generales_folder": self.descargadas_generales_folder,
            "cargadas_folder": self.cargadas_folder
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file)

    def seleccionar_descargadas_materia_prima(self):
        self.descargadas_materia_prima_folder = filedialog.askdirectory()
        if self.descargadas_materia_prima_folder:
            self.materia_prima_path_label.config(text=self.descargadas_materia_prima_folder)
            self.descargadas_materia_prima_symbol.config(text="✔️")  # Cambiar a ✔️ si se selecciona la carpeta
        else:
            self.descargadas_materia_prima_symbol.config(text="❌")  # Devolver a ❌ si no se selecciona nada

    def seleccionar_descargadas_generales(self):
        self.descargadas_generales_folder = filedialog.askdirectory()
        if self.descargadas_generales_folder:
            self.generales_path_label.config(text=self.descargadas_generales_folder)
            self.descargadas_generales_symbol.config(text="✔️")
        else:
            self.descargadas_generales_symbol.config(text="❌")

    def seleccionar_cargadas(self):
        self.cargadas_folder = filedialog.askdirectory()
        if self.cargadas_folder:
            self.cargadas_path_label.config(text=self.cargadas_folder)
            self.cargadas_symbol.config(text="✔️")
        else:
            self.cargadas_symbol.config(text="❌")

    def verificar_factura(self):
        nombre_factura = self.factura_entry.get().lower()

        if not nombre_factura:
            self.result_label.config(text="Por favor, ingrese el nombre de la factura.")
            return

        # No es necesario que las 3 carpetas estén seleccionadas, con que haya una es suficiente
        if not (self.descargadas_materia_prima_folder or self.descargadas_generales_folder or self.cargadas_folder):
            self.result_label.config(text="Por favor, seleccione al menos una carpeta.")
            return

        self.archivos_encontrados.clear()  # Limpiar la lista de archivos encontrados

        if self.descargadas_materia_prima_folder:
            self.archivos_encontrados += self.buscar_archivos_similares(self.descargadas_materia_prima_folder, nombre_factura)

        if self.descargadas_generales_folder:
            self.archivos_encontrados += self.buscar_archivos_similares(self.descargadas_generales_folder, nombre_factura)

        if self.cargadas_folder:
            self.archivos_encontrados += self.buscar_archivos_similares(self.cargadas_folder, nombre_factura)

        if self.archivos_encontrados:
            self.result_label.config(text="Archivos encontrados:")
            self.mostrar_archivos_encontrados()  # Llama al método para mostrar los archivos encontrados
        else:
            self.result_label.config(text="No se encontraron archivos con ese nombre.")

    def buscar_archivos_similares(self, carpeta, nombre_factura):
        archivos = os.listdir(carpeta)
        return [os.path.join(carpeta, archivo) for archivo in archivos if nombre_factura in archivo.lower()]

    def mostrar_archivos_encontrados(self):
        # Mostrar un cuadro de diálogo con los archivos encontrados
        seleccion = simpledialog.askstring("Seleccionar archivo", "Archivos encontrados:\n" + "\n".join(self.archivos_encontrados) + "\nIngrese el nombre del archivo a previsualizar:")
        
        if seleccion:
            archivo_a_previsualizar = next((archivo for archivo in self.archivos_encontrados if seleccion.lower() in archivo.lower()), None)
            if archivo_a_previsualizar:
                self.archivo_encontrado = archivo_a_previsualizar  # Guardar el archivo seleccionado para previsualizar
                self.previsualizar_archivo()  # Llama a la función de previsualización
            else:
                messagebox.showerror("Error", "No se encontró un archivo con ese nombre.")

    def previsualizar_archivo(self):
        if self.archivo_encontrado:
            try:
                if platform.system() == "Windows":
                    os.startfile(self.archivo_encontrado)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.Popen(["open", self.archivo_encontrado])
                else:  # Linux
                    subprocess.Popen(["xdg-open", self.archivo_encontrado])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

    def actualizar_simbolos(self):
        if self.descargadas_materia_prima_folder:
            self.descargadas_materia_prima_symbol.config(text="✔️")
            self.materia_prima_path_label.config(text=self.descargadas_materia_prima_folder)
        if self.descargadas_generales_folder:
            self.descargadas_generales_symbol.config(text="✔️")
            self.generales_path_label.config(text=self.descargadas_generales_folder)
        if self.cargadas_folder:
            self.cargadas_symbol.config(text="✔️")
            self.cargadas_path_label.config(text=self.cargadas_folder)

    def on_closing(self):
        self.guardar_configuracion()
        self.destroy()

if __name__ == "__main__":
    app = FacturaChecker()
    app.mainloop()