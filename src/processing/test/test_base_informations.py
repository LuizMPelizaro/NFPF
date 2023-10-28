import pytest
from pandas.errors import InvalidColumnName

from src.processing.base_informations import DataAnalyses


@pytest.fixture
def data_analyses_instance():
    return DataAnalyses('../../../data/wfp_food_prices_nga.csv')


def test_filter_columns_info(data_analyses_instance):
    columns = ["date", "state"]
    result = data_analyses_instance._DataAnalyses__filter_columns_info(columns)
    assert result == {"date": 264, "state": 14}


def test_filter_columns_info_with_invalid_column(data_analyses_instance):
    columns = ["invalid"]
    with pytest.raises(InvalidColumnName):
        data_analyses_instance._DataAnalyses__filter_columns_info(columns)
