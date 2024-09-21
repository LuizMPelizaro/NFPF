from src.data_process.adjust_data import DataProcess
from src.data_process.fix_nan_data_points import FixNanDataPoints

path_of_data = '../data/raw/wfp_food_prices_nga.csv'
path_to_save = '../data/processed/'
columns_to_remove = ['latitude', 'longitude']
path_to_save_logs = '../data/logs/'
path_of_fix_dataframes = '../data/processed/'
columns_to_fix_dataframes = ['price', 'usdprice']

data_process = DataProcess(dataframe_path=path_of_data, path_to_save=path_to_save, columns_to_remove=columns_to_remove,
                           path_to_save_logs=path_to_save_logs)
data_process.process()

fix_nan_data_points = FixNanDataPoints(dataframes_path=path_of_fix_dataframes,
                                       columns_to_apply=columns_to_fix_dataframes)
fix_nan_data_points.apply_fix()
