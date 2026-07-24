

from app.api.v1.devices.schemas import AssignDeviceDTO
from app.api.v1.devices.schemas import UpdateStatusDeviceDTO
from fastapi import HTTPException
import pytest
from app.core.enums import ActionType
from app.models import device
from app.api.v1.devices.schemas import CreateDeviceDTO
from app.api.v1.devices.service import DeviceService
from unittest.mock import Mock

def test_create_device():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_device_repository.get_device_by_serial_number.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = True
    mock_type_device_repository.get_type_device_by_id.return_value = True
    current_user = {'id': 1}
    create_device_dto = CreateDeviceDTO(
        serial_number='123456789',
        brand='HP',
        model='ProBook',
        buy_date='2022-01-01',
        status_id=1,
        type_id=1
    )
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    service.create_device(create_device_dto, current_user)
    device = mock_device_repository.create_device.call_args.args[0]
    action = mock_action_log_repository.add_action_log.call_args.args[0]
    
    assert device.serial_number == create_device_dto.serial_number
    assert device.brand == create_device_dto.brand
    assert device.model == create_device_dto.model
    assert device.buy_date == create_device_dto.buy_date
    assert device.status_id == create_device_dto.status_id
    assert device.type_id == create_device_dto.type_id
    assert action.user_id == 1
    assert action.action_id == ActionType.CREATE_DEVICE
    mock_device_repository.create_device.assert_called_once()
    mock_action_log_repository.add_action_log.assert_called_once()

def test_create_device_already_exist():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_device_repository.get_device_by_serial_number.return_value = True
    current_user = {'id': 1}
    create_device_dto = CreateDeviceDTO(
        serial_number='123456789',
        brand='HP',
        model='ProBook',
        buy_date='2022-01-01',
        status_id=1,
        type_id=1
    )
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    with pytest.raises(HTTPException) as excinfo:
        service.create_device(create_device_dto, current_user)

    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == "Device already exists"
    assert mock_device_repository.get_device_by_serial_number.call_count == 1
    assert mock_status_device_repository.get_status_device_by_id.call_count == 0
    assert mock_type_device_repository.get_type_device_by_id.call_count == 0
    assert mock_device_repository.create_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0

def test_create_device_status_not_found():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_device_repository.get_device_by_serial_number.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = None
    current_user = {'id': 1}
    create_device_dto = CreateDeviceDTO(
        serial_number='123456789',
        brand='HP',
        model='ProBook',
        buy_date='2022-01-01',
        status_id=1,
        type_id=1
    )
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository
    )

    with pytest.raises(HTTPException) as excinfo:
        service.create_device(create_device_dto, current_user)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Status device not found"
    assert mock_device_repository.get_device_by_serial_number.call_count == 1
    assert mock_status_device_repository.get_status_device_by_id.call_count == 1
    assert mock_type_device_repository.get_type_device_by_id.call_count == 0
    assert mock_device_repository.create_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0

def test_create_device_type_not_found():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_type_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_device_repository.get_device_by_serial_number.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = True
    mock_type_device_repository.get_type_device_by_id.return_value = None
    current_user = {'id': 1}
    create_device_dto = CreateDeviceDTO(
        serial_number='123456789',
        brand='HP',
        model='ProBook',
        buy_date='2022-01-01',
        status_id=1,
        type_id=1
    )
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository
    )

    with pytest.raises(HTTPException) as excinfo:
        service.create_device(create_device_dto, current_user)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Type device not found"
    assert mock_device_repository.get_device_by_serial_number.call_count == 1
    assert mock_status_device_repository.get_status_device_by_id.call_count == 1
    assert mock_type_device_repository.get_type_device_by_id.call_count == 1
    assert mock_device_repository.create_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0
    

def test_update_status_device():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_type_device_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = True
    mock_status_device_repository.get_status_device_by_id.return_value = True

    update_status_device_dto = UpdateStatusDeviceDTO(status_id=1)
    current_user = {'id': 1}
    
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    service.update_status_device(1, update_status_device_dto, current_user)
    
    mock_status_device_repository.get_status_device_by_id.assert_called_once()
    mock_device_repository.update_device.assert_called_once()
    mock_action_log_repository.add_action_log.assert_called_once()
    mock_device_repository.update_device.assert_called_once_with(
        1,
        {"status_id": 1}
    )


def test_update_status_device_not_found():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_type_device_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = None
    mock_status_device_repository.get_status_device_by_id.return_value = True

    update_status_device_dto = UpdateStatusDeviceDTO(status_id=1)
    current_user = {'id': 1}
    
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    with pytest.raises(HTTPException) as excinfo:
        service.update_status_device(1, update_status_device_dto, current_user)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Device not found"
    assert mock_device_repository.get_device_by_id.call_count == 1
    assert mock_status_device_repository.get_status_device_by_id.call_count == 0
    assert mock_device_repository.update_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0

def test_update_status_device_status_not_found():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_type_device_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = True
    mock_status_device_repository.get_status_device_by_id.return_value = None

    update_status_device_dto = UpdateStatusDeviceDTO(status_id=1)
    current_user = {'id': 1}
    
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    with pytest.raises(HTTPException) as excinfo:
        service.update_status_device(1, update_status_device_dto, current_user)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Status device not found"
    assert mock_device_repository.get_device_by_id.call_count == 1
    assert mock_status_device_repository.get_status_device_by_id.call_count == 1
    assert mock_device_repository.update_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0


def test_assign_device():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_type_device_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = True
    mock_user_repository.get_user_by_id.return_value = True

    assign_device_dto = AssignDeviceDTO(user_id=1)
    current_user = {'id': 1}
    
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    service.assign_device(1, assign_device_dto, current_user)
    assert mock_device_repository.update_device.call_args.args[1] == {"user_id": 1}
    mock_device_repository.update_device.assert_called_once()
    mock_action_log_repository.add_action_log.assert_called_once()
    mock_device_repository.get_device_by_id.assert_called_once()
    mock_user_repository.get_user_by_id.assert_called_once()

def test_assign_device_not_found():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_type_device_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = None

    assign_device_dto = AssignDeviceDTO(user_id=1)
    current_user = {'id': 1}
    
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    with pytest.raises(HTTPException) as excinfo:
        service.assign_device(1, assign_device_dto, current_user)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Device not found"
    assert mock_device_repository.get_device_by_id.call_count == 1
    assert mock_user_repository.get_user_by_id.call_count == 0
    assert mock_device_repository.update_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0

def test_assign_device_user_not_found():
    mock_device_repository = Mock()
    mock_status_device_repository = Mock()
    mock_action_log_repository = Mock()
    mock_user_repository = Mock()
    mock_type_device_repository = Mock()

    mock_device_repository.get_device_by_id.return_value = True
    mock_user_repository.get_user_by_id.return_value = None

    assign_device_dto = AssignDeviceDTO(user_id=1)
    current_user = {'id': 1}
    
    service = DeviceService(
        device_repository=mock_device_repository,
        status_device_repository=mock_status_device_repository,
        type_device_repository=mock_type_device_repository,
        action_log_repository=mock_action_log_repository,
        user_repository=mock_user_repository,
    )

    with pytest.raises(HTTPException) as excinfo:
        service.assign_device(1, assign_device_dto, current_user)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "User not found"
    assert mock_device_repository.get_device_by_id.call_count == 1
    assert mock_user_repository.get_user_by_id.call_count == 1
    assert mock_device_repository.update_device.call_count == 0
    assert mock_action_log_repository.add_action_log.call_count == 0
