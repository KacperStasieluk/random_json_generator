import json
import os
import random
import string

import tkinter as tk
from tkinter import filedialog, messagebox


def generate_random_json_value(depth=0):
    """
    Generate a random JSON value with controlled recursion depth.
    """
    if depth == 0:
        return {generate_random_json_key(): generate_random_json_value(depth + 1) for _ in range(2)}
    elif depth > 3:
        return generate_simple_value()

    data_type = random.choice(['int', 'float', 'str', 'list', 'dict'])

    if data_type in ['int', 'float', 'str']:
        return generate_simple_value(data_type)
    elif data_type == 'list':
        return [generate_random_json_value(depth + 1) for _ in range(random.randint(2, 5))]
    elif data_type == 'dict':
        return {generate_random_json_key(): generate_random_json_value(depth + 1) for _ in range(random.randint(2, 5))}

def generate_simple_value(data_type=None):
    """
    Generate a simple random value (int, float, or string).
    """
    if data_type == 'int':
        return random.randint(1, 100)
    elif data_type == 'float':
        return round(random.uniform(1.0, 100.0), 2)
    elif data_type == 'str':
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))
    else:
        return random.choice([random.randint(1, 100), round(random.uniform(1.0, 100.0), 2),
                              ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))])

def generate_random_json_key():
    """
    Generate a random string - will be used as a key in JSON dictionary.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15)))

def create_json_files(n, path, f_name):
    """
    Create n JSON files with random content.
    """
    path = (path + '/') if path else ''
    for i in range(n):
        json_data = generate_random_json_value()
        file_name = f'{path}{f_name}_{i+1}.json'
        try:
            with open(file_name, 'w') as file:
                json.dump(json_data, file, indent=4)
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while creating {file_name}: {e}')
            continue

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.path_label = tk.Label(self, text='Path:')
        self.path_label.grid(row=0, column=0, sticky='w', padx=5)

        self.path_entry = tk.Entry(self, width=50)
        self.path_entry.grid(row=0, column=1, sticky='ew', padx=5)
        current_directory = os.getcwd()
        self.path_entry.insert(0, current_directory)

        self.path_button = tk.Button(self, text='Choose...', command=self.browse_folder)
        self.path_button.grid(row=0, column=2, padx=5, pady=5)

        self.name_label = tk.Label(self, text='JSON file name:')
        self.name_label.grid(row=1, column=0, sticky='w', padx=5)

        self.name_entry = tk.Entry(self, width=50)
        self.name_entry.grid(row=1, column=1, sticky='ew', padx=5)
        self.name_entry.insert(0, 'random_json')

        self.number_label = tk.Label(self, text='Number of JSON files:')
        self.number_label.grid(row=2, column=0, sticky='w', padx=5)

        self.number_entry = tk.Spinbox(self, from_=1, to=10000, width=10)
        self.number_entry.grid(row=2, column=1, sticky='ew', padx=5)

        self.generate_button = tk.Button(self, text='Generate', command=self.generate)
        self.generate_button.grid(row=2, column=2, padx=5, pady=5)

    def browse_folder(self):
        directory = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, directory)

    def generate(self):
        path = self.path_entry.get()
        f_name = self.name_entry.get()
        try:
            num_files = int(self.number_entry.get())
            filenames = create_json_files(num_files, path, f_name)
            messagebox.showinfo('Success', f'Successfully created {num_files} JSON files in {path}')
        except ValueError:
            messagebox.showerror('Error', 'The number of files must be an integer.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

root = tk.Tk()
root.geometry('550x100')
root.title('Random JSON Generator')
root.resizable(False, False)
app = Application(master=root)
app.mainloop()
