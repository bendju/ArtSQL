import os
os.system("")

INTEGER = 0
STRING = ' '
FLOAT = 0.0
BOOL = True

def get_tables(filename):
    tables = []
    with open(f'{filename}.artsql', 'r') as f:
        for row in f:
            data = row.strip().split(';')
            if data[1] == 'Database':
                tables.append(data)
            else:
                break
    return tables

def print_tables(filename):
    print(get_tables(filename))

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "END": "\033[0m",
}