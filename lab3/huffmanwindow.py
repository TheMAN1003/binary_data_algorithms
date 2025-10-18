import tkinter as tk
import os
import struct
from tkinter import messagebox
from huffman import count_frequencies, huffman_tree, code_table, BitStream

window = tk.Tk()
window.title("Кодер/Декодер Хаффмана")
window.geometry("650x300")

main_frame = tk.Frame(window)
main_frame.pack(pady=10)

encoder_frame = tk.LabelFrame(main_frame, text="Стиснення")
encoder_frame.grid(row=0, column=0, padx=10, pady=10)

tk.Label(encoder_frame, text="Вхідний файл кодера").grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_input_enc = tk.Entry(encoder_frame, width=40)
entry_input_enc.grid(row=0, column=1, padx=5, pady=5)

tk.Label(encoder_frame, text="Вихідний файл кодера (опціонально)").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_output_enc = tk.Entry(encoder_frame, width=40)
entry_output_enc.grid(row=1, column=1, padx=5, pady=5)

def encode_file_huffman():
    input_file = entry_input_enc.get().strip()
    output_file = entry_output_enc.get().strip()
    
    if not input_file:
        messagebox.showerror("Помилка", "Будь ласка, введіть назву вхідного файлу.")
        return
    
    if not output_file:
        name, _ = os.path.splitext(input_file)
        output_file = name + ".huf" 

    try:
        with open(input_file, "rb") as f:
            data = f.read()
        
        original_length = len(data)

        if original_length > (1<<32):
            messagebox.showerror("Помилка", "Розмір вхідного файлу завеликий.")
            return

        frequencies = count_frequencies(data)
        root = huffman_tree(frequencies)
        code_tbl = code_table(root)
        
        bs = BitStream(output_file)
        bs.encode_bit_sequence(data, code_tbl, frequencies)
        del bs
        
        messagebox.showinfo("Перемога", f"Успішно закодовано файл {input_file} (Довжина: {original_length} байтів) у {output_file}")
        
    except FileNotFoundError:
        messagebox.showerror("Помилка", f"Файл не знайдено: {input_file}")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

encoder_button = tk.Button(encoder_frame, text="Закодувати", command=encode_file_huffman, bg="lightblue")
encoder_button.grid(row=2, column=1, padx=5, pady=5, sticky='e')


decoder_frame = tk.LabelFrame(main_frame, text="Розпакування")
decoder_frame.grid(row=1, column=0, padx=10, pady=10)

tk.Label(decoder_frame, text="Вхідний файл декодера").grid(row=0, column=0, padx=5, pady=5, sticky='w')
entry_input_dec = tk.Entry(decoder_frame, width=40)
entry_input_dec.grid(row=0, column=1, padx=5, pady=5)

tk.Label(decoder_frame, text="Вихідний файл декодера").grid(row=1, column=0, padx=5, pady=5, sticky='w')
entry_output_dec = tk.Entry(decoder_frame, width=40)
entry_output_dec.grid(row=1, column=1, padx=5, pady=5)

def decode_file_huffman():
    input_file = entry_input_dec.get().strip()
    output_file = entry_output_dec.get().strip()
    
    if not input_file:
        messagebox.showerror("Помилка", "Будь ласка, введіть назву вхідного файлу.")
        return
    if not output_file:
        messagebox.showerror("Помилка", "Будь ласка, введіть назву вихідного файлу.")
        return

    try:
        with open(input_file, "rb") as input_read_f:
            fulldata = input_read_f.read()

        FREQ_TABLE_SIZE = 1024
        LENGTH_SIZE = 8
        HEADER_SIZE = FREQ_TABLE_SIZE + LENGTH_SIZE
        
        if len(fulldata) < HEADER_SIZE:
             raise ValueError("Вхідний файл занадто малий, або пошкоджений.")

        freq_bytes = fulldata[:FREQ_TABLE_SIZE]
        length_bytes = fulldata[FREQ_TABLE_SIZE : HEADER_SIZE]
        data_to_decode = fulldata[HEADER_SIZE:]

        original_length = struct.unpack('>Q', length_bytes)[0]
        
        root = huffman_tree(freq_bytes)
        code_tbl = code_table(root)
        bs = BitStream(output_file)
        bs.decode_bit_sequence(data_to_decode, code_tbl, original_length)
        del bs
        
        messagebox.showinfo("Перемога", f"Успішно декодовано файл {input_file} у {output_file}")
        
    except FileNotFoundError:
        messagebox.showerror("Помилка", f"Файл не знайдено: {input_file}")
    except struct.error:
         messagebox.showerror("Помилка", "Некоректний формат довжини файлу в заголовку.")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

decoder_button = tk.Button(decoder_frame, text="Декодувати", command=decode_file_huffman, bg="lightblue")
decoder_button.grid(row=2, column=1, padx=5, pady=5, sticky='e')

window.mainloop()