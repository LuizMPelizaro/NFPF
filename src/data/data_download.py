import os

import cdsapi

from src.exceptions.data_download import DownloadDataERA5Exceptions
from dotenv import load_dotenv


class DownloadDataERA5:
    load_dotenv()

    # 13.881
    # <- 2.703
    # -> 14.678
    # 3.996
    def __init__(self, name_dataframe: str):
        self.name_dataframe = name_dataframe

    def download(self, input_dict):
        c = cdsapi.Client(key=f"{os.environ.get('UID')}:{os.environ.get('APIKEY')}",
                          url="https://cds.climate.copernicus.eu/api/v2")
        if self._validate_dict_to_download(input_dict):
            for variable in input_dict.get('variable'):
                for year in input_dict.get('year'):
                    c.retrieve(self.name_dataframe, self._format_dict_to_download(input_dict, variable, year),
                               f'../../data/external_dataframe/{self.name_dataframe}_{year}_{variable}.{input_dict.get("format")}')
                    print('Success download !')

    @staticmethod
    def _format_dict_to_download(input_dict, variable, year):
        dict_to_download = input_dict
        dict_to_download['variable'] = variable
        dict_to_download['year'] = year
        return dict_to_download

    def _validate_dict_to_download(self, input_dict):
        if self.name_dataframe == 'sis-agrometeorological-indicators':
            return self._validate_agrometeorological_dict(input_dict)
        elif self.name_dataframe == 'sis-agroclimatic-indicators':
            return self._validate_dict_agroclimatic_dataset(input_dict)
        elif self.name_dataframe == 'sis-agroproductivity-indicators':
            return self._validate_dict_productivity_dataset(input_dict)
        else:
            raise DownloadDataERA5Exceptions('Invalid dataset name or not implemented validator !')

    def _validate_agrometeorological_dict(self, input_dict):
        expected_keys = ['version', 'format', 'year', 'variable', 'month', 'day', 'area', 'statistic']
        mandatory_fields = ['year', 'month', 'day']
        return self._validate_generic_dict(input_dict, expected_keys, mandatory_fields)

    def _validate_dict_productivity_dataset(self, input_dict):
        expected_keys = ['format', 'growing_season', 'crop_type', 'product_family', 'variable', 'year', 'month',
                         'harvest_year', 'day']
        mandatory_fields = ['year', 'month', 'day']
        return self._validate_generic_dict(input_dict, expected_keys, mandatory_fields)

    def _validate_dict_agroclimatic_dataset(self, input_dict):
        expected_keys = ['format', 'version', 'period', 'temporal_aggregation', 'experiment', 'origin', 'variable']
        return self._validate_generic_dict(input_dict, expected_keys)

    def _validate_generic_dict(self, input_dict, expected_keys, mandatory_fields=None):
        if not all(key in input_dict for key in expected_keys):
            return False
        if mandatory_fields:
            for field in mandatory_fields:
                if len(input_dict.get(field, [])) < 1:
                    raise DownloadDataERA5Exceptions(f'Insert {field} in dict to request !')
            return True
        return True


if __name__ == '__main__':
    # test = DownloadDataERA5('sis-agroproductivity-indicators')
    years = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011',
             '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    # grow_seasons = ['1st_season_per_campaign', '2st_season_per_campaign']
    # crops = ['maize', 'soybean', 'spring_wheat', 'wet_rice', 'winter_wheat']
    # variables = ['total_above_ground_production', 'crop_development_stage', 'total_weight_storage_organs']
    # for crop in crops:
    #     for year in years:
    #         for variable in variables:
    #             print(f'{crop}, {variable}, {year} ')
    #             data_sis_agroclimatic_indicators = {
    #                 'format': 'tgz',
    #                 'product_family': ['crop_productivity_indicators'],
    #                 'variable': [variable],
    #                 'crop_type': [crop],
    #                 'year': [year],
    #                 'day': [
    #                     '10', '20', '28',
    #                     '30', '31',
    #                 ],
    #                 'month': [
    #                     '01', '02', '03',
    #                     '04', '05', '06',
    #                     '07', '08', '09',
    #                     '10', '11', '12',
    #                 ],
    #                 'harvest_year': [year],
    #                 'growing_season': '1st_season_per_campaign',
    #             }
    #             test.download(data_sis_agroclimatic_indicators)

    test = DownloadDataERA5('sis-agrometeorological-indicators')
    variables = ['2m_temperature']
    statistcs = [
        '24_hour_maximum', '24_hour_mean', '24_hour_minimum',
        'day_time_maximum', 'day_time_mean', 'night_time_mean',
        'night_time_minimum',
    ]
    for variable in variables:
        for statistc in statistcs:
            data_download = {
                'version': '1_1',
                'format': 'tgz',
                'variable': '2m_temperature',
                'statistic': [statistc],
                'year': '2002',
                'month': [
                    '01', '02', '03',
                    '04', '05', '06',
                    '07', '08', '09',
                    '10', '11', '12',
                ],
                'day': ['01', '02', '03',
                        '04', '05', '06',
                        '07', '08', '09',
                        '10', '11', '12',
                        '13', '14', '15',
                        '16', '17', '18',
                        '19', '20', '21',
                        '22', '23', '24',
                        '25', '26', '27',
                        '28', '29', '30',
                        '31', ],
                'area': [
                    13.88, 2.7, 3.99,
                    14.67,
                ],
            }
            test.download(data_download)
