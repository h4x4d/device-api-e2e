import pytest
from hamcrest import assert_that, equal_to

from data.device import PLATFORM, USER_ID, NEW_USER_ID, NEW_PLATFORM, \
    NEW_MALFORMED_USER_ID, NONEXISTENT_DEVICE_ID
from framework.grpc.clients.ozonmp.act_device_api.v1.act_device_api_pb2 import \
    DescribeDeviceV1Response, UpdateDeviceV1Response


@pytest.mark.parametrize("field_to_change", [("user_id",), ("platform",), ("both",)],
                         ids=["user_id", "platform", "both"])
def test_update_device_grpc(device_api_grpc, device, field_to_change):
    device_data: DescribeDeviceV1Response = device_api_grpc.get_device(int(device))

    response: UpdateDeviceV1Response = device_api_grpc.update_device(int(device),
                                                                     platform=PLATFORM if
                                                                     field_to_change not in ("platform", "both")
                                                                     else NEW_PLATFORM,
                                                                     user_id=int(USER_ID) if
                                                                     field_to_change not in ("user_id", "both")
                                                                     else int(NEW_USER_ID))

    assert_that(response.success, equal_to(True), "Validating response")

    assert_that(
        device_data.value.platform, equal_to(PLATFORM if field_to_change not in ("platform", "both")
                                             else NEW_PLATFORM),
        f'Platform is {device_data.value.platform}',
    )
    assert_that(
        str(device_data.value.user_id), equal_to(USER_ID if field_to_change not in ("user_id", "both")
                                                 else NEW_USER_ID),
        f'UserID is {device_data.value.user_id}'
    )


def test_errored_data_update_device_grpc(device_api_grpc, device):
    with pytest.raises(TypeError):
        device_api_grpc.update_device(int(device),
                                      platform=NEW_PLATFORM,
                                      user_id=NEW_MALFORMED_USER_ID)


def test_update_nonexistent_device_grpc(device_api_grpc):
    response = device_api_grpc.update_device(NONEXISTENT_DEVICE_ID,
                                             platform=NEW_PLATFORM,
                                             user_id=int(NEW_USER_ID))

    assert_that(response.success, equal_to(False), "Non-valid response")
