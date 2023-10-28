import os

import pandas as pd


def get_dataframe(csv_filename: str) -> pd.DataFrame:
    """
    Get dataframe file in data archives.
    :param csv_filename: Name of datafile.
    :return: Pandas Dataframe.
    """
    if csv_filename not in os.listdir(csv_filename):
        raise FileNotFoundError('File not found in path !')
    dataframe = pd.read_csv(f'{csv_filename}')
    return dataframe


def create_csvfile(dataframe: pd.DataFrame, name_of_file, dir_to_save):
    if dir_to_save not in os.listdir('../../data'):
        os.makedirs(f'../../data/{dir_to_save}')
    if not dataframe.empty:
        dataframe.to_csv(f'../../data/{dir_to_save}/{name_of_file}', index=False)
        print(f'Dataframe {name_of_file} created !!')
    else:
        raise pd.errors.EmptyDataError('Dataframe empty !!')
