import os.path
from .errors import error


index = 0
class ArtSQL:
    def __init__(self, **fields):
        self.data = None
        global index
        self.__fields_row = []
        self.__fields_items = [item for item in fields.items()]

        index += 1
        self.__index = index
        self.__row_index = 0
        self.__bool_row = True
        self.__create_file()
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

    def get_list_data(self, **filter_parameters):
        self.data = self.get_all_data()
        self.data[0].pop(0)
        datas = [item for item in filter_parameters.items()]

        valid_parameters = []
        valid_datas = self.__fields_items
        valid_datas.insert(0, ('index', 1))

        for i in range(len(datas)):## table datas * filter items
            for j in range(len(self.data[0])):
                if self.data[0][j].lower() == datas[i][0]:
                    if type(self.data[1][j]) != type(datas[i][1]):
                        error(f'error')
                    valid_parameters.append(1)

        if len(valid_parameters) != len(datas):
            error(f'You added invalid filter parameter(s)')

        return_data = []
        check_sort = [[] for i in range(len(self.data))]
        self.data.pop(0)

        var_list = []
        for i, item in enumerate(self.__fields_items):
            for j in range(len(datas)):
                if item[0] == datas[j][0]:
                    var_list.append(i)

        for i, item in enumerate(self.data):
            for j in range(len(var_list)):
                for k in range(len(datas)):
                    if item[var_list[j]] == datas[k][1]:
                        check_sort[i].append(1)

        for i, item in enumerate(check_sort):
            if len(item) == len(filter_parameters):
                return_data.append(self.data[i])
        return return_data

    def get_dict_data(self, **filter_parameters):
        list_data = self.get_list_data(**filter_parameters)
        return_data = []
        keys = [k for k, i in self.__fields_items]
        for i in range(len(list_data)):
            return_data.append(dict(zip(keys, list_data[i])))
        return return_data

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

    def del_full_database(self):
        datas = []
        with open('file.artsql', 'r') as f:
            for row in f:
                data = row.strip().split(';')
                data.pop()
                datas.append(data)

        new_datas = []
        for i in range(len(datas)):
            if int(datas[i][0]) != self.__index:
                new_datas.append(datas[i])
        with open('file.artsql', 'w') as f:
            for i, item in enumerate(new_datas):
                for j in range(len(item)):
                    f.write(f'{new_datas[i][j]};')
                f.write('\n')

    def del_by_filter(self, **deleting_filter_parameters):
        deleting_datas = self.get_list_data(**deleting_filter_parameters)
        print(deleting_datas)

        all_data = []
        with open('file.artsql', 'r') as f:
            for row in f:
                convert_datas = []
                datas = row.strip().split(';')
                datas.pop()
                for item in datas:
                    convert_datas.append(self.__convert_string(item))
                all_data.append(convert_datas)

        database_data = [item[1:] for item in all_data if item[0] == self.__index]
        final_data = [item for item in database_data if item not in deleting_datas]
        no_database_data = [item for item in all_data if item[0] != self.__index]

        for i in range(len(final_data)):
            final_data[i].insert(0, self.__index)

        for i in range(len(no_database_data)):
            final_data.append(no_database_data[i])

        with open('file.artsql', 'w') as f:
            for i, item in enumerate(final_data):
                for j in range(len(item)):
                    f.write(f'{final_data[i][j]};')
                f.write('\n')
        self.__sort_database()

    def __create_file(self):
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
            self.__sort_database()
    def __sort_database(self):
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

