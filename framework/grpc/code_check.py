from hamcrest import assert_that, equal_to


def code_check(response, expectation: bool):
    assert_that(response.success, equal_to(expectation),
                f"Response success is {response.success}, not {expectation}")
