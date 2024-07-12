import os.path
from .errors import error


# noTODO separating table rows and sqlbrowser ***
index = 0
class ArtSQL:
    def __init__(self, **fields):
        global index
        self.__fields_row = []
        self.__fields_items = [item for item in fields.items()]

        index += 1
        self.__index = index
        self.__row_index = 0
        self.__bool_row = True
        self.create_file()
        self.__add_table_fields()


    def get_all_data(self):
        datas = []
        with open('file.artsql', 'r') as f:
            for row in f:
                data = row.strip().split(';')
                data.pop()
                try:
                    if int(data[0]) == self.__index:
                        convert_data = []
                        for i in range(len(data)):
                            convert_data.append(self.__convert_string(data[i]))
                        convert_data.pop(0)
                        datas.append(convert_data)
                except:
                    pass
        return datas

    def get_filter_data(self):
        datas = self.get_all_data()


    def add_data(self, oblige=False, **data):
        if len(data) != len(self.__fields_items):
            error('you do not added enough parameters!')
        self.__row_index += 1
        with open('file.artsql', 'rb') as f:
            for row in f:
                datas = row.strip().split(';'.encode())
                if f'{datas[0].decode()}.{datas[1].decode()}' == f'{self.__index}.{self.__row_index}':
                    self.__bool_row = False
                    try:
                        self.__row_index = int(datas[1].decode()) + 1
                    except Exception:
                        pass

        if self.__bool_row or oblige:
            with open('file.artsql', 'ab') as f:
                for i, item in enumerate(data.items()):
                    if item[0] != self.__fields_items[i][0]:
                        error(f'error you added invalid parameter (add_data()): ** {item[0]} ** but giving ** {self.__fields_items[i][0]} **')
                    if type(self.__fields_items[i][1]) != type(item[1]):
                        error('You Added invalid parameter(s)')

                f.write(f'{self.__index};{self.__row_index};'.encode())
                for item in data.items():
                    f.write(f'{item[1]};'.encode())
                f.write('\n'.encode())


    def create_file(self):
        if not os.path.exists('file.artsql'):
            with open('file.artsql', 'ab'):
                pass

    def __convert_string(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False

        try:
            float_value = float(s)
            if float_value.is_integer():
                return int(float_value)
            return float_value
        except ValueError:
            pass

        return s

    def __add_table_fields(self):
        help_val = True
        with open('file.artsql', 'r') as f:
            for row in f:
                datas = row.strip().split(';')
                try:
                    if int(datas[0]) == self.__index:
                        help_val = False
                except:
                    pass
        if help_val:
            with open('file.artsql', 'ab') as f:
                f.write(f'{self.__index};Database;Index;'.encode())
                for i in range(len(self.__fields_items)):
                    f.write(f'{self.__fields_items[i][0]};'.encode())
                f.write('\n'.encode())

    @staticmethod
    def sort_database():
        database, data = [], []
        with open('file.artsql', 'r') as read:
            for row in read:
                datas = row.strip().split(';')
                datas.pop()
                if datas[1] == 'Database':
                    database.append(datas)
                else:
                    data.append(datas)

        with open('file.artsql', 'wb') as write:
            for i, item in enumerate(database):
                for j in range(len(item)):
                    write.write(f'{database[i][j]};'.encode())
                write.write('\n'.encode())

            for i, item in enumerate(data):
                for j in range(len(item)):
                    write.write(f'{data[i][j]};'.encode())
                write.write('\n'.encode())




