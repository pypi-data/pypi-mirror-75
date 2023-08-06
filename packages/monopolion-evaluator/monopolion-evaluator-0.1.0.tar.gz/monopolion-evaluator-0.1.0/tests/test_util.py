import os
import re

import pytest

from monopolion_evaluator.util import create_model_directory

FAKE_MODEL_DIR = "/tmp/foo"


def test_create_model_directory(fs):
    fs.create_dir(FAKE_MODEL_DIR)

    path = create_model_directory(FAKE_MODEL_DIR)
    assert re.match(FAKE_MODEL_DIR + r'/\d{4}-\d{2}-\d{2}T\d{6}', path)
    assert os.path.isdir(path)


def test_create_model_directory_permission_denied(fs):
    fs.create_dir(FAKE_MODEL_DIR, perm_bits=0o000)

    with pytest.raises(PermissionError):
        create_model_directory(FAKE_MODEL_DIR)
