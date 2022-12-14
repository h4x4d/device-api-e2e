import allure
import requests
from framework.rest.models import DeviceResponse
from framework.rest.write_log import write_log


class DeviceAPI:
    def __init__(self, host, token):
        self.host = host
        self.session = requests.Session()
        self.session.headers.update({'Authorization': token})

    def get_device(self, device_id):
        url = f'{self.host}/api/v1/devices/{device_id}'
        response = self.session.get(url)

        allure.attach(write_log(response), "Get log", allure.attachment_type.TEXT)

        assert response.status_code == 200, 'Wrong code'
        device_data = response.json().get('value') if response.ok else None
        return response.status_code, DeviceResponse(**device_data)

    def create_device(self, platform, user_id):
        url = f'{self.host}/api/v1/devices'
        data = {
            "platform": platform,
            "userId": user_id,
        }

        response = self.session.post(url, json=data)

        allure.attach(write_log(response), "Create log", allure.attachment_type.TEXT)

        device_id = response.json().get('deviceId') if response.ok else None
        return response.status_code, device_id

    def delete_device(self, device_id: str):
        url = f'{self.host}/api/v1/devices/{device_id}'
        response = self.session.delete(url)

        allure.attach(write_log(response), "Delete log", allure.attachment_type.TEXT)

        device_data = response.json() if response.ok else None
        return response.status_code, device_data

    def update_device(self, device_id: int, platform: str = None, user_id: int = None):
        url = f"{self.host}/api/v1/devices/{device_id}"

        data = {
            "platform": platform,
            "user_id": user_id
        }

        response = self.session.put(url, json=data)

        allure.attach(write_log(response), "Update log", allure.attachment_type.TEXT)

        device_data = response.json() if response.ok else None

        return response.status_code, device_data
