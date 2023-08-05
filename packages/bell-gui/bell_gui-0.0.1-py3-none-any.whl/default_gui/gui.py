import tkinter as tk
from tkinter import filedialog as fd


def select_path(entry):
    """
    Selects dir path and adds it to the entry.
    """
    def select():
        path = fd.askdirectory()
        entry.delete(0, 'end')
        entry.insert(0, path)
    return select


def select_file(entry):
    """
    Selects file path and adds it to the entry.
    """
    def select():
        path = fd.askopenfilename()
        entry.delete(0, 'end')
        entry.insert(0, path)
    return select


class Form:
    """
    Simple default from for getting user input. Accepts text, file paths and dir paths.
    """

    def __init__(self, fields, button_text, trigger):
        self.field_names = fields
        self.button_text = button_text
        self.trigger = trigger
        self.window = None

    def _make_field(self, name, pos, field_type):
        field_name = tk.Label(text=name)
        entry = tk.Entry(width=100)
        field_name.grid(row=pos, column=0)
        entry.grid(row=pos, column=1)
        if field_type == 'dir_path':
            path_button = tk.Button(text='↪', command=select_path(entry))
            path_button.grid(row=pos, column=2)
        elif field_type == 'file_path':
            path_button = tk.Button(text='↪', command=select_file(entry))
            path_button.grid(row=pos, column=2)
        return name, entry

    def _get_fields(self):
        result = {n: e.get() for n, e in self.fields.items()}
        self.window.destroy()
        self.trigger(result)

    def run(self):
        """
        Run the window until trigger functon is called via button
        """
        self.window = tk.Tk()
        self.window.title('Input')

        fields = [
            self._make_field(
                name, pos, typ) for pos, (name, typ) in enumerate(
                self.field_names)]
        fields = {n: e for n, e in fields}
        self.fields = fields

        button = tk.Button(
            text=self.button_text,
            command=self._get_fields)
        button.grid(row=len(fields), column=0)

        self.window.mainloop()
