import inspect

from .varrible import COLOR
import traceback

def error(data):
    print(COLOR['GREEN'] + '-'*len(data) + COLOR['END'])
    caller_line = inspect.currentframe().f_back.f_lineno
    print(COLOR['RED'] +  data + COLOR['END'])
    print(COLOR['GREEN'] + '-' * len(data) + COLOR['END'])

    traceback.print_exc()
    exit()
