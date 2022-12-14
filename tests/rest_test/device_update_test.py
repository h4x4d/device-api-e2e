import allure
import pytest
from hamcrest import assert_that, equal_to

from data.device import PLATFORM, USER_ID, NEW_USER_ID, NEW_PLATFORM, \
    NEW_MALFORMED_USER_ID, NONEXISTENT_DEVICE_ID
from framework.fields_check import check_platform, check_user_id
from framework.rest.code_check import code_check


@allure.title("Test edit device rest")
@pytest.mark.parametrize("field_to_change", [("user_id",), ("platform",), ("both",)],
                         ids=["user_id", "platform", "both"])
def test_update_device_rest(device_api, device, field_to_change):
    with allure.step("Getting test device"):
        status_code, device_data = device_api.get_device(int(device))

    code_check(status_code, "ok")

    with allure.step("Updating test device"):
        status_code, response = device_api.update_device(int(device),
                                                         platform=PLATFORM if
                                                         field_to_change not in ("platform", "both")
                                                         else NEW_PLATFORM,
                                                         user_id=int(USER_ID) if
                                                         field_to_change not in ("user_id", "both")
                                                         else int(NEW_USER_ID))

    with allure.step("Checking"):
        code_check(status_code, "ok")
        check_platform(device_data, PLATFORM if field_to_change not in ("platform", "both") else NEW_PLATFORM)
        check_user_id(device_data, USER_ID if field_to_change not in ("user_id", "both") else NEW_USER_ID)


@allure.title("Test edit device with malformed data rest")
def test_errored_data_update_device_rest(device_api, device):
    with allure.step("Updating test device with malformed data"):
        status_code, response = device_api.update_device(int(device),
                                                         platform=NEW_PLATFORM,
                                                         user_id=NEW_MALFORMED_USER_ID)

    code_check(status_code, "bad")


@allure.title("Test edit nonexistent device rest")
def test_update_nonexistent_device_rest(device_api):
    with allure.step("Updating nonexistent device"):
        status_code, response = device_api.update_device(NONEXISTENT_DEVICE_ID,
                                                         platform=NEW_PLATFORM,
                                                         user_id=int(NEW_USER_ID))

    assert_that(response['success'], equal_to(False), "Non-valid response")
