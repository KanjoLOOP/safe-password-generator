# Importamos herramientas necesarias
import string       # Para usar letras y símbolos
import random       # Para generar cosas al azar
import tkinter as tk  # Para crear la ventana y botones
from tkinter import messagebox, filedialog  # Para mostrar mensajes y guardar archivos
import pyperclip    # Para copiar texto al portapapeles

# Esta función crea una contraseña segura
def generar_contrasena():
    longitud = random.randint(12, 20)  # Elegimos una longitud entre 12 y 20 caracteres
    caracteres = string.ascii_letters + string.digits + string.punctuation  # Letras, números y símbolos

    # Aseguramos que la contraseña tenga al menos una letra mayúscula, una minúscula, un número y un símbolo
    contrasena = [
        random.choice(string.ascii_uppercase),  # Mayúscula
        random.choice(string.ascii_lowercase),  # Minúscula
        random.choice(string.digits),           # Número
        random.choice(string.punctuation)       # Símbolo
    ]

    # Rellenamos el resto de la contraseña con caracteres aleatorios
    while len(contrasena) < longitud:
        contrasena.append(random.choice(caracteres))

    random.shuffle(contrasena)  # Mezclamos el orden para mayor seguridad
    return "".join(contrasena)  # Convertimos la lista en texto

# Esta función genera varias contraseñas según el número que el usuario indique
def generar_contrasenas():
    try:
        num = int(entry_num.get())  # Leemos cuántas contraseñas quiere el usuario
        if num <= 0:
            raise ValueError  # Si el número es 0 o negativo, mostramos error
    except ValueError:
        messagebox.showerror("Error", "Introduce un número válido mayor que 0")
        return

    text_area.config(state="normal")  # Activamos el área de texto
    text_area.delete("1.0", tk.END)   # Borramos lo que había antes

    global lista_contrasenas
    lista_contrasenas = []  # Creamos una lista vacía para guardar las contraseñas

    for _ in range(num):  # Repetimos tantas veces como contraseñas se pidan
        pwd = generar_contrasena()  # Creamos una contraseña
        lista_contrasenas.append(pwd)  # La guardamos
        text_area.insert(tk.END, pwd + "\n")  # La mostramos en pantalla

    text_area.config(state="disabled")  # Bloqueamos el área para que no se edite
    text_area.yview_moveto(0)  # Volvemos al principio del área de texto

# Esta función copia todas las contraseñas generadas al portapapeles
def copiar_todas():
    if not lista_contrasenas:  # Si no hay contraseñas, mostramos advertencia
        messagebox.showwarning("Atención", "No hay contraseñas generadas")
        return
    pyperclip.copy("\n".join(lista_contrasenas))  # Copiamos todas juntas
    messagebox.showinfo("Copiado", "Todas las contraseñas copiadas al portapapeles")

# Esta función guarda las contraseñas en un archivo de texto
def exportar():
    if not lista_contrasenas:  # Si no hay contraseñas, mostramos advertencia
        messagebox.showwarning("Atención", "No hay contraseñas generadas")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto","*.txt")])
    if archivo:  # Si el usuario elige un nombre de archivo
        with open(archivo, "w") as f:
            f.write("\n".join(lista_contrasenas))  # Guardamos todas las contraseñas
        messagebox.showinfo("Exportado", f"Contraseñas exportadas a {archivo}")

# Estas funciones cambian el color del botón cuando el ratón pasa por encima
def on_enter(e):
    e.widget['bg'] = '#00ff00'  # Fondo verde
    e.widget['fg'] = '#000000'  # Texto negro

def on_leave(e):
    e.widget['bg'] = '#000000'  # Fondo negro
    e.widget['fg'] = '#00ff00'  # Texto verde

# Aquí empieza la ventana principal del programa
root = tk.Tk()
root.title("Generador de Contraseñas Hacker")  # Título de la ventana

# Tamaño de la ventana
window_width = 900
window_height = 600

# Calculamos la posición para que la ventana aparezca centrada en la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Aplicamos tamaño y posición
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.configure(bg="black")  # Fondo negro
root.resizable(True, True)  # Se puede cambiar el tamaño

# Título grande en la parte superior
tk.Label(root, text="Generador de Contraseñas", font=("Courier", 18, "bold"), bg="black", fg="#00ff00").pack(pady=15)

# Sección donde están los controles (entrada y botones)
controls_card = tk.Frame(root, bg="black")
controls_card.pack(fill="x", padx=30, pady=5)

# Texto y caja para escribir cuántas contraseñas queremos
tk.Label(controls_card, text="Número de contraseñas:", bg="black", fg="#00ff00", font=("Courier", 12)).pack(side="left", padx=5)
entry_num = tk.Entry(controls_card, width=5, bg="black", fg="#00ff00", insertbackground="#00ff00", font=("Courier", 12))
entry_num.pack(side="left", padx=5)

# Botones con sus funciones
buttons = [
    ("Generar", generar_contrasenas),
    ("Copiar todas", copiar_todas),
    ("Exportar a .txt", exportar)
]

# Creamos los botones y les añadimos el efecto de color al pasar el ratón
for text, command in buttons:
    btn = tk.Button(controls_card, text=text, width=15, bg="black", fg="#00ff00", font=("Courier", 12), relief="flat", command=command)
    btn.pack(side="left", padx=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Línea verde decorativa debajo de los botones
separator = tk.Frame(root, bg="#00ff00", height=2)
separator.pack(fill="x", padx=30, pady=(0,10))

# Área donde se muestran las contraseñas generadas
text_frame = tk.Frame(root, bg="black")
text_frame.pack(fill="both", expand=True, padx=30, pady=10)

# Caja de texto para mostrar las contraseñas
text_area = tk.Text(text_frame, font=("Courier", 14), bg="black", fg="#00ff00", insertbackground="#00ff00",
                    wrap="none", bd=0)
text_area.grid(row=0, column=0, sticky="nsew")

# Barra para desplazarse si hay muchas contraseñas
scrollbar = tk.Scrollbar(text_frame, command=text_area.yview, bg="black", activebackground="#00ff00")
scrollbar.grid(row=0, column=1, sticky="ns")
text_area.config(yscrollcommand=scrollbar.set)

# Ajustes para que el área de texto se expanda correctamente
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

# Lista donde se guardan las contraseñas generadas
lista_contrasenas = []

# Iniciamos el programa
root.mainloop()
