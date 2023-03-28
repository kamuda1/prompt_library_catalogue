import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class FileBrowserApp:
    print('In the class')
    def __init__(self, master):
        print('In the init block')
        self.master = master
        self.master.title("File Browser")

        # Create a frame for the file list
        self.file_list_frame = ttk.Frame(self.master)
        self.file_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and a listbox for the file list
        self.file_list_scrollbar = ttk.Scrollbar(self.file_list_frame)
        self.file_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list = tk.Listbox(self.file_list_frame, yscrollcommand=self.file_list_scrollbar.set)
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_list_scrollbar.config(command=self.file_list.yview)
        self.file_list.bind('<<ListboxSelect>>', self.display_file_content)

        # Create a frame for the file content
        self.file_content_frame = ttk.Frame(self.master)
        self.file_content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and a text widget for the file content
        self.file_content_scrollbar = ttk.Scrollbar(self.file_content_frame)
        self.file_content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_content = tk.Text(self.file_content_frame, wrap=tk.WORD,
                                    yscrollcommand=self.file_content_scrollbar.set)
        self.file_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_content_scrollbar.config(command=self.file_content.yview)
        self.load_directory_contents()

    def load_directory_contents(self):
        directory = filedialog.askdirectory()
        if not directory:
            return

        file_list = sorted(os.listdir(directory))
        for file in file_list:
            if os.path.isfile(os.path.join(directory, file)):
                self.file_list.insert(tk.END, file)

        self.directory = directory

    def display_file_content(self, event):
        selection = event.widget.curselection()
        if not selection:
            return

        file_name = event.widget.get(selection[0])
        file_path = os.path.join(self.directory, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        self.file_content.delete(1.0, tk.END)
        self.file_content.insert(tk.INSERT, content)


if __name__ == "__main__":
    print('in the main block')
    root = tk.Tk()
    app = FileBrowserApp(root)
    root.mainloop()
