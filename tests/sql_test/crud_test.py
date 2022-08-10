import requests
from hamcrest import assert_that, equal_to


def test_crud_create(device_api_alchemy, device):
    updates = device_api_alchemy.entries_by_id(int(device))

    assert_that(len(updates), equal_to(1))

    create_update = updates[-1]
    print(create_update.payload)
    assert_that(create_update.type, equal_to(1))


def test_crud_edit(device_api_alchemy, device, device_api):
    event = device_api_alchemy.first_edit_event()
    payload = event.payload

    update = device_api.update_device(device, payload['platform'], payload['user_id'])
    assert_that(update[0], equal_to(requests.codes['ok']))

    updates = device_api_alchemy.entries_by_id(int(device))

    assert_that(len(updates), equal_to(2))

    new_payload = payload.copy()
    new_payload['id'] = int(device)

    new_update = updates[-1]

    assert_that(new_update.type, equal_to(2))
    assert_that(new_update.payload, equal_to(new_payload))


def test_crud_delete(device_api_alchemy, device, device_api):
    deletion = device_api.delete_device(device)

    assert_that(deletion[0], equal_to(requests.codes['ok']))

    updates = device_api_alchemy.entries_by_id(int(device))
    assert_that(len(updates), equal_to(2))

    delete_update = updates[-1]
    assert_that(delete_update.type, equal_to(3))
