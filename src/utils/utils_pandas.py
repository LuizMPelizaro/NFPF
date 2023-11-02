import os

import pandas as pd


def create_csvfile(dataframe: pd.DataFrame, name_of_file, dir_to_save):
    if dir_to_save not in os.listdir('../../data'):
        os.makedirs(f'../../data/{dir_to_save}')
    if not dataframe.empty:
        dataframe.to_csv(f'../../data/{dir_to_save}/{name_of_file}', index=False)
        print(f'Dataframe {name_of_file} created !!')
    else:
        raise pd.errors.EmptyDataError('Dataframe empty !!')


def separate_dataframe(dataframe: pd.DataFrame, columns: list[str], value):
    dataframe_final = dataframe[dataframe[columns] == value]
    return dataframe_final
