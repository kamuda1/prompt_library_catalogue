import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FileBrowserApp:
    def __init__(self, master):
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

        # similarity button
        self.similarity_button = ttk.Button(self.file_list_frame, text="Order by similarity",
                                            command=self.order_files_by_similarity)
        self.similarity_button.pack(side=tk.BOTTOM)

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

    def load_content_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            filename, file_extension = os.path.splitext(file_path)
            if file_extension == '.json':
                content_json = json.load(file)
                content = content_json['nodes'][0]['text']
            else:
                content = file.read()
        return content

    def display_file_content(self, event):
        selection = event.widget.curselection()
        if not selection:
            return

        file_name = event.widget.get(selection[0])
        file_path = os.path.join(self.directory, file_name)

        content = self.load_content_from_file(file_path)

        self.file_content.delete(1.0, tk.END)
        self.file_content.insert(tk.INSERT, content)

    def order_files_by_similarity(self):
        # Get the selected file's content
        selected_file_index = self.file_list.curselection()
        if not selected_file_index:
            return

        selected_file = self.file_list.get(selected_file_index)
        selected_file_path = os.path.join(self.directory, selected_file)

        with open(selected_file_path, 'r', encoding='utf-8') as file:
            selected_file_content = file.read()

        # Load contents of all files in the directory
        file_contents = []
        file_names = self.file_list.get(0, tk.END)

        for file_name in file_names:
            file_path = os.path.join(self.directory, file_name)
            content = self.load_content_from_file(file_path)
            file_contents.append(content)

        # Calculate similarity using TfidfVectorizer and cosine_similarity
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([selected_file_content] + file_contents)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

        # Sort files by similarity
        sorted_files = sorted(zip(file_names, similarity_scores), key=lambda x: x[1], reverse=True)
        self.file_list.delete(0, tk.END)
        for file, _ in sorted_files:
            self.file_list.insert(tk.END, file)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileBrowserApp(root)
    root.mainloop()
