import pytest
import pandas as pd
import os
from unittest import mock

from src.data_process.adjust_data import DataProcess


# Certifique-se de ajustar o nome do arquivo onde a classe está implementada

@pytest.fixture
def sample_dataframe():
    data = {
        'date': pd.date_range('2023-01-01', periods=10, freq='M'),
        'priceflag': ['actual'] * 5 + ['forecast'] * 5,
        'price': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        'usdprice': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        'col1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        'col2': ['X', 'Y', 'Z', 'W', 'V', 'U', 'T', 'S', 'R', 'Q']
    }
    return pd.DataFrame(data)

@pytest.fixture
def data_process_instance(tmpdir, sample_dataframe):
    # Definir caminhos temporários para salvar os arquivos
    dataframe_path = tmpdir.join("dataframe.csv")
    path_to_save = tmpdir.join("save_path")
    path_to_save_logs = tmpdir.join("log_path")

    # Salvar o dataframe temporariamente
    sample_dataframe.to_csv(dataframe_path, index=False)

    # Inicializar a classe DataProcess
    columns_to_remove = ['col1', 'col2']
    return DataProcess(str(dataframe_path), str(path_to_save), columns_to_remove, str(path_to_save_logs))

# Testando a leitura do arquivo
def test_read_raw_data(data_process_instance):
    data_process_instance._DataProcess__read_raw_data()
    assert isinstance(data_process_instance.raw_dataframe, pd.DataFrame), "O arquivo não foi carregado corretamente"

# Testando a criação de IDs
def test_create_id(data_process_instance):
    data_process_instance._DataProcess__read_raw_data()
    data_process_instance.raw_dataframe = data_process_instance.raw_dataframe[data_process_instance.raw_dataframe['priceflag'] != 'forecast']
    data_process_instance._DataProcess__create_id()
    assert 'series_id' in data_process_instance.raw_dataframe.columns, "A coluna 'series_id' não foi criada"
    assert data_process_instance.raw_dataframe['series_id'].nunique() > 0, "Os IDs das séries não foram gerados corretamente"

# Testando a remoção de colunas
def test_remove_columns(data_process_instance):
    data_process_instance._DataProcess__read_raw_data()
    data_process_instance.raw_dataframe = data_process_instance.raw_dataframe[data_process_instance.raw_dataframe['priceflag'] != 'forecast']
    data_process_instance._DataProcess__remove_columns()
    assert 'col1' not in data_process_instance.raw_dataframe.columns, "A coluna 'col1' não foi removida"
    assert 'col2' not in data_process_instance.raw_dataframe.columns, "A coluna 'col2' não foi removida"

# Testando o processamento completo
@mock.patch('src.data_process.adjust_data.logger')
def test_process_data(mock_logger, data_process_instance):
    data_process_instance._DataProcess__read_raw_data()
    data_process_instance.process()
    assert os.path.exists(f'{data_process_instance.path_to_save}'), "Os dados processados não foram salvos corretamente"
    mock_logger.success.assert_called_with('Done process data.')
