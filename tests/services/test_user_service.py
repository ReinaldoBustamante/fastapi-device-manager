from app.models import Device
from app.api.v1.users.schemas import CreateUserDTO
from fastapi import HTTPException
from app.api.v1.users.service import UserService
from unittest.mock import Mock, patch
from app.models import User
import pytest

def test_get_user_by_id_without_user_return_404():
    mock_user_repository = Mock()
    mock_device_repository = Mock()
    mock_user_repository.get_user_by_id.return_value = None

    user_service = UserService(mock_user_repository, mock_device_repository)
    
    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_id(1)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
    mock_user_repository.get_user_by_id.assert_called_once_with(1)

def test_get_user_by_id_return_user():
    mock_user_repository = Mock()
    mock_device_repository = Mock()
    mock_user = User(id=1, first_name="John", last_name="Doe", email="[EMAIL_ADDRESS]", password="[PASSWORD]")
    mock_user_repository.get_user_by_id.return_value = mock_user

    user_service = UserService(mock_user_repository, mock_device_repository)
    
    user = user_service.get_user_by_id(1)
    assert user == mock_user
    mock_user_repository.get_user_by_id.assert_called_once_with(1)

def test_create_user_with_existing_email_return_409():
    mock_user_repository = Mock()
    mock_device_repository = Mock()
    mock_create_user_dto = Mock()
    mock_user_repository.get_user_by_email.return_value = True

    user_service = UserService(mock_user_repository, mock_device_repository)

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(mock_create_user_dto)
        
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "User already exists"
    mock_user_repository.get_user_by_email.assert_called_once_with(mock_create_user_dto.email)

def test_create_user_without_existing_email_return_201():
    mock_user_repository = Mock()
    mock_user_repository.get_user_by_email.return_value = None
    mock_device_repository = Mock()
    mock_user = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="hashed_password",
        role_id=2
    )
    mock_create_user_dto = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="12345678"
    )
    mock_user_repository.create_user.return_value = mock_user

    with patch("app.api.v1.users.service.hash_password") as mock_hash:
        mock_hash.return_value = "hashed_password"
    
        user_service = UserService(mock_user_repository, mock_device_repository)
        user = user_service.create_user(mock_create_user_dto)

        assert user.first_name == mock_user.first_name
        assert user.last_name == mock_user.last_name
        assert user.email == mock_user.email
        assert user.password == mock_user.password
        assert user.role_id == mock_user.role_id
    
        assert mock_user_repository.get_user_by_email.call_count == 1
        assert mock_user_repository.create_user.call_count == 1

def test_deactivate_user_without_user_return_404():
    mock_user_repository = Mock()
    mock_device_repository = Mock()
    mock_user_repository.get_user_by_id.return_value = None

    user_service = UserService(mock_user_repository, mock_device_repository)
    
    with pytest.raises(HTTPException) as exc_info:
        user_service.deactivate_user(1)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
    mock_user_repository.get_user_by_id.assert_called_once_with(1)
    mock_user_repository.patch_user.assert_not_called()
    mock_device_repository.update_device.assert_not_called()

def test_deactivate_user_with_inactive_user_return_409():
    mock_user_repository = Mock()
    mock_device_repository = Mock()
    mock_user = User(id=1, first_name="John", last_name="Doe", email="[EMAIL_ADDRESS]", password="hashed_password", is_active=False)
    mock_user_repository.get_user_by_id.return_value = mock_user

    user_service = UserService(mock_user_repository, mock_device_repository)
    
    with pytest.raises(HTTPException) as exc_info:
        user_service.deactivate_user(1)
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "User is already inactive"
    mock_user_repository.get_user_by_id.assert_called_once_with(1)
    mock_user_repository.patch_user.assert_not_called()
    mock_device_repository.update_device.assert_not_called()

def test_deactivate_user_with_user_and_devices_return_200():
    mock_user_repository = Mock()
    mock_device_repository = Mock()
    mock_user = Mock()
    mock_user.is_active = True
    mock_user.devices = [Mock(), Mock()]

    mock_user_repository.get_user_by_id.return_value = mock_user
    mock_user_repository.patch_user.return_value = None
    mock_device_repository.update_device.return_value = None
    
    user_service = UserService(mock_user_repository, mock_device_repository)
    
    result = user_service.deactivate_user(1)
    assert result == {
        "message": "User deactivated successfully"
    }
    mock_user_repository.get_user_by_id.assert_called_once_with(1)
    assert mock_user_repository.patch_user.call_count == 1
    assert mock_device_repository.update_device.call_count == 2
    


 