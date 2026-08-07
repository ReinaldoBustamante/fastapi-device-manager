from datetime import date
from app.api.v1.devices.schemas import CreateDeviceDTO, UpdateStatusDeviceDTO, AssignDeviceDTO
from app.api.v1.devices.service import DeviceService
from fastapi import HTTPException
from unittest.mock import Mock
import pytest

def test_get_all_devices_return_paginated_dict():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_devices = [Mock(), Mock()]
    mock_device_repository.get_all_devices.return_value = (mock_devices, 2)

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    result = device_service.get_all_devices(status_id=1, search="Dell", limit=10, offset=0)

    assert result == {
        "devices": mock_devices,
        "pagination": {
            "limit": 10,
            "offset": 0,
            "total": 2
        }
    }
    mock_device_repository.get_all_devices.assert_called_once_with(1, "Dell", 10, 0)

def test_get_device_by_id_without_device_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = None

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.get_device_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Device not found"
    mock_device_repository.get_device_by_id.assert_called_once_with(1)

def test_get_device_by_id_return_device():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device = Mock()
    mock_device_repository.get_device_by_id.return_value = mock_device

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    device = device_service.get_device_by_id(1)
    assert device == mock_device
    mock_device_repository.get_device_by_id.assert_called_once_with(1)

def test_create_device_with_existing_serial_number_return_409():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_serial_number.return_value = Mock()
    create_dto = CreateDeviceDTO(
        serial_number="SN12345",
        brand="Dell",
        model="XPS 15",
        buy_date=date(2024, 1, 1),
        status_id=1,
        type_id=1
    )
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.create_device(create_dto, current_user)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Serial number already exists"
    mock_device_repository.get_device_by_serial_number.assert_called_once_with("SN12345")
    mock_device_repository.create_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_create_device_with_nonexistent_status_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_serial_number.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = None

    create_dto = CreateDeviceDTO(
        serial_number="SN12345",
        brand="Dell",
        model="XPS 15",
        buy_date=date(2024, 1, 1),
        status_id=99,
        type_id=1
    )
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.create_device(create_dto, current_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Status device not found"
    mock_status_device_repository.get_status_device_by_id.assert_called_once_with(99)
    mock_device_repository.create_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_create_device_with_nonexistent_type_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_serial_number.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = Mock()
    mock_type_device_repository.get_type_device_by_id.return_value = None

    create_dto = CreateDeviceDTO(
        serial_number="SN12345",
        brand="Dell",
        model="XPS 15",
        buy_date=date(2024, 1, 1),
        status_id=1,
        type_id=99
    )
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.create_device(create_dto, current_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Type device not found"
    mock_type_device_repository.get_type_device_by_id.assert_called_once_with(99)
    mock_device_repository.create_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_create_device_success_return_device():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_serial_number.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = Mock()
    mock_type_device_repository.get_type_device_by_id.return_value = Mock()

    created_device = Mock(id=10)
    mock_device_repository.create_device.return_value = created_device

    create_dto = CreateDeviceDTO(
        serial_number="SN12345",
        brand="Dell",
        model="XPS 15",
        buy_date=date(2024, 1, 1),
        status_id=1,
        type_id=1
    )
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    result = device_service.create_device(create_dto, current_user)

    assert result == created_device
    assert mock_device_repository.create_device.call_count == 1
    assert mock_action_log_repository.add_action_log.call_count == 1

def test_update_status_device_without_device_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = None
    update_dto = UpdateStatusDeviceDTO(status_id=2)
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.update_status_device(1, update_dto, current_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Device not found"
    mock_device_repository.update_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_update_status_device_without_status_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device = Mock()
    mock_device_repository.get_device_by_id.return_value = mock_device
    mock_status_device_repository.get_status_device_by_id.return_value = None

    update_dto = UpdateStatusDeviceDTO(status_id=99)
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.update_status_device(1, update_dto, current_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Status device not found"
    mock_device_repository.update_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_update_status_device_success():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device = Mock()
    mock_device_repository.get_device_by_id.return_value = mock_device
    mock_status_device_repository.get_status_device_by_id.return_value = Mock()

    update_dto = UpdateStatusDeviceDTO(status_id=2)
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    result = device_service.update_status_device(1, update_dto, current_user)

    assert result == "Device status updated successfully"
    mock_device_repository.update_device.assert_called_once_with(mock_device, {"status_id": 2})
    assert mock_action_log_repository.add_action_log.call_count == 1

def test_assign_device_without_device_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = None
    assign_dto = AssignDeviceDTO(user_id=5)
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.assign_device(1, assign_dto, current_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Device not found"
    mock_device_repository.update_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_assign_device_without_user_return_404():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device = Mock()
    mock_device_repository.get_device_by_id.return_value = mock_device
    mock_user_repository.get_user_by_id.return_value = None

    assign_dto = AssignDeviceDTO(user_id=99)
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    with pytest.raises(HTTPException) as exc_info:
        device_service.assign_device(1, assign_dto, current_user)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
    mock_device_repository.update_device.assert_not_called()
    mock_action_log_repository.add_action_log.assert_not_called()

def test_assign_device_success():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()

    mock_device = Mock()
    mock_user = Mock()
    mock_device_repository.get_device_by_id.return_value = mock_device
    mock_user_repository.get_user_by_id.return_value = mock_user

    assign_dto = AssignDeviceDTO(user_id=5)
    current_user = {"id": 1}

    device_service = DeviceService(
        mock_device_repository,
        mock_status_device_repository,
        mock_type_device_repository,
        mock_action_log_repository,
        mock_user_repository
    )

    result = device_service.assign_device(1, assign_dto, current_user)

    assert result == "Device assigned successfully"
    mock_device_repository.update_device.assert_called_once_with(mock_device, {"user_id": 5})
    assert mock_action_log_repository.add_action_log.call_count == 1
