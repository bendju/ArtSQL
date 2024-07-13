from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import Toplevel
from tkscrolledframe import ScrolledFrame

class Window(Tk):
    def __init__(self):
        super().__init__()
        # vars
        self.filter_entries = []
        self.file_path = ''
        self.database_index = 0
        self.label_datas = []

        # widget classes
        self.sf = ScrolledFrame(self, width=800, height=600)

        self.button_box = ttk.Frame(self)
        open_button = ttk.Button(self.button_box, text='Open', command=self.open_database, padding=5)
        refresh_button = ttk.Button(self.button_box, text='Refresh', command=self.re_open_database, padding=5)
        filter_button = ttk.Button(self.button_box, text='Filter', command=self.filter, padding=5)
        self.database_condition = Label(self.button_box, text='Please Open Database', fg='red')
        self.select_database_var = IntVar()
        self.select_database = ttk.Combobox(self.button_box, textvariable=self.select_database_var, width=4, state='disabled')

        self.text_box = self.sf.display_widget(Frame)

        # widget places
        self.button_box.grid(row=0, column=0, sticky='w', pady=6)
        self.select_database.grid(row=0, column=0, padx=4, pady=0)
        open_button.grid(row=0, column=1, padx=4, pady=0)
        refresh_button.grid(row=0, column=2, padx=4, pady=0)
        filter_button.grid(row=0, column=3, padx=4, pady=0)
        self.database_condition.grid(row=0, column=4, padx=10, pady=0)

        self.sf.grid(row=2, column=0, columnspan=2)

        # configure
        self.title('ARTSQL DataBase Browser')
        self.bind("<Configure>", self.on_resize)
        self.geometry('800x600+200+100')

        self.select_database.bind('<<ComboboxSelected>>', self.update_database)

        self.sf.bind_arrow_keys(self)
        self.sf.bind_scroll_wheel(self)

        self.select_database['values'] = (1,)
        self.select_database.current(0)

    def open_database(self):
        self.file_path = filedialog.askopenfilename(title='Open file', filetypes=(("ARTSQL Database", "*.artsql"),))
        data = self.get_data()
        current_database = [item for item in data if int(item[0]) == self.select_database_var.get()]
        del_database_index = [item[1:] for item in current_database]
        del_database_index[0].pop(0)
        self.write_data(del_database_index)
        self.database_condition.config(text='Database Opened', fg='green')

    def re_open_database(self):
        data = self.get_data()
        current_database = [item for item in data if int(item[0]) == self.select_database_var.get()]
        del_database_index = [item[1:] for item in current_database]
        del_database_index[0].pop(0)
        self.write_data(del_database_index)
        self.database_condition.config(text='Database Refreshed', fg='orange')

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

            data = self.get_data()
            current_database = [item for item in data if int(item[0]) == self.select_database_var.get()]
            del_database_index = [item[1:] for item in current_database]
            del_database_index[0].pop(0)

            for item in self.filter_entries:
                item.destroy()

            self.filter_entries = []
            for i, item in enumerate(del_database_index[0]):
                frame = ttk.Frame(filter_box)
                Label(frame, text=item, width=25).grid(row=i, column=0)
                entry = Entry(frame, width=25)
                entry.grid(row=i, column=1)
                self.filter_entries.append(entry)
                frame.grid(row=i + 1, column=0, pady=4)

            collect_button = ttk.Button(filter_box, text='Filter', command=self.filter_now)
            collect_button.grid()

    def filter_now(self):
        datas = [f'{data.get()}' for data in self.filter_entries]
        datas_len = len([item for item in datas if item != ''])

        data = self.get_data()
        current_database = [item for item in data if int(item[0]) == self.select_database_var.get()]
        del_database_index = [item[1:] for item in current_database]
        del_database_index.pop(0)

        filtered_data = []
        check_sort = [[] for i in range(len(del_database_index))]

        for i in range(len(del_database_index)):
            for j in range(len(datas)):
                if del_database_index[i][j].lower() == datas[j].lower():
                    check_sort[i].append(1)

        for i, item in enumerate(check_sort):
            if len(item) == datas_len:
                filtered_data.append(del_database_index[i])

        filtered_data.insert(0, current_database[0][2:])
        self.write_data(filtered_data)
    def write_data(self, data):
        # delete undo labels
        for item in self.label_datas:
            item.grid_forget()
            item.destroy()
        # add new labels
        self.label_datas = []
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                label = ttk.Label(self.text_box, text=val, borderwidth=2, relief="solid", padding=4, font=('Arial', 16))
                label.grid(row=i, column=j, sticky="nsew")
                self.label_datas.append(label)

    def get_data(self):
        if self.file_path != '':
            data = []
            self.database_index = 0
            with open(self.file_path, 'r') as f:
                for row in f:
                    datas = row.strip().split(';')
                    datas.pop()
                    data.append(datas)
                    if datas[1] == 'Database':
                        self.database_index += 1

            self.select_database_configure(self.database_index)
            return data

    def on_resize(self, event):
        self.sf.configure(width=self.winfo_width() - 20, height=self.winfo_height() - 65)

    def select_database_configure(self, value):
        self.select_database['values'] = list((i + 1 for i in range(value)))
        self.select_database.config(state='active')

    def update_database(self, event):
        self.re_open_database()
app = Window()
app.mainloop()