import os
from utils.robot_check import is_allowed
from db import database


def test_robot_check_allowed():
    # common site should return a boolean (can't guarantee True/False in CI)
    assert isinstance(is_allowed("https://example.com"), bool)


def test_db_init(tmp_path):
    # Point DB to a temporary sqlite file
    os.environ["BGV_DB"] = f"sqlite:///{tmp_path / 'test.db'}"
    database.init_db()
    # After init, the file should exist
    assert (tmp_path / 'test.db').exists()
