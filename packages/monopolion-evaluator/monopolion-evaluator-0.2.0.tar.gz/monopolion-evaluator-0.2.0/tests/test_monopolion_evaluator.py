import os
import tempfile

import pytest

from monopolion_evaluator.classifier import Classifier
from monopolion_evaluator.cli import main


@pytest.fixture
def mock_classifier(monkeypatch):
    def mock_fit(*args, **kwargs):
        return None

    monkeypatch.setattr(Classifier, "fit_model", mock_fit)


def test_version(mock_classifier):
    main(['version'])


def test_train(mock_classifier):
    main(['train', '--training=tests/fixtures/toy_data_2player.gz', '--epochs=1'])


def test_train_validation(mock_classifier):
    main([
        'train',
        '--training=tests/fixtures/toy_data_2player.gz',
        '--validation=tests/fixtures/toy_data_2player.gz',
        '--epochs=1'])


def test_train_layers(mock_classifier):
    main([
        'train',
        '--training=tests/fixtures/toy_data_2player.gz',
        '-l', '1', '2', '4',
        '--epochs=1'])


def test_train_output_and_predict_integration():
    with tempfile.TemporaryDirectory() as tmp_dir_name:
        main([
            'train',
            '--training=tests/fixtures/toy_data_2player.gz',
            '-l', '1', '2', '4',
            '--epochs=1',
            f'--output={tmp_dir_name}'])

        model_dirs = os.listdir(tmp_dir_name)
        assert len(model_dirs) == 1
        model_dir = os.path.join(tmp_dir_name, model_dirs[0])

        main([
            'predict',
            f'--model={model_dir}',
            '--csv=tests/fixtures/toy-data-predict-cases.csv'])
