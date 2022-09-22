import allure
import pytest
from grpc import RpcError

from data.device import PLATFORM, USER_ID, NONEXISTENT_DEVICE_ID
from framework.fields_check import check_platform, check_user_id


@allure.title("Testing get of device (grpc)")
def test_get_device_grpc(device_api_grpc, device):
    with allure.step("Getting device"):
        device_data = device_api_grpc.get_device(int(device))

    check_platform(device_data, PLATFORM)
    check_user_id(device_data, USER_ID)


@allure.title("Testing get of nonexistent device (grpc)")
def test_get_nonexistent_device_grpc(device_api_grpc):
    with allure.step("Checking error"):
        with pytest.raises(RpcError):
            with allure.step("Trying to get nonexistent device"):
                device_api_grpc.get_device(NONEXISTENT_DEVICE_ID)
