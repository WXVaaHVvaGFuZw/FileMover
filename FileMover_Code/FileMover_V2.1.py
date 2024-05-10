import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class FileMoverApp:
    def __init__(self, master):
        self.master = master
        master.title("FileMover_V2.1")

        # 创建菜单栏
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        # 文件菜单
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=master.quit)

        # 设置菜单
        self.setting_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Setting", menu=self.setting_menu)
        self.setting_var = tk.StringVar()
        self.setting_var.set(r"D:\桌面")
        self.setting_menu.add_command(label="Set Source Path", command=self.select_setting_path)

        # 其他代码与之前相同
        self.common_frame = tk.LabelFrame(master, text="Common File", padx=10, pady=10)
        self.common_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.common_checkboxes = []
        self.common_extensions = {
            "Word": [".doc", ".docx"],
            "Excel": [".xls", ".xlsx"],
            "PPT": [".ppt", ".pptx"],
            "Text": [".txt"],
            "Image": [".png", ".jpg", ".jpeg", ".gif"],
            "Video": [".mp4"]
        }
        for row, (file_type, extensions) in enumerate(self.common_extensions.items(), start=1):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.common_frame, text=file_type, variable=var)
            checkbox.grid(row=row, column=0, sticky="w")
            self.common_checkboxes.append((var, extensions))

        self.common_select_all_var = tk.IntVar()
        self.common_select_all_checkbox = tk.Checkbutton(self.common_frame, text="Select All", variable=self.common_select_all_var, command=self.toggle_common_checkboxes)
        self.common_select_all_checkbox.grid(row=0, column=1, sticky="e")

        # Code File Section
        self.code_frame = tk.LabelFrame(master, text="Code File", padx=10, pady=10)
        self.code_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.code_checkboxes = []
        self.code_extensions = {
            "C": [".c"],
            "C++": [".cpp"],
            "Python": [".py"],
            "HTML": [".html"],
            "CSS": [".css"],
            "JavaScript": [".js"]
        }
        for row, (file_type, extensions) in enumerate(self.code_extensions.items(), start=1):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.code_frame, text=file_type, variable=var)
            checkbox.grid(row=row, column=0, sticky="w")
            self.code_checkboxes.append((var, extensions))

        self.code_select_all_var = tk.IntVar()
        self.code_select_all_checkbox = tk.Checkbutton(self.code_frame, text="Select All", variable=self.code_select_all_var, command=self.toggle_code_checkboxes)
        self.code_select_all_checkbox.grid(row=0, column=1, sticky="e")

        # Move Path Section
        self.move_path_frame = tk.Frame(master)
        self.move_path_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.move_path_frame, text="Select DEST Path", command=self.select_path).grid(row=0, column=0, padx=(0, 10))
        self.path_var = tk.StringVar()
        self.path_var.set("E:")
        self.path_entry = tk.Entry(self.move_path_frame, textvariable=self.path_var)
        self.path_entry.grid(row=0, column=1, padx=(0, 10))
        tk.Button(self.move_path_frame, text="Move Files", command=self.move_files).grid(row=0, column=2)

    def toggle_common_checkboxes(self):
        select_all = self.common_select_all_var.get()
        for var, _ in self.common_checkboxes:
            var.set(select_all)

    def toggle_code_checkboxes(self):
        select_all = self.code_select_all_var.get()
        for var, _ in self.code_checkboxes:
            var.set(select_all)

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def move_files(self):
        source_path = self.setting_var.get()
        destination_path = self.path_var.get()
        moved_files_count = 0

        for var, extensions in self.common_checkboxes:
            if var.get() == 1:
                folder_name = [key for key, value in self.common_extensions.items() if value == extensions][0]
                moved_files_count += self.move_files_by_extension(source_path, destination_path, extensions, folder_name)

        for var, extensions in self.code_checkboxes:
            if var.get() == 1:
                folder_name = [key for key, value in self.code_extensions.items() if value == extensions][0]
                moved_files_count += self.move_files_by_extension(source_path, destination_path, extensions, folder_name)

        if moved_files_count == 0:
            messagebox.showinfo("FileMover", "No files to move.")
        else:
            messagebox.showinfo("FileMover", f"{moved_files_count} files moved successfully.")

    def move_files_by_extension(self, source_path, destination_path, extensions, folder_name):
        self.create_folder_if_not_exists(os.path.join(destination_path, folder_name))
        moved_files_count = 0
        for file in os.listdir(source_path):
            if any(file.endswith(ext) for ext in extensions):
                shutil.move(os.path.join(source_path, file), os.path.join(destination_path, folder_name, file))
                moved_files_count += 1
        return moved_files_count

    def create_folder_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def select_setting_path(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Setting")

        path_frame = tk.Frame(new_window)
        path_frame.pack(padx=10, pady=10)

        tk.Label(path_frame, text="Source Path:").pack(side=tk.LEFT)
        path_entry = tk.Entry(path_frame)
        path_entry.pack(side=tk.LEFT)
        path_entry.insert(0, self.setting_var.get())

        tk.Button(path_frame, text="OK", command=lambda: self.set_path_and_close_window(new_window, path_entry.get())).pack(side=tk.LEFT)

    def set_path_and_close_window(self, window, path):
        self.setting_var.set(path)
        window.destroy()

root = tk.Tk()
app = FileMoverApp(root)
root.mainloop()