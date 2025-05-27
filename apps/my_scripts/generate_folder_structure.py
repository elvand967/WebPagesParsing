# D:\PythonProject\WebPagesParsing\apps\my_scripts\generate_folder_structure.py

'''
🗂 GUI-скрипт для генерации отчёта по структуре каталогов с исключениями
'''

import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

def print_tree(path, exclusions, prefix="", is_last=True, output_lines=None):
    if output_lines is None:
        output_lines = []

    abs_path = os.path.abspath(path)
    if abs_path in exclusions:
        return output_lines

    name = os.path.basename(path)
    if name == "":
        output_lines.append(abs_path.upper())
    else:
        connector = "\\---" if is_last else "+---"
        output_lines.append(f"{prefix}{connector}{name}")

    new_prefix = prefix + ("    " if is_last else "|   ")

    try:
        entries = [e for e in os.listdir(path)]
    except PermissionError:
        return output_lines

    entries = [e for e in entries if os.path.abspath(os.path.join(path, e)) not in exclusions]

    dirs = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(path, e))]

    for i, file in enumerate(files):
        is_last_file = (i == len(files) - 1) and (len(dirs) == 0)
        file_connector = "\\---" if is_last_file else "+---"
        output_lines.append(f"{new_prefix}{file_connector}{file}")

    for i, directory in enumerate(dirs):
        is_last_dir = (i == len(dirs) - 1)
        print_tree(os.path.join(path, directory), exclusions, new_prefix, is_last_dir, output_lines)

    return output_lines

def generate_tree_report(base_path, exclusions, output_file):
    lines = print_tree(base_path, exclusions)
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")
    return lines

def launch_gui():
    def select_folder():
        path = filedialog.askdirectory()
        if path:
            base_path_var.set(path)
            abs_base = os.path.abspath(path)
            for excl in default_exclusions:
                full_path = os.path.join(abs_base, excl)
                if os.path.exists(full_path) and full_path not in exclusions:
                    exclusions.append(full_path)
                    exclusions_listbox.insert(tk.END, full_path)
            refresh_explorer(path)

    def add_exclusion():
        base_path = base_path_var.get()
        if not base_path:
            messagebox.showwarning("Ошибка", "Сначала выберите базовую директорию.")
            return

        excl_path = filedialog.askdirectory(initialdir=base_path, title="Выберите папку для исключения")
        if not excl_path:
            excl_path = filedialog.askopenfilename(initialdir=base_path, title="Выберите файл для исключения")

        if excl_path:
            abs_path = os.path.abspath(excl_path)
            if abs_path not in exclusions:
                exclusions.append(abs_path)
                exclusions_listbox.insert(tk.END, abs_path)

    def enter_exclusion_manually():
        path = simpledialog.askstring("Путь вручную", "Введите полный путь к файлу или папке:")
        if path:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path) and abs_path not in exclusions:
                exclusions.append(abs_path)
                exclusions_listbox.insert(tk.END, abs_path)

    def remove_exclusion():
        selection = exclusions_listbox.curselection()
        if selection:
            index = selection[0]
            exclusions.pop(index)
            exclusions_listbox.delete(index)

    def generate():
        base_path = base_path_var.get()
        if not base_path:
            messagebox.showwarning("Ошибка", "Выберите папку.")
            return
        output = "folder_structure.py.txt"
        lines = generate_tree_report(base_path, exclusions, output)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "\n".join(lines))
        messagebox.showinfo("Готово", f"Файл '{output}' создан.")

    def refresh_explorer(path):
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Выбран путь: {path}\n")

    root = tk.Tk()
    root.title("Дерево каталогов с исключениями")
    root.geometry("800x600")

    default_exclusions = ['.idea', '.venv', '.git']
    exclusions = []

    tk.Label(root, text="Рабочая директория:").pack(anchor="w", padx=10, pady=(10, 0))
    base_path_var = tk.StringVar()
    tk.Entry(root, textvariable=base_path_var).pack(fill="x", padx=10)
    tk.Button(root, text="Выбрать папку", command=select_folder).pack(padx=10, pady=5)

    tk.Label(root, text="Исключения (абсолютные пути):").pack(anchor="w", padx=10)
    exclusions_frame = tk.Frame(root)
    exclusions_frame.pack(fill="x", padx=10)

    exclusions_listbox = tk.Listbox(exclusions_frame, height=6)
    exclusions_listbox.pack(side="left", fill="x", expand=True)

    tk.Button(exclusions_frame, text="+", width=3, command=add_exclusion).pack(side="left", padx=2)
    tk.Button(exclusions_frame, text="✍️", width=3, command=enter_exclusion_manually).pack(side="left", padx=2)
    tk.Button(exclusions_frame, text="-", width=3, command=remove_exclusion).pack(side="left")

    tk.Button(root, text="Создать файл отчёта", command=generate, bg="#4CAF50", fg="white").pack(pady=10)

    output_text = ScrolledText(root, height=20)
    output_text.pack(fill="both", expand=True, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()