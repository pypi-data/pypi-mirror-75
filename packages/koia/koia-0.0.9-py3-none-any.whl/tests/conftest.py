import json

import pytest


class Helpers:
    def database_config(self, filename: str) -> dict:
        with open(filename, "r") as f:
            data = json.load(f)

        return data


@pytest.fixture
def helpers():
    return Helpers
