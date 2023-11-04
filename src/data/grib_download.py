import os

import cdsapi

from src.exceptions.grib_dowload import DownloadDataERA5Exceptions


# todo Criar classe para download dos arquivos do era 5
class DownloadDataERA5:
    # 13.881
    # <- 2.703
    # -> 14.678
    # 3.996
    def __init__(self, name_dataframe: str,
                 compress_type: str):
        self.name_dataframe = name_dataframe
        self.type_compress = compress_type

    # todo verificar se a variavel tem os tipos de escolha, caso não, não é nescessario passa todos o parametros.
    # todo para cada ano e cada variavel repetir o processo.

    def download(self, input_dict):
        c = cdsapi.Client(key=f"{'262360'}:{'1c48e7d7-e52b-49ab-b349-2fff684dbceb'}", url="https://cds.climate.copernicus.eu/api/v2")
        if self._validate_dict_to_download(input_dict):
            for variable in input_dict.get('variable'):
                for year in input_dict.get('year'):
                    c.retrieve(self.name_dataframe, self._format_dict_to_download(input_dict, variable, year),
                               f'{self.name_dataframe}.{self.type_compress}')
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
        if input_dict.get('format') != self.type_compress:
            return False
        if mandatory_fields:
            for field in mandatory_fields:
                if len(input_dict.get(field, [])) < 1:
                    raise DownloadDataERA5Exceptions(f'Insert {field} in dict to request !')
            return True
        return True


if __name__ == '__main__':

    test = DownloadDataERA5('sis-agroproductivity-indicators', 'tgz')
    data_sis_agroproductivity_indicators = {
        'format': 'tgz',
        'growing_season': '1st_season_per_campaign',
        'crop_type': 'maize',
        'product_family': 'crop_productivity_indicators',
        'variable': ['crop_development_stage'],
        'year': ['2002'],
        'month': [
            '01', '03', '05',
            '07', '08', '10',
            '12',
        ],
        'harvest_year': '2002',
        'day': '31',
    }
    test.download(data_sis_agroproductivity_indicators)
