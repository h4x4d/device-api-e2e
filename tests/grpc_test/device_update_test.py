import pytest

from data.device import PLATFORM, USER_ID, NEW_USER_ID, NEW_PLATFORM, \
    NEW_MALFORMED_USER_ID, NONEXISTENT_DEVICE_ID
from framework.fields_check import check_platform, check_user_id
from framework.grpc.clients.ozonmp.act_device_api.v1.act_device_api_pb2 import \
    DescribeDeviceV1Response, UpdateDeviceV1Response
from framework.grpc.code_check import code_check


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

    code_check(response, True)

    check_platform(device_data, PLATFORM if field_to_change not in ("platform", "both") else NEW_PLATFORM)
    check_user_id(device_data, USER_ID if field_to_change not in ("user_id", "both") else NEW_USER_ID)


def test_errored_data_update_device_grpc(device_api_grpc, device):
    with pytest.raises(TypeError):
        device_api_grpc.update_device(int(device),
                                      platform=NEW_PLATFORM,
                                      user_id=NEW_MALFORMED_USER_ID)


def test_update_nonexistent_device_grpc(device_api_grpc):
    response = device_api_grpc.update_device(NONEXISTENT_DEVICE_ID,
                                             platform=NEW_PLATFORM,
                                             user_id=int(NEW_USER_ID))

    code_check(response, False)
