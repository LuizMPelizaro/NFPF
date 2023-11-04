import pytest

from src.data.grib_download import DownloadDataERA5

data_sis_agrometeorological_indicator = {
    'version': '1_1',
    'format': 'tgz',
    'year': '2002',
    'variable': '2m_dewpoint_temperature',
    'month': [
        '01', '02', '03',
        '04', '05', '06',
        '07',
    ],
    'day': [
        '01', '02', '03',
        '04', '05', '06',
        '07', '08', '09',
        '10', '11', '12',
        '13', '14', '15',
        '16', '17', '18',
        '19', '20', '21',
        '22', '23', '24',
        '25', '26', '27',
        '28', '29', '30',
        '31',
    ],
    'area': [
        13.88, 2.7, 4,
        14.68,
    ],
    'statistic': '24_hour_mean',
}

data_sis_agroproductivity_indicators = {
    'format': 'tgz',
    'growing_season': '1st_season_per_campaign',
    'crop_type': 'maize',
    'product_family': 'crop_productivity_indicators',
    'variable': 'crop_development_stage',
    'year': '2002',
    'month': [
        '01', '03', '05',
        '07', '08', '10',
        '12',
    ],
    'harvest_year': '2002',
    'day': '31',
}

data_sis_agroclimatic_indicators = {
    'format': 'tgz',
    'version': '1.1',
    'period': '201101_204012',
    'temporal_aggregation': 'season',
    'experiment': 'rcp2_6',
    'origin': 'miroc_esm_chem_model',
    'variable': 'maximum_number_of_consecutive_dry_days',
}


@pytest.fixture()
def setup():
    download_data = DownloadDataERA5('sis-agroclimatic-indicators', 'tgz')
    yield download_data


def test_normal_constructor_class(setup):
    assert isinstance(setup.name_dataframe, str)
    assert isinstance(setup.type_compress, str)


def test_validate_dict_agroclimatic_dataset(setup, input_dict=data_sis_agroclimatic_indicators):
    expected_keys = ['format', 'version', 'period', 'temporal_aggregation', 'experiment', 'origin', 'variable']
    if not all(key in input_dict for key in expected_keys):
        return False
    if input_dict['format'] != setup.type_compress:
        return False


def test_validate_dict_agrometeorological_dataset(setup, input_dict=data_sis_agrometeorological_indicator):
    expected_keys = ['version', 'format', 'year', 'variable', 'month', 'day', 'area', 'statistic']
    assert validate_dict(input_dict, setup, expected_keys)


def test_validate_dict_productivity_dataset(setup, input_dict=data_sis_agroproductivity_indicators):
    expected_keys = ['format', 'growing_season', 'crop_type', 'product_family', 'variable', 'year', 'month',
                     'harvest_year', 'day']
    assert validate_dict(input_dict, setup, expected_keys)


def test_invalid_format_for_agrometeorological_dataset(setup, input_dict):
    expected_keys = ['version', 'format', 'year', 'variable', 'month', 'day', 'area', 'statistic']
    input_dict['format'] = 'invalid_format'
    assert not validate_dict(input_dict, setup, expected_keys)


# Teste para uma chave com valor vazio (no caso, 'year')
def test_empty_year_for_agrometeorological_dataset(setup, input_dict):
    expected_keys = ['version', 'format', 'year', 'variable', 'month', 'day', 'area', 'statistic']
    input_dict['year'] = ''
    assert not validate_dict(input_dict, setup, expected_keys)


# Teste para um formato inválido em um dataset de produtividade
def test_invalid_format_for_productivity_dataset(setup, input_dict):
    expected_keys = ['format', 'growing_season', 'crop_type', 'product_family', 'variable', 'year', 'month',
                     'harvest_year', 'day']
    input_dict['format'] = 'invalid_format'
    assert not validate_dict(input_dict, setup, expected_keys)


# Teste para uma chave com valor vazio (no caso, 'crop_type') em um dataset de produtividade
def test_empty_crop_type_for_productivity_dataset(setup, input_dict):
    expected_keys = ['format', 'growing_season', 'crop_type', 'product_family', 'variable', 'year', 'month',
                     'harvest_year', 'day']
    input_dict['crop_type'] = ''
    assert not validate_dict(input_dict, setup, expected_keys)


def validate_dict(input_dict, setup, expected_keys, mandatory_fields=['month', 'day', 'year']):
    if not all(key in input_dict for key in expected_keys):
        return False
    if input_dict['format'] != setup.type_compress:
        return False
    for field in mandatory_fields:
        if len(input_dict[field]) < 1:
            return False
    return True
