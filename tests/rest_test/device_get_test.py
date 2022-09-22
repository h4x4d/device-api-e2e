import allure

from data.device import PLATFORM, USER_ID
from framework.rest.code_check import code_check
from framework.fields_check import check_platform, check_user_id


@allure.title("Test get device rest")
def test_get_device_rest(device_api, device):
    with allure.step("Getting test device"):
        status_code, device_data = device_api.get_device(device)

    with allure.step("Checking"):
        code_check(status_code, "ok")
        check_platform(device_data, PLATFORM)
        check_user_id(device_data, USER_ID)
