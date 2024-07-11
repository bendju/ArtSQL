import os.path
from .errors import error

index = 0
class ArtSQL:

    def __init__(self, **fields):
        global index
        self.fields_row = []
        self.fields_items = [item for item in fields.items()]

        index += 1
        self.index = index
        self.row_index = 0
        self.check_row = None
        self.bool_row = True
        self.create_file()

    def add_data(self, **data):
        self.row_index += 1
        self.check_row = f'{self.index}.{self.row_index}'
        with open('file.artsql', 'rb') as f:
            for row in f:
                datas = row.strip().split(';'.encode())
                if datas[0].decode() == self.check_row:
                    self.bool_row = False
        if self.bool_row:
            with open('file.artsql', 'ab') as f:
                f.write(f'{self.index};{self.row_index};'.encode())
                for i, item in enumerate(data.items()):
                    if item[0] != self.fields_items[i][0]:
                        error(f'error you added invalid parameter: ** {item[0]} ** but giving ** {self.fields_items[i][0]} **')
                    if type(self.fields_items[i][1]) != type(item[1]):
                        error('invalid parameter(s)')
                    f.write(f'{item[1]};'.encode())
                f.write('\n'.encode())


    def create_file(self):
        if not os.path.exists('file.artsql'):
            with open('file.artsql', 'ab') as f:
                f.write(f'Database;Index;'.encode())
                for i in range(len(self.fields_items)):
                    f.write(f'{self.fields_items[i][0]};'.encode())
                f.write('\n'.encode())
