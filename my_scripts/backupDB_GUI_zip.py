# D:\PythonProject\WebPagesParsing\my_scripts\backupDB_GUI_zip.py

import os
import shutil
import zipfile
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import pyperclip
import subprocess
import sys

def sanitize_filename(s):
    return "".join(c for c in s if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')

def backup_db(db_path, comment, backup_folder, archive=False):
    if not os.path.exists(db_path):
        return False, f"Файл базы данных не найден:\n{db_path}"

    os.makedirs(backup_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    base_name = f'db_backup_{timestamp}'
    backup_file = os.path.join(backup_folder, f'{base_name}.sqlite3')

    try:
        shutil.copy(db_path, backup_file)

        if comment.strip():
            log_file = os.path.join(backup_folder, f'{base_name}.txt')
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(comment.strip() + '\n')

        if archive:
            zip_path = os.path.join(backup_folder, f'{base_name}.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(backup_file, arcname=os.path.basename(backup_file))
                if comment.strip():
                    zipf.writestr("comment.txt", comment.strip())
            os.remove(backup_file)
            if comment.strip():
                os.remove(log_file)
            return True, f"\u2705 Копия заархивирована:\n{zip_path}"
        else:
            return True, f"\u2705 Копия создана:\n{backup_file}"

    except Exception as e:
        return False, f'\u274C Ошибка: {e}'

def load_existing_backups(backup_folder):
    items = []
    for fname in sorted(os.listdir(backup_folder), reverse=True):
        if fname.endswith(".sqlite3") or fname.endswith(".zip"):
            base = os.path.splitext(fname)[0]
            file_path = os.path.join(backup_folder, fname)
            comment = ""

            if fname.endswith(".zip"):
                try:
                    with zipfile.ZipFile(file_path, 'r') as zipf:
                        if "comment.txt" in zipf.namelist():
                            with zipf.open("comment.txt") as f:
                                comment = f.read().decode("utf-8").strip()
                except Exception:
                    comment = "(ошибка чтения комментария)"
            else:
                txt_path = os.path.join(backup_folder, base + ".txt")
                if os.path.exists(txt_path):
                    with open(txt_path, encoding="utf-8") as f:
                        comment = f.read().strip()

            items.append((base, file_path, None, comment))
    return items

def launch_gui():
    def select_db():
        path = filedialog.askopenfilename(title="Выберите базу данных", filetypes=[("SQLite", "*.sqlite3"), ("Все файлы", "*.*")])
        if path:
            db_path_var.set(path)

    def run_backup():
        db_path = db_path_var.get().strip()
        comment = comment_entry.get("1.0", tk.END).strip()
        archive = archive_var.get()

        success, message = backup_db(db_path, comment, backup_folder, archive)
        messagebox.showinfo("Результат", message)
        if success:
            comment_entry.delete("1.0", tk.END)
            refresh_backup_list()

    def refresh_backup_list():
        backup_listbox.delete(0, tk.END)
        backup_map.clear()

        for base, file_path, _, comment in load_existing_backups(backup_folder):
            display = f"{os.path.basename(file_path)} — {comment}" if comment else os.path.basename(file_path)
            backup_listbox.insert(tk.END, display)
            backup_map[base] = file_path

    def copy_selected_path():
        selection = backup_listbox.curselection()
        if selection:
            selected = backup_listbox.get(selection[0])
            base = selected.split(" — ")[0].replace(".sqlite3", "").replace(".zip", "")
            file_path = backup_map.get(base, None)
            if file_path:
                pyperclip.copy(file_path)
                messagebox.showinfo("Скопировано", f"Путь скопирован:\n{file_path}")
        else:
            messagebox.showwarning("Выбор", "Выберите файл из списка.")

    def delete_selected():
        selection = backup_listbox.curselection()
        if not selection:
            messagebox.showwarning("Выбор", "Выберите копию для удаления.")
            return

        selected = backup_listbox.get(selection[0])
        base = selected.split(" — ")[0].replace(".sqlite3", "").replace(".zip", "")
        file_path = backup_map.get(base, None)

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Ошибка", "Файл не найден.")
            return

        confirm = messagebox.askyesno("Удаление", f"Удалить файл:\n{os.path.basename(file_path)}?")
        if confirm:
            try:
                os.remove(file_path)
                messagebox.showinfo("Удалено", "Файл удалён.")
                refresh_backup_list()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")

    def open_in_explorer():
        selection = backup_listbox.curselection()
        if not selection:
            messagebox.showwarning("Выбор", "Выберите копию из списка.")
            return

        selected = backup_listbox.get(selection[0])
        base = selected.split(" — ")[0].replace(".sqlite3", "").replace(".zip", "")
        file_path = backup_map.get(base, None)

        if file_path and os.path.exists(file_path):
            try:
                subprocess.run(['explorer', '/select,', file_path.replace('/', '\\')])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть проводник:\n{e}")
        else:
            messagebox.showerror("Ошибка", "Файл не найден.")

    def confirm_exit():
        if messagebox.askyesno("Выход", "Вы точно хотите выйти?"):
            root.destroy()
            sys.exit()

    root = tk.Tk()
    root.title("Резервное копирование БД")
    root.geometry("520x720")

    backup_folder = os.path.join(os.path.dirname(__file__), "backup_folder")
    os.makedirs(backup_folder, exist_ok=True)
    backup_map = {}

    tk.Label(root, text="Путь к базе данных:").pack(anchor="w", padx=10, pady=(10, 0))
    db_path_var = tk.StringVar(value=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')))
    tk.Entry(root, textvariable=db_path_var).pack(fill="x", padx=10)
    tk.Button(root, text="Выбрать файл...", command=select_db, bg="#000080", fg="white").pack(padx=10, pady=5)

    tk.Label(root, text="Комментарий к резервной копии:").pack(anchor="w", padx=10)
    comment_entry = ScrolledText(root, height=4)
    comment_entry.pack(fill="x", padx=10, pady=5)

    archive_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Архивировать копию (.zip)", variable=archive_var).pack(anchor="w", padx=12, pady=5)

    tk.Button(root, text="Создать резервную копию", command=run_backup, bg="#800040", fg="white").pack(padx=10, pady=10)

    tk.Label(root, text="Сохранённые резервные копии:").pack(anchor="w", padx=10)
    backup_listbox = tk.Listbox(root, height=12)
    backup_listbox.pack(fill="both", expand=True, padx=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="📂 Открыть в проводнике", command=open_in_explorer, bg="#F2B600", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="📋 Скопировать путь", command=copy_selected_path, bg="#008000", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="🗑️ Удалить копию", command=delete_selected, bg="#e53935", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="🚪 Выход", command=confirm_exit, bg="#0000FF", fg="white").pack(side="left", padx=5)

    root.protocol("WM_DELETE_WINDOW", confirm_exit)
    refresh_backup_list()
    root.mainloop()

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("Установите pyperclip: pip install pyperclip")
    else:
        launch_gui()
