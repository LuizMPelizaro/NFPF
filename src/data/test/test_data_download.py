import pytest

from src.data.data_download import DownloadDataERA5

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


class TestDownloadDataERA5:

    @pytest.fixture
    def setup(self):
        # You can set up any necessary dependencies here or initialize your class.
        pass

    def test_download(self, setup, monkeypatch):
        # Mock the behavior of the cdsapi.Client and validate the download method
        pass

    def test_format_dict_to_download(self, setup):
        # Test the _format_dict_to_download method with different input data
        pass

    @pytest.mark.parametrize("dataset_name, validator_method", [
        ('sis-agrometeorological-indicators', '_validate_agrometeorological_dict'),
        ('sis-agroclimatic-indicators', '_validate_dict_agroclimatic_dataset'),
        ('sis-agroproductivity-indicators', '_validate_dict_productivity_dataset'),
    ])
    def test_validate_dict_to_download(self, setup, dataset_name, validator_method):
        # Test the _validate_dict_to_download method for different dataset names
        pass

    def test_validate_agrometeorological_dict(self, setup):
        # Test the _validate_agrometeorological_dict method with different input data
        pass

    def test_validate_dict_productivity_dataset(self, setup):
        # Test the _validate_dict_productivity_dataset method with different input data
        pass

    def test_validate_dict_agroclimatic_dataset(self, setup):
        # Test the _validate_dict_agroclimatic_dataset method with different input data
        pass

    def test_validate_generic_dict(self, setup):
        # Test the _validate_generic_dict method with different input data
        pass

    def test_validate_generic_dict_with_mandatory_fields(self, setup):
        # Test the _validate_generic_dict method with mandatory fields and different input data
        pass
