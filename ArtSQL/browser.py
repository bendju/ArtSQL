from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import Toplevel
from tkscrolledframe import ScrolledFrame

# noTODO bool filter_now create full new

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.temporary_data = []
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

        self.select_database_var = IntVar()
        self.select_database = ttk.Combobox(self.button_box, textvariable=self.select_database_var, width=4, state='disabled')
        self.select_database['values'] = (1,)
        self.select_database.current(0)
        open_button = ttk.Button(self.button_box, text='Open', command=self.open_database, padding=5)
        refresh_button = ttk.Button(self.button_box, text='Refresh', command=self.re_open_database, padding=5)
        filter_button = ttk.Button(self.button_box, text='Filter', command=self.filter, padding=5)
        self.database_condition = Label(self.button_box, text='Please Open Database', fg='red')

        self.select_database.grid(row=0, column=0, padx=4, pady=0)
        open_button.grid(row=0, column=1, padx=4, pady=0)
        refresh_button.grid(row=0, column=2, padx=4, pady=0)
        filter_button.grid(row=0, column=3, padx=4, pady=0)
        self.database_condition.grid(row=0, column=4, padx=10, pady=0)

        self.button_box.grid(row=0, column=0, sticky='w', pady=6)
        self.datas_name_box.grid(row=1, column=0, sticky='w')
        self.sf.grid(row=2, column=0, columnspan=2)

        self.geometry(f'{self.width}x{self.height}+200+100')
        self.title('ARTSQL DataBase Browser')
        self.bind("<Configure>", self.on_resize)

    def open_database(self):
        self.file_path = filedialog.askopenfilename(title='Open file', filetypes=(("ARTSQL Database", "*.artsql"),))
        if self.file_path != '':
            self.data = []
            select_index = 0
            with open(self.file_path, 'r') as f:
                for row in f:
                    data = row.strip().split(';')
                    data.pop()
                    if data[1] == 'Database':
                        select_index += 1
                    self.data.append(data)
            self.write_data(self.data)
            self.database_condition.config(text='Database Opened', fg='green')
            self.select_database_configure(select_index)

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
        filtered_data = []
        for i in range(len(data)):
            if data[i][1] == 'Database':
                self.temporary_data.append(data[i])

        for i in range(len(data)):
            try:
                if int(data[i][0]) == self.select_database_var.get():
                    data[i].pop(0)
                    filtered_data.append(data[i])
            except:
                pass
        data = filtered_data
        for i, item in enumerate(data):
            if item[0] == 'Database':
                item.pop(0)

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
        self.sf.configure(width=self.width-20, height=self.height-65)

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

            choice_temporary_data = []
            for i, item in enumerate(self.temporary_data):
                if self.data[i][1] == 'Database' and int(self.data[i][0]) == self.select_database_var.get():
                    choice_temporary_data = self.data[i]

            print(self.temporary_data)

            for i, item in enumerate(choice_temporary_data[2:]):
                frame = ttk.Frame(filter_box)
                Label(frame, text=item, width=25).grid(row=i, column=0)
                entry = Entry(frame, width=25)
                entry.grid(row=i, column=1)
                self.filter_entries.append(entry)
                frame.grid(row=i+1, column=0, pady=4)

            collect_button = ttk.Button(filter_box, text='Filter', command=self.filter_now)
            collect_button.grid()

        else:
            self.database_condition.configure(text='Please Open Database', fg='red', font=('Arial', 14))

    def filter_now(self):
        datas = [data.get() for data in self.filter_entries]
        datas_len = 0
        for item in datas:
            if item != '':
                datas_len += 1

        filtered_data = []
        check_short = [[] for i in range(len(self.data))]
        for i in range(len(self.data)):
            for j in range(len(datas)):
                if self.data[i][j] == datas[j]:
                    check_short[i].append(1)

        for i, item in enumerate(check_short):
            if len(item) == datas_len:
                filtered_data.append(self.data[i])

        filtered_data.insert(0, self.data[0])
        self.write_data(filtered_data)

    def select_database_configure(self, value):
        self.select_database['values'] = list((i + 1 for i in range(value)))
        self.select_database.config(state='active')


app = Window()

app.mainloop()