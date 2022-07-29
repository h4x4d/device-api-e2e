import pytest

from framework.device_api import DeviceAPI
from config import HOST, TOKEN
from data.device import PLATFORM, USER_ID


@pytest.fixture(scope='session')
def device_api():
    return DeviceAPI(HOST, TOKEN)


@pytest.fixture(scope='function')
def device(device_api):
    _, device_id = device_api.create_device(platform=PLATFORM, user_id=USER_ID)

    yield device_id

    device_api.delete_device(device_id)
