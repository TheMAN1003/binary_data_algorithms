import tkinter as tk
import os
from tkinter import messagebox
from enc import enc
from dec import dec

window = tk.Tk()
window.title("RLE Кодер/Декодер")
window.geometry("600x300")

main_frame = tk.Frame(window)
main_frame.pack()

encoder_frame = tk.LabelFrame(main_frame, text="Кодер")
encoder_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(encoder_frame, text="Вхідний файл кодера").grid(row=0, column=0, padx=5, pady=5)
entry_input = tk.Entry(encoder_frame, width=40)
entry_input.grid(row=0, column=1, padx=5, pady=5)

tk.Label(encoder_frame, text="Вихідний файл кодера (може бути порожній)").grid(row=1, column=0, padx=5, pady=5)
entry_output = tk.Entry(encoder_frame, width=40)
entry_output.grid(row=1, column=1, padx=5, pady=5)

def encode_file():
    input_file = entry_input.get().strip()
    output_file = entry_output.get().strip()
    if not input_file:
        messagebox.showerror("Помилка", "Будь ласка, введіть назву вхідного файлу кодера.")
        return
    if not output_file:
        name, _ = os.path.splitext(input_file)
        output_file = name + ".rle"
    try:
        with open(input_file, "rb") as f:
            data = f.read()
        encoded_text = enc(data)
        with open(output_file, "wb") as f:
            f.write(encoded_text)
        messagebox.showinfo("Перемога", f"Успішно закодовано файл {input_file} у {output_file} використовуючи RLE!")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

encoder_button = tk.Button(encoder_frame, text="Закодувати", command=encode_file, bg="lightblue")
encoder_button.grid(row=2, column=1, padx=5, pady=5)

decoder_frame = tk.LabelFrame(main_frame, text="Декодер")
decoder_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Label(decoder_frame, text="Вхідний файл декодера").grid(row=0, column=0, padx=5, pady=5)
entry_input2 = tk.Entry(decoder_frame, width=40)
entry_input2.grid(row=0, column=1, padx=5, pady=5)

tk.Label(decoder_frame, text="Вихідний файл декодера").grid(row=1, column=0, padx=5, pady=5)
entry_output2 = tk.Entry(decoder_frame, width=40)
entry_output2.grid(row=1, column=1, padx=5, pady=5)

def decode_file():
    input_file = entry_input2.get().strip()
    output_file = entry_output2.get().strip()
    if not input_file:
        messagebox.showerror("Помилка", "Будь ласка, введіть назву вхідного файлу декодера.")
        return
    if not output_file:
        messagebox.showerror("Помилка", "Будь ласка, введіть назву вихідного файлу декодера.")
        return
    try:
        with open(input_file, "rb") as f:
            data = f.read()
        decoded_text = dec(data)
        with open(output_file, "wb") as f:
            f.write(decoded_text)
        messagebox.showinfo("Перемога", f"Успішно декодовано файл {input_file} у {output_file} використовуючи RLE!")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

decoder_button = tk.Button(decoder_frame, text="Декодувати", command=decode_file, bg="lightblue")
decoder_button.grid(row=2, column=1, padx=5, pady=5)

window.mainloop()