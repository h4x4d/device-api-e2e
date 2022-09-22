import json

import allure
import grpc

from framework.grpc.clients.ozonmp.act_device_api.v1.act_device_api_pb2 import (
    DescribeDeviceV1Request, CreateDeviceV1Request, RemoveDeviceV1Request, UpdateDeviceV1Request,
    DescribeDeviceV1Response
)
from framework.grpc.clients.ozonmp.act_device_api.v1.act_device_api_pb2_grpc import (
    ActDeviceApiServiceStub)
from framework.grpc.serializer import serialize_to_json
from framework.rest.models import DeviceResponse


class DeviceAPIGRPC:
    def __init__(self, host):
        self._channel = grpc.insecure_channel(host)
        self._stub = ActDeviceApiServiceStub(self._channel)

    def get_device(self, device_id: int):
        request = DescribeDeviceV1Request(device_id=device_id)

        allure.attach(serialize_to_json(request), 'Describe device request',
                      allure.attachment_type.JSON)

        response: DescribeDeviceV1Response = self._stub.DescribeDeviceV1(request)

        allure.attach(serialize_to_json(response), 'Describe device response',
                      allure.attachment_type.JSON)

        return response

    def create_device(self, platform: str, user_id: int):
        request = CreateDeviceV1Request(platform=platform,
                                        user_id=user_id)
        allure.attach(serialize_to_json(request), 'Create device request',
                      allure.attachment_type.JSON)

        response = self._stub.CreateDeviceV1(request)
        allure.attach(serialize_to_json(response), 'Create device response',
                      allure.attachment_type.JSON)

        return response

    def delete_device(self, device_id: int):
        request = RemoveDeviceV1Request(device_id=device_id)
        allure.attach(serialize_to_json(request), 'Delete device request',
                      allure.attachment_type.JSON)

        response = self._stub.RemoveDeviceV1(request)
        allure.attach(serialize_to_json(response), 'Delete device response',
                      allure.attachment_type.JSON)

        return response

    def update_device(self, device_id: int, platform: str = None, user_id: int = None):
        request = UpdateDeviceV1Request(device_id=device_id,
                                        platform=platform,
                                        user_id=user_id)
        allure.attach(serialize_to_json(request), 'Update device request',
                      allure.attachment_type.JSON)

        response = self._stub.UpdateDeviceV1(request)
        allure.attach(serialize_to_json(response), 'Update device response',
                      allure.attachment_type.JSON)

        return response
