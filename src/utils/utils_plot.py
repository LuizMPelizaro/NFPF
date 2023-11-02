import pandas as pd
import os


def filter_series_time(dataframe: pd.DataFrame, dict_filters: dict, commodity: str):
    """
    Filters the DataFrame based on the provided parameters.
    Args:
        dataframe:Dataframe to filter.
        dict_filters: Dict with filters.
        commodity:Name of commodity to filter.

    Returns:
        Dataframe filtered per type and commodity.
    """
    if dict_filters['type'] == 'market':
        dataframe_final = dataframe[(dataframe[dict_filters['coin']] > 0) & (dataframe['commodity'] == commodity)]
        return dataframe_final
    elif dict_filters['type'] == 'city' or dict_filters['type'] == 'state':
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        dataframe_filtered = dataframe[(dataframe[dict_filters['coin']] > 0) & (dataframe['commodity'] == commodity)]
        dataframe_final = dataframe_filtered.groupby([dict_filters['type'], 'date'])[dict_filters['coin']].apply(
            dict_filters['math_function']).reset_index()
        return dataframe_final
    else:
        Exception('Invalid filter !!')


def create_dir_to_save_img(dir_to_save) -> None:
    """
    Create dir to save image of plots.
    Args:
        dir_to_save: Directory to save images.
    Returns:
        None
    """
    if not os.path.exists(f'../../img/{dir_to_save}'):
        os.makedirs(f'../../img/{dir_to_save}')
