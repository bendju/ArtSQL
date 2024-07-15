import os.path
from .errors import *
from .varrible import get_tables

index = 0

## noTODO re del_by_filter, get_list_data
class MetaArtSQL:
    def __init__(self, filename='file', existing_index=0, **fields):
        global index
        index += 1
        self.__index = index
        self.__row_index = 0
        self.__filename = filename
        self.__fields_items = [item for item in fields.items()]

        if existing_index == 0:
            self.__create_file()
            self.__add_table_fields()
            self.__sort_database()
            self.check_index()
        else:
            self.__index = existing_index

    def get_list_data(self, fields=False, **filter_parameters):
        self.__len_check(filter_parameters, f'Add Minimum 1 filter parameter for filtering')
        filtering_datas = [item for item in filter_parameters.items()] # [('age', 10)]
        filter_parameters = self.__fields_items.copy() #[('index', 1), ('name', ' '), ('age', 0), ('fa', ' ')]
        filter_parameters.insert(0, ('index', 1))

        # check types
        for i in range(len(filtering_datas)):
            for j in range(len(filter_parameters)):
                if filtering_datas[i][0] == filter_parameters[j][0]:
                    if type(filtering_datas[i][1]) != type(filter_parameters[j][1]):
                        error(f'You Added Invalid type in get_list_data() method!! \n'
                              f' ** {filtering_datas[i][0]} parameter giving {type(filter_parameters[j][1])}\n'
                              f' but you added {type(filtering_datas[i][1])} **')

        # select datas
        return_data = []
        return_index = []
        filter_template = []
        filtering_datas_dict = dict(filtering_datas)
        for data in filter_parameters:
            key, item = data
            if key in filtering_datas_dict:
                filter_template.append(filtering_datas_dict[key])
            else:
                filter_template.append(None)

        data = self.get_all_data()

        # print(data)
        for i in range(len(data)):
            for j in range(len(filter_template)):
                if filter_template[j] is None:
                    try:
                        data[i].pop(j)
                        data[i].insert(j, None)
                    except:
                        pass

        ## get return indexes
        return_index = [i for i, item in enumerate(data) if item == filter_template]
        """
        for i, item in enumerate(data):
            if item == filter_template:
                return_index.append(i)
        """
        # return data
        original_data = self.get_all_data()
        for i in return_index:
            return_data.append(original_data[i])

        return return_data

    def get_dict_data(self, **filter_parameters):
        data = self.get_list_data(**filter_parameters)
        return_data = []
        keys = [k for k, i in self.__fields_items]
        keys.insert(0, 'index')
        for i in range(len(data)):
            return_data.append(dict(zip(keys, data[i])))
        return return_data

    def get_all_data(self, fields=False):
        data = self.__get_all()
        convert_data = [item[1:] for item in data if item[0] == self.__index]
        return convert_data if fields else convert_data[1:]

    def add_data(self, oblige=False, **data):
        # check rows
        check = True
        check_data = self.__get_all()
        self.__row_index += 1
        database_data = [item[1:] for item in check_data if item[0] == self.__index]

        for i in range(len(database_data)):
            if database_data[i][0] == self.__row_index:
                check = False

        # check length
        try:
            if len(data) != len(self.__fields_items):
                raise ValueError
        except ValueError as e:
            print(e)
            error('you do not added enough parameters!')

        ## check type
        datas = [item for item in data.items()]
        for i in range(len(datas)):
            if datas[i][1] == '':
                tuple_data = (datas[i][0] , self.__fields_items[i][1])
                datas.pop(i)
                datas.insert(i, tuple_data)
            try:
                if type(datas[i][1]) != type(self.__fields_items[i][1]):
                    raise ValueError
            except:
                error(f'You Added Invalid Value in add_data() method\n give me {type(datas[i][1])}, and not {type(self.__fields_items[i][1])}')

        ## covert
        final_data = [[item[1] for item in datas]]
        if oblige:
            final_data[0].insert(0, f'{database_data[len(database_data) -1][0] + 1}')
        else:
            final_data[0].insert(0, self.__row_index)
        final_data[0].insert(0, self.__index)

        # add data
        if check or oblige:
            self.__write_all(final_data)

    def delete_database_file(self):
        try:
            os.remove(f'{self.__filename}.artsql')
        except FileNotFoundError as e:
            print(e)
            error('file is not exist')

    def del_database(self):
        data = self.__get_all()
        datas = [item for item in data if item[0] != self.__index]
        self.__write_all(datas, mode='w')

    def del_by_filter(self, **deleting_parameters):
        deleting_datas = self.get_list_data(**deleting_parameters)
        all_data = self.__get_all()

        database_data = [item[1:] for item in all_data if item[0] == self.__index]
        final_data = [item for item in database_data if item not in deleting_datas]
        no_database_data = [item for item in all_data if item[0] != self.__index]

        for i in range(len(final_data)):
            final_data[i].insert(0, self.__index)

        final_data.extend(no_database_data)

        self.__write_all(final_data, 'w')
        self.__sort_database()

    def __get_all(self):
        data = []
        with open(f'{self.__filename}.artsql', 'r') as f:
            for row in f:
                datas = row.strip().split(';')
                convert_data = []
                for i in range(len(datas)):
                    convert_data.append(self.__convert_string(datas[i]))
                data.append(convert_data)

        return data

    def __write_all(self, data, mode='a'):
        with open(f'{self.__filename}.artsql', mode) as f:
            for i, item in enumerate(data):
                for j in range(len(item)):
                    if j + 1 == len(item):
                        f.write(f'{data[i][j]}')
                    else:
                        f.write(f'{data[i][j]};')
                f.write('\n')

    def __create_file(self):
        if not os.path.exists('file.artsql'):
            with open(f'{self.__filename}.artsql', 'ab'):
                pass

    def __add_table_fields(self):
        # create table fields string
        table_fields = [self.__index, 'Database', 'Index']
        for i in range(len(self.__fields_items)):
            table_fields.append(self.__fields_items[i][0])

        # check table fields
        data = self.__get_all()
        check = True
        for i in range(len(data)):
            if data[i] == table_fields:
                check = False
                break
        if check:
            self.__write_all([table_fields])

    def __sort_database(self):
        datas = self.__get_all()
        data, database = [], []

        for i in range(len(datas)):
            if datas[i][1] == 'Database':
                database.append(datas[i])
            else:
                data.append(datas[i])

        database.extend(data)
        self.__write_all(database, mode='w')

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

    def __len_check(self, var, text):
        if len(var) < 1:
            error(text)

    def check_index(self):
        new_index = [item[0] for i, item in enumerate(get_tables(self.__filename))]
        self.__index = int(new_index[-1])

