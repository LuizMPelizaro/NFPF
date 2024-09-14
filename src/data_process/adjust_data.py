import os
import sys
from os import mkdir

import pandas as pd
from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


class DataProcess:
    def __init__(self, dataframe_path, path_to_save, columns_to_remove, path_to_save_logs):
        self.dataframe_path = dataframe_path
        self.path_to_save = path_to_save
        self.columns_to_remove = columns_to_remove
        self.path_to_save_logs = path_to_save_logs
        self.raw_dataframe = None

    def __create_id(self):
        logger.info('Create id for series.')
        logger.info('Remove flags is forecast.')
        exclude_columns = self.columns_to_remove
        exclude_columns.extend(['date', 'price', 'usdprice'])
        columns_to_use = self.raw_dataframe.columns.difference(exclude_columns)
        self.raw_dataframe = self.raw_dataframe[self.raw_dataframe['priceflag'] != 'forecast']

        generate_id = self.raw_dataframe[columns_to_use].astype('category').apply(lambda x: '_'.join(x), axis=1)

        self.raw_dataframe['series_id'] = generate_id

        self.raw_dataframe['series_id'] = self.raw_dataframe['series_id'].astype('category').cat.codes
        logger.info('Created id for series.')

    @staticmethod
    def __data_is_continuous(dataframe):
        dataframe = dataframe.sort_values(by='date')
        dataframe['diff'] = dataframe['date'].diff()
        is_continuous = dataframe['diff'].iloc[1:].nunique() == 1
        return is_continuous

    def __get_incomplete_series(self):
        dataframe = self.raw_dataframe.copy()
        dataframe_continuos = {
            'SerieCod': [],
            'DataContinuity': [],
            'DataPoints': []
        }
        for cod in dataframe['series_id'].unique():
            dataframe_to_check = dataframe[dataframe['series_id'] == cod]
            dataframe_continuos['SerieCod'].append(dataframe_to_check['series_id'].iloc[0])
            dataframe_continuos['DataContinuity'].append(self.__data_is_continuous(dataframe_to_check))
            dataframe_continuos['DataPoints'].append(len(dataframe_to_check['date'].unique()))
        return pd.DataFrame(dataframe_continuos)

    def __generate_log_table(self):
        logger.info('Generate log table.')
        dataframe_log = self.__get_incomplete_series()
        logger.info(f'Save log table in {self.path_to_save}')
        if not os.path.exists(self.path_to_save_logs):
            os.mkdir(self.path_to_save_logs)
        dataframe_log.to_csv(f'{self.path_to_save_logs}/log_table.csv', index=False)
        return dataframe_log

    def __remove_series(self):
        series_to_remove = self.__generate_log_table()
        logger.info('Removing series that have fewer than 24 data points.')
        list_of_id_to_remove = series_to_remove[series_to_remove['DataPoints'] < 24]['SerieCod'].to_list()
        self.raw_dataframe = self.raw_dataframe[~self.raw_dataframe['series_id'].isin(list_of_id_to_remove)]

    def __remove_columns(self):
        if not self.columns_to_remove:
            logger.info('Not columns to remove.')
        elif set(self.columns_to_remove).issubset(set(self.raw_dataframe.columns)):
            self.raw_dataframe = self.raw_dataframe.drop(columns=self.columns_to_remove)
            logger.info(f'Remove {self.columns_to_remove} columns.')
        else:
            logger.error('Not columns in dataset.')

    def __read_raw_data(self):
        if 'csv' in self.dataframe_path:
            self.raw_dataframe = pd.read_csv(self.dataframe_path)
        elif 'excel' in self.dataframe_path:
            self.raw_dataframe = pd.read_excel(self.dataframe_path)
        elif 'parquet' in self.dataframe_path:
            self.raw_dataframe = pd.read_parquet(self.dataframe_path)
        else:
            logger.error('Not implemented yet.')
            raise NotImplementedError('Not implemented yet.')

    def __save_data(self):
        if not os.path.exists(f'{self.path_to_save}'):
            mkdir(f'{self.path_to_save}')
        for series_id in self.raw_dataframe['series_id'].unique():
            dataframe_to_save = self.raw_dataframe[self.raw_dataframe['series_id'] == series_id].reset_index(drop=True)
            dataframe_to_save.to_parquet(f'{self.path_to_save}/{series_id}.parquet', index=False)

    def process(self):
        logger.info('Start process data')
        logger.info(f'Read {self.dataframe_path}')
        self.__read_raw_data()
        logger.info(f'Fix date to datetime.')
        self.raw_dataframe['date'] = pd.to_datetime(self.raw_dataframe['date'])
        self.raw_dataframe['date'] = self.raw_dataframe['date'].apply(lambda x: x.replace(day=1))
        logger.info(f'Filter columns.')
        self.__remove_columns()
        logger.info(f'Create ids for series.')
        self.__create_id()
        logger.info(f'Generate log table.')
        self.__generate_log_table()
        logger.info(f'Remove series.')
        self.__remove_series()
        logger.info(f'Save dataframes.')
        self.__save_data()
        logger.success('Done process data.')


if __name__ == '__main__':
    path_of_dataframe = sys.argv[1]
    path_to_save_dataframes = sys.argv[2]
    columns_to_remove = sys.argv[3]
    path_to_save_logs = sys.argv[4]

    dp = DataProcess(dataframe_path=path_of_dataframe,
                     path_to_save=path_to_save_dataframes,
                     columns_to_remove=columns_to_remove,
                     path_to_save_logs=path_to_save_logs)
    dp.process()
