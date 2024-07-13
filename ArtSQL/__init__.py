from .varrible import STRING, INTEGER, FLOAT, BOOL
from .ArtSQL import MetaArtSQL

class ArtSQL(MetaArtSQL):
    def __init__(self, **fields):
        super().__init__()
        """
        enter the fields, they will be the cells of the table.
        A field looks like this: name=STRING,
        the first element of the fields is (name) 
        and the second element is 
        defined by the current data type: 
            STRING;  INTEGER;  FLOAT;  BOOL
        """

    def get_all_data(self):
        """
        passes all the data in the table

        :return:
        """


    def get_list_data(self, **filter_parameters):
        """
        the filter expects data (name='ArtSQL').
        that matches these filter criteria,
        returned as a two-dimensional list.: [['ArtSQL'], ['ArtSQL']]

        :param filter_parameters:
        :return:
        """


    def get_dict_data(self, **filter_parameters):
        """
        the filter expects data (name='ArtSQL').
        that matches these filter criteria,
        returned as a two-dimensional list.
        Only the data in the list will be dictations: [{'name': 'ArtSQL'}, {'name': 'ArtSQL'}]

        :param filter_parameters:
        :return:
        """


    def add_data(self, oblige=False, **data):
        """
        Filling table cells with data.
        Pay attention to types.
        !!! IMPORTANT !!! Type the table cells in order and type all the cells. !!! IMPORTANT !!!

        :param oblige: Once you've used it, you'll always need it. This makes it mandatory to add data.
        For more information, visit the documentation official website


        :param data:
        :return:
        """


    def del_full_database(self):
        """
        deletes the data + cells of the entire database

        :return:
        """

    def del_by_filter(self, **deleting_filter_parameters):
        """
        the filter expects data eg: (name='ArtSQL').
        That match the filter will be deleted from the database.

        :param deleting_filter_parameters:
        :return:
        """