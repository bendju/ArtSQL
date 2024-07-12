import os
from .errors import error


class ArtSQL:
    global index
    index = 0

    def __init__(self, **fields):
        self.bool_row = True
        global index
        index += 1
        self.index = index
        self.row_index = 0
        self.fields = fields
        self.check_row = ''
        self.create_file()

    def get_data(self):
        getting_datas = []
        getting_datas_plus = []
        with open('file.artsql', 'rb') as f:
            for row in f:
                get_datas = row.strip().split(';'.encode())
                get_datas.pop()
                if int(get_datas[0].decode()[0]) == self.index:  # legkomolyabb hiba nem olvassa be
                    getting_datas_plus.append(get_datas)

        for i, item in enumerate(getting_datas_plus):
            getting_datas_plus_help = []
            for j in range(len(item)):
                getting_datas_plus_help.append(getting_datas_plus[i][j].decode())
            getting_datas.append(getting_datas_plus_help)

        return getting_datas

    def add_data(self, **data):
        print(data)
        if len(data) != len(self.fields):
            error(f'Invalid Parameters \n You Added {len(data)}, but {len(self.fields)} given')

        self.row_index += 1
        self.check_row = f'{self.index}.{self.row_index}'
        with open('file.artsql', 'rb') as f:
            for row in f:
                datas = row.strip().split(';'.encode())
                if datas[0].decode() == self.check_row:
                    self.bool_row = False

        if self.bool_row:
            with open('file.artsql', 'ab') as f:
                f.write(f'{self.index}.{self.row_index};'.encode())
                for i in range(len(self.fields)):
                    help_var = None
                    if self.fields[i][1] == 0:
                        help_var = 0
                    elif self.fields[i][1] == 1:
                        help_var = ' '
                    elif self.fields[i][1] == 2:
                        help_var = 0.0
                    elif self.fields[i][1] == 3:
                        help_var = True

                    if type(data[i]) is type(help_var):
                        f.write(f'{str(data[i][1])};'.encode())
                    else:
                        error(f'Invalid Parameter(s) you added {type(data[i])}, but giving {type(help_var)}')
                f.write('\n'.encode())

    def create_file(self):
        if not os.path.exists('file.artsql'):
            with open('file.artsql', 'ab') as f:
                pass

    def __str__(self):
        return f'ArtSQL database {self.index}'
