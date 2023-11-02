import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.utils.utils_pandas import separate_dataframe


class PlotBaseInformation:
    def __init__(self, csv_filename: str, x_value: str, y_value: str, x_label: str = '', y_label: str = '',
                 title: str = '', orient='v'):
        self.csv_filename = csv_filename
        self.x_value = x_value
        self.y_value = y_value
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.orient = orient

    def num_values_per(self, save_img=False, img_name=''):
        data = pd.read_csv(self.csv_filename)
        sns.set(style="whitegrid")
        sns.set(context="notebook")
        plt.figure(figsize=(12, 8))
        sns.barplot(x=self.x_value, y=self.y_value, data=data, orient=self.orient)
        plt.ylabel(self.y_label)
        plt.xlabel(self.x_label)
        plt.title(self.title)
        if save_img:
            plt.savefig(f'../../img/{img_name}.jpg')
        plt.show()

    # todo, create time series plot per commodity price s c m
    def plot_time_series(self, column, save_img=False):
        dataframe = pd.read_csv(self.csv_filename)
        values = dataframe[column].unique()
        for value in values:
            print(value)
            dataframe_plot = separate_dataframe(dataframe, column, value)
            print(dataframe_plot)
            exit()

    # todo, create plot price variance

    def get_series_time_data(self, column):
        pass


if __name__ == '__main__':
    test = PlotBaseInformation('../../data/wfp_food_prices_nga.csv', '', '',
                               '', '', "", 'h')
    test.plot_time_series('commodity')
