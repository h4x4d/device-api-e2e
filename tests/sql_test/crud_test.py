import requests
from hamcrest import assert_that, equal_to
import allure

from framework.rest.code_check import code_check


@allure.title("Test check CREATE CRUD")
def test_crud_create(device_api_alchemy, device):

    with allure.step("Get CRUD"):
        updates = device_api_alchemy.entries_by_id(int(device))

    with allure.step("check CRUD len"):
        assert_that(len(updates), equal_to(1))

    with allure.step("check CREATE type"):
        create_update = updates[-1]
        assert_that(create_update.type, equal_to(1))


@allure.title("Test check EDIT CRUD")
def test_crud_edit(device_api_alchemy, device, device_api):
    with allure.step("Get edit event of device"):
        event = device_api_alchemy.first_edit_event()
        payload = event.payload

    with allure.step("Update device"):
        update = device_api.update_device(device, payload['platform'], payload['user_id'])

    code_check(update[0], "ok")

    with allure.step("Get CRUD"):
        updates = device_api_alchemy.entries_by_id(int(device))

    with allure.step("Get len of CRUD"):
        assert_that(len(updates), equal_to(2))

    with allure.step("Check Payload"):
        new_payload = payload.copy()
        new_payload['id'] = int(device)

        new_update = updates[-1]
        del new_payload['created_at']
        del new_payload['updated_at']

        assert_that(new_update.type, equal_to(2))
        assert_that(new_update.payload, equal_to(new_payload))


@allure.title("Test check DELETE CRUD")
def test_crud_delete(device_api_alchemy, device, device_api):
    with allure.step("Delete device"):
        deletion = device_api.delete_device(device)

    code_check(deletion[0], "ok")

    with allure.step("Get CRUD"):
        updates = device_api_alchemy.entries_by_id(int(device))

    with allure.step("Get len of CRUD"):
        assert_that(len(updates), equal_to(2))

    with allure.step("Check type of update"):
        delete_update = updates[-1]
        assert_that(delete_update.type, equal_to(3))
