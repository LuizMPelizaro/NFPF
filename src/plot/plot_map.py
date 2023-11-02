import pandas as pd
import folium

from folium.plugins import HeatMap


class PlotMap:
    def __init__(self, csv_filename: str, map_type: str):
        self.csv_filename = csv_filename
        self.map_type = map_type

    def plot_map(self, group_per):
        m = folium.Map(location=[9.0820, 8.6753], tiles="Cartodb Positron", zoom_start=6)
        if group_per == 'city' or group_per == 'market':
            self._plot_map_pin_points(m, group_per)
        elif group_per == 'state':
            self._plot_concentration_map(m, group_per)

    def _plot_map_pin_points(self, map_func, group_per):
        dataframe_to_plot = self._get_cords_per(group_per)
        for key in range(0, len(dataframe_to_plot.index)):
            folium.Marker([dataframe_to_plot['latitude'][key],
                           dataframe_to_plot['longitude'][key]],
                          tooltip=f'{dataframe_to_plot[group_per][key]}').add_to(map_func)
        map_func.save('../../img/maps/pin_city.html')

    def _plot_concentration_map(self, map_func, group_per):
        dataframe_to_plot = self._get_cords_per(group_per)
        cords = []
        for key in range(0, len(dataframe_to_plot)):
            lat_long = [dataframe_to_plot['latitude'][key], dataframe_to_plot['longitude'][key]]
            cords.append(lat_long)
        HeatMap(cords).add_to(map_func)
        map_func.save('../../img/maps/state_concentration.html')

    def _get_cords_per(self, grouping_type: str):
        dataframe = pd.read_csv(self.csv_filename)
        dataframe = dataframe[[grouping_type, 'latitude', 'longitude']]
        dataframe_unique = dataframe.drop_duplicates(subset=[grouping_type, 'latitude', 'longitude']).reset_index(
            drop=True)
        return dataframe_unique
