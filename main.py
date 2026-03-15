import tkinter as tk
from app.table import truth_table

def truth_tables_cons(text):
    text = text.strip()
    output_text.insert(tk.END, f"Procesando: {text}\n\n")
    output_text.insert(tk.END, truth_table(text))
    output_text.insert(tk.END, "\n")
    output_text.see(tk.END)

def send_text():
    entrada = input_text.get()
    if entrada.strip():
        truth_tables_cons(entrada)
        input_text.delete(0, tk.END)

def insert_caracter(char):
    pos = input_text.index(tk.INSERT)
    input_text.insert(pos, char)

root = tk.Tk()
root.title("Truth Tables")
root.geometry("800x530")

help_label = tk.Label(root, text="Generador de Tablas de Verdad", bg="lightgrey", fg="black", font=("Arial", 12), anchor="w", justify="left")
help_label.pack(fill="x", padx=5, pady=5)


output_text = tk.Text(root, height=20, width=80, bg="black", font=("Consolas", 12), fg="white", insertbackground="white")
output_text.pack(padx=10, pady=5)

input_text = tk.Entry(root, width=80, bg="black", fg="white", font=("Arial", 12), insertbackground="white")
input_text.pack(padx=10, pady=(0,5))
input_text.bind("<Return>", lambda event: send_text())

special_frame = tk.Frame(root)
special_frame.pack(pady=(0,5))
special_chars = ["∨", "∧", "->", "<->", "~"] 

for char in special_chars:
    btn = tk.Button(special_frame, text=char, width=5, command=lambda c=char: insert_caracter(c))
    btn.pack(side="left", padx=5)


send_button = tk.Button(root, text="Send", command=send_text)
send_button.pack(pady=(0,10))

root.mainloop()