import pytest
import os
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture(scope='session')
def api_key():
    key = os.getenv('REQRES_PUBLIC_KEY')
    if not key:
        raise ValueError("REQRES_PUBLIC_KEY not found")
    return key

@pytest.fixture(scope='session')
def base_url():
    return 'https://reqres.in/api'

@pytest.fixture(scope='session')
def headers(api_key):
    return {"x-api-key": api_key}