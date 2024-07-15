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

    def get_all_data(self, fields=False):
        """
        passes all the data in the table

        :return:
        """
        return super().get_all_data()


    def get_list_data(self, fields=False, **filter_parameters):
        """
        the filter expects data (name='ArtSQL').
        that matches these filter criteria,
        returned as a two-dimensional list.: [['ArtSQL'], ['ArtSQL']]

        :param fields:
        :param filter_parameters:
        :return:
        """
        return super().get_list_data(**filter_parameters)


    def get_dict_data(self, **filter_parameters):
        """
        the filter expects data (name='ArtSQL').
        that matches these filter criteria,
        returned as a two-dimensional list.
        Only the data in the list will be dictations: [{'name': 'ArtSQL'}, {'name': 'ArtSQL'}]

        :param filter_parameters:
        :return:
        """
        return super().get_dict_data(**filter_parameters)


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
        super().add_data(oblige=False, **data)


    def del_database(self):
        """
        deletes the data + cells of the entire database

        :return:
        """
        super().del_database()

    def delete_database_file(self):
        '''
        for deleting database file
        :return:
        '''
        super().delete_database_file()

    def del_by_filter(self, **deleting_filter_parameters):
        """
        the filter expects data eg: (name='ArtSQL').
        That match the filter will be deleted from the database.

        :param deleting_filter_parameters:
        :return:
        """
        super().del_by_filter(**deleting_filter_parameters)