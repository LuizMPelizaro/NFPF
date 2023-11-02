import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.utils.utils_plot import filter_series_time, create_dir_to_save_img


class Plot:
    def __init__(self, csv_filename: str, x_value: str, y_value: str, x_label: str = '', y_label: str = '',
                 title: str = '', orient='v'):
        """
        Class for automatically creating plots.
        Implemented plots: num_values_per and time_series_plot.
        Args:
            csv_filename: Path or CSV filename.
            x_value: Value for the X-axis.
            y_value: Value for the Y-axis.
            x_label: Name for the X-axis in the plot.
            y_label: Name for the Y-axis in the plot.
            title: Title for the plot.
            orient: Orientation for the plot.
        """
        self.path_csv_filename = csv_filename
        self.x_value = x_value
        self.y_value = y_value
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.orient = orient

    def num_values_per(self, save_img=False, img_name=''):
        """
        Bar plot for unique values.
        Args:
            save_img: If True, save the plot image.
            img_name: Name for the image file.
        """
        data = pd.read_csv(self.path_csv_filename)
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

    def time_series_plot(self, filtered_by: dict, show_plot: bool = False, save_img: bool = False):
        """
        Plot the time series based on the provided filter.
        Args:
            filtered_by: Dictionary of filters, e.g.
            filters = {
            'type': 'market',
            'coin': 'price',
            'math_function': 'mean'
                }
            show_plot: If True, display the plot in the IDE.
            save_img: If True, save the image.
        """
        for dataframe in os.listdir(self.path_csv_filename):
            print(f'Plot dataframe: {dataframe[:-4]}')
            df = pd.read_csv(f'{self.path_csv_filename}/{dataframe}')
            products = df['commodity'].unique()
            for commodity in products:
                df_plot = filter_series_time(df, filtered_by, commodity)
                df_plot_final = df_plot.copy()
                df_plot_final['date'] = pd.to_datetime(df_plot_final['date'])
                sns.set(style="darkgrid")
                plt.figure(figsize=(11, 8))
                sns.lineplot(data=df_plot_final, x='date', y=filtered_by['coin'])
                plt.title(f'{self.title} {commodity}')
                plt.xlabel(f'{self.x_label}')
                plt.ylabel(f'{self.y_label}')
                plt.xticks(rotation=45)
                if save_img:
                    directory = f'time_series_per_{filtered_by["type"]}_{filtered_by["coin"]}'
                    sub_directory = f'time_series_plot_per_{filtered_by["type"]}_{dataframe[:-4]}_{filtered_by["coin"]}'
                    create_dir_to_save_img(
                        f'{directory}/{sub_directory}')
                    plt.savefig(
                        f'../../img/{directory}/{sub_directory}/time_series_{commodity}.jpg')
                if show_plot:
                    plt.show()
                plt.close()

