from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import Toplevel
from tkscrolledframe import ScrolledFrame


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.label_datas = []
        self.width = 800
        self.height = 600
        self.data = []
        self.file_path = ''
        self.filter_entries = []

        self.sf = ScrolledFrame(self, width=self.width, height=self.height)
        self.sf.bind_arrow_keys(self)
        self.sf.bind_scroll_wheel(self)

        self.text_box = self.sf.display_widget(Frame)
        self.button_box = ttk.Frame(self)
        self.datas_name_box = ttk.Frame(self)

        open_button = ttk.Button(self.button_box, text='Open', command=self.open_database, padding=5)
        refresh_button = ttk.Button(self.button_box, text='Refresh', command=self.re_open_database, padding=5)
        filter_button = ttk.Button(self.button_box, text='Filter', command=self.filter, padding=5)
        settings_button = ttk.Button(self.button_box, text='Settings', command=self.settings, padding=5)
        self.database_condition = Label(self.button_box, text='Please Open Database', fg='red')

        open_button.grid(row=0, column=0, padx=4, pady=0)
        refresh_button.grid(row=0, column=1, padx=4, pady=0)
        filter_button.grid(row=0, column=2, padx=4, pady=0)
        settings_button.grid(row=0, column=3, padx=4, pady=0)
        self.database_condition.grid(row=0, column=4, padx=10, pady=0)

        self.button_box.grid(row=0, column=0, sticky='w')
        self.datas_name_box.grid(row=1, column=0, sticky='w')
        self.sf.grid(row=2, column=0, columnspan=2)

        self.geometry(f'{self.width}x{self.height}+200+100')
        self.title('ARTSQL DataBase Browser')
        self.bind("<Configure>", self.on_resize)

    def open_database(self):
        self.file_path = filedialog.askopenfilename(title='Open file', filetypes=(("ARTSQL database", "*.artsql"),))
        if self.file_path != '':
            self.data = []
            with open(self.file_path, 'r') as f:
                for row in f:
                    data = row.strip().split(';')
                    data.pop()
                    self.data.append(data)
            self.write_data(self.data)
            self.database_condition.config(text='Database Opened', fg='green')

    def re_open_database(self):
        if self.file_path != '':
            self.data = []
            with open(self.file_path, 'r') as f:
                for row in f:
                    data = row.strip().split(';')
                    data.pop()
                    self.data.append(data)
            self.write_data(self.data)
            self.database_condition.config(text='Successful Reloaded', fg='orange')

    def write_data(self, data):
        for item in self.label_datas:
            item.grid_forget()
            item.destroy()
        self.label_datas = []
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                label = ttk.Label(self.text_box, text=val, borderwidth=2, relief="solid", padding=4, font=('Arial', 16))
                label.grid(row=i, column=j, sticky="nsew")
                self.label_datas.append(label)

    def on_resize(self, event):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.sf.configure(width=self.width-20, height=self.height-55)

    def filter(self):
        if self.file_path != '':
            filter_window = Toplevel()
            filter_window.geometry('400x400+200+200')
            filter_window.resizable(width=False, height=False)
            filter_window.title('Filter')
            filter_window.transient(self)
            filter_window.grab_set()

            s_filter = ScrolledFrame(filter_window, width=380, height=345)
            s_filter.bind_arrow_keys(filter_window)
            s_filter.bind_scroll_wheel(filter_window)

            filter_box = s_filter.display_widget(Frame)
            s_filter.pack(fill=BOTH, expand=True)
            for i, item in enumerate(self.data[0]):
                frame = ttk.Frame(filter_box)
                Label(frame, text=item, width=25).grid(row=i, column=0)
                entry = Entry(frame, width=25)
                entry.grid(row=i, column=1)
                self.filter_entries.append(entry)
                frame.grid(row=i, column=0, pady=4)

            collect_button = ttk.Button(filter_box, text='Filter', command=self.filter_now)
            collect_button.grid()

        else:
            self.database_condition.configure(text='Please Open Database', fg='red', font=('Arial', 14))


    def filter_now(self):
        print(f'{self.filter_entries} data, type: {type(self.filter_entries)}')
        datas = []
        for i, item in self.filter_entries:
            datas.append(item.get())
        print(datas, self.filter_entries)
    def settings(self):
        pass

app = Window()

app.mainloop()