import allure
import requests
from hamcrest import assert_that, equal_to


@allure.step("Status code check")
def code_check(status_code: int, expectation: str):
    assert_that(status_code, equal_to(requests.codes[expectation]),
                f"Excepted status code not is {expectation}")
