import allure

from framework.rest.models import DeviceResponse
from hamcrest import assert_that, equal_to


def _check_value(value, expectation, what_is):
    assert_that(value, equal_to(expectation), f"{what_is} != {expectation}, but == {value}")


@allure.step("Checking user_id")
def check_user_id(response, expectation):
    if type(response) == DeviceResponse:
        user_id = response.userId
    else:
        user_id = str(response.value.user_id)

    _check_value(user_id, expectation, "user_id")


@allure.step("Checking platform")
def check_platform(response, expectation):
    if type(response) == DeviceResponse:
        platform = response.platform
    else:
        platform = response.value.platform

    _check_value(platform, expectation, "platform")
