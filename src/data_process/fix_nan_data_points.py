import os
import sys

import pandas as pd
from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


class FixNanDataPoints:
    def __init__(self, dataframes_path, columns_to_apply):
        self.dataframes_path = dataframes_path
        self.columns_to_apply = columns_to_apply

    @staticmethod
    def __interpolate(dataframe, column):
        interpolate = dataframe[column].interpolate(method='slinear')
        dataframe[column] = dataframe[column].combine_first(interpolate)
        return dataframe

    def __get_dataframe_list(self):
        try:
            dataframes_list = os.listdir(self.dataframes_path)
            return dataframes_list
        except NotADirectoryError as e:
            raise e

    def __check_column_type(self, dataframe):
        for col in self.columns_to_apply:
            if pd.api.types.is_integer_dtype(dataframe[col]):
                continue
            elif pd.api.types.is_float_dtype(dataframe[col]):
                continue
            else:
                raise 'Column type not supported.'
        return True

    def __read_data(self, dataframe_path):
        if 'csv' in dataframe_path:
            raw_dataframe = pd.read_csv(f'{self.dataframes_path}/{dataframe_path}')
        elif 'excel' in dataframe_path:
            raw_dataframe = pd.read_excel(f'{self.dataframes_path}/{dataframe_path}')
        elif 'parquet' in dataframe_path:
            raw_dataframe = pd.read_parquet(f'{self.dataframes_path}/{dataframe_path}')
        else:
            logger.error('Not implemented yet.')
            raise NotImplementedError('Not implemented yet.')
        return raw_dataframe

    @staticmethod
    def __reindexing(dataframe):
        dataframe_reindexing = dataframe.copy()
        dataframe_reindexing = dataframe_reindexing.set_index('date', drop=True)
        full_index = pd.date_range(start=dataframe_reindexing.index.min(), end=dataframe_reindexing.index.max(),
                                   freq='MS')
        dataframe_reindexing = dataframe_reindexing.reindex(full_index)
        dataframe_reindexing.index.name = 'date'
        dataframe_reindexing.reset_index(inplace=True)
        return dataframe_reindexing

    def __save_data(self, dataframe, filename):
        dataframe.to_parquet(f'{self.dataframes_path}/{filename}', index=False)

    def apply_fix(self):
        logger.info(f'Start fixing data.')
        dataframe_list = self.__get_dataframe_list()
        for dataframe in dataframe_list:
            logger.info(f'Fixing {dataframe}')
            df = self.__read_data(dataframe)
            if self.__check_column_type(df):
                df_reindex = self.__reindexing(df)
                for col in self.columns_to_apply:
                    df_reindex = self.__interpolate(df_reindex, col)
                df_reindex = df_reindex.ffill()
                logger.info(f'saving {dataframe}.')
                self.__save_data(df_reindex, dataframe)
        logger.success(f'Success fixing data.')
