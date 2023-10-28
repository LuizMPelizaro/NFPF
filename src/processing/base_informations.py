import pandas as pd
from pandas.errors import InvalidColumnName
from src.utils.utils_pandas import get_dataframe, create_csvfile


class DataAnalyses:

    def __init__(self, csv_filename):
        self._csv_filename = csv_filename
        self._dataframe = get_dataframe(csv_filename)

    def __filter_columns_info(self, columns: list[str]) -> dict:
        """
        Return dataframe info per columns, type and number of unique values
        :param columns: Name of columns to consult
        :return: Dict with infos.
        """
        dataframe = self.dataframe
        dict_infos = {}
        for column in columns:
            if column not in dataframe.columns:
                raise InvalidColumnName(f'Invalid column name: {column}')
            dict_infos[column] = len(dataframe[column].unique())
        return dict_infos

    def get_infos(self, columns: list[str]) -> None:
        """
        Print infos of columns in console.
        :param columns: columns to check infos.
        :return: None
        """
        try:
            infos = self.__filter_columns_info(columns)
            for key, value in infos.items():
                print(f'Column: {key}\nUnique values: {value}')
                print('-----------------------------------------')
        except Exception as e:
            print(f'Error !\n{e}')

    def get_info_per(self, column: list[str]) -> None:
        """
        Create a DataFrame with the number of unique values per column, grouped by the specified column.
        :param column: list of columns to group.
        :return: None
        """
        try:
            dataframe = self.dataframe.copy()
            unique_values = dataframe.groupby(column).agg(lambda col: len(col.unique().tolist())).reset_index()
            dataframe_unique_values = pd.DataFrame(unique_values)
            create_csvfile(dataframe_unique_values, f'{self.csv_filename[:-4]}_agg_per_{column}.csv',
                           'dataframe_filter')
        except Exception as e:
            print(f'An error occurred: {str(e)}')

    def separate_dataframe_per(self, column: str) -> None:
        """
        Separate the dataframe by a specific column, e.g., State, retrieve all the data for that state, and place it in
        a new dataframe.
        :param column:The column by which the grouping will be done.
        :return:None
        """
        try:
            dataframe = self.dataframe.copy()
            values = dataframe[column].unique()
            for value in values:
                print(f'Separate per {value}')
                dataframe_separated = self.dataframe[dataframe[column] == value]
                create_csvfile(dataframe_separated, f'{value}.csv', f'dataframe_separated_per_{column}')
        except Exception as e:
            print(f'An error occurred: {str(e)}')

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def csv_filename(self):
        return self._csv_filename
