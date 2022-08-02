import pytest
import requests
from hamcrest import assert_that, equal_to

from data.device import PLATFORM, USER_ID, NEW_USER_ID, NEW_PLATFORM, \
    NEW_MALFORMED_USER_ID, NONEXISTENT_DEVICE_ID


@pytest.mark.parametrize("field_to_change", [("user_id",), ("platform",), ("both",)],
                         ids=["user_id", "platform", "both"])
def test_update_device_rest(device_api, device, field_to_change):
    status_code, device_data = device_api.get_device(int(device))

    assert_that(status_code, equal_to(requests.codes['ok']))

    status_code, response = device_api.update_device(int(device),
                                                     platform=PLATFORM if
                                                     field_to_change not in ("platform", "both")
                                                     else NEW_PLATFORM,
                                                     user_id=int(USER_ID) if
                                                     field_to_change not in ("user_id", "both")
                                                     else int(NEW_USER_ID))

    assert_that(status_code, equal_to(requests.codes['ok']))

    assert_that(
        device_data.platform, equal_to(PLATFORM if field_to_change not in ("platform", "both")
                                       else NEW_PLATFORM),
        f'Platform is {device_data.platform}',
    )
    assert_that(
        str(device_data.userId), equal_to(USER_ID if field_to_change not in ("user_id", "both")
                                          else NEW_USER_ID),
        f'UserID is {device_data.userId}'
    )


def test_errored_data_update_device_rest(device_api, device):
    status_code, response = device_api.update_device(int(device),
                                                     platform=NEW_PLATFORM,
                                                     user_id=NEW_MALFORMED_USER_ID)

    assert_that(status_code, equal_to(requests.codes['bad']))


def test_update_nonexistent_device_rest(device_api):
    status_code, response = device_api.update_device(NONEXISTENT_DEVICE_ID,
                                                     platform=NEW_PLATFORM,
                                                     user_id=int(NEW_USER_ID))

    # assert_that(status_code, equal_to(requests.codes['bad']))

    assert_that(response['success'], equal_to(False), "Non-valid response")
