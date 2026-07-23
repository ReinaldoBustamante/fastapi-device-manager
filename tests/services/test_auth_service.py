from app.api.v1.auth.schemas import CreateUserDTO
from app.api.v1.auth.service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from unittest.mock import Mock, patch, call
import pytest
from fastapi import HTTPException

def test_login():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_user = Mock()
    mock_auth_repository.get_by_username.return_value = mock_user

    form_data = OAuth2PasswordRequestForm(
        username="test@test.com",
        password="test"
    )

    service= AuthService(auth_repository=mock_auth_repository, role_repository=mock_role_repository)

    with patch("app.api.v1.auth.service.verify_password") as mock_verify_password, \
        patch("app.api.v1.auth.service.create_token") as mock_create_token:

        mock_verify_password.return_value = True
        mock_create_token.return_value = "fake_token"

        result = service.login(form_data)

        assert result == {
            "access_token": "fake_token"
        }
    mock_auth_repository.get_by_username.assert_called_once_with(form_data.username)

def test_login_with_unknown_user():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_auth_repository.get_by_username.return_value = None

    form_data = OAuth2PasswordRequestForm(
        username="test@test.com",
        password="test"
    )

    service = AuthService(auth_repository=mock_auth_repository, role_repository=mock_role_repository)

    with pytest.raises(HTTPException) as exc_info:
        service.login(form_data)
    
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials"
    mock_auth_repository.get_by_username.assert_called_once_with(form_data.username)

def test_login_with_invalid_password():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_user = Mock()
    mock_auth_repository.get_by_username.return_value = mock_user
    form_data = OAuth2PasswordRequestForm(
        username="test@test.com",
        password="test"
    )

    service= AuthService(auth_repository=mock_auth_repository, role_repository=mock_role_repository)

    with patch("app.api.v1.auth.service.verify_password") as mock_verify_password:
        mock_verify_password.return_value = False
        with pytest.raises(HTTPException) as exc_info:
            service.login(form_data)
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid credentials"

    mock_auth_repository.get_by_username.assert_called_once_with(form_data.username)


def test_register():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_current_role = Mock()
    mock_current_user = {"role_id": 1}
    mock_current_role.name = "ADMIN"
    mock_create_user_dto = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="[EMAIL_ADDRESS]",
        password="password",
        role_id=2
    )
    mock_role_repository.get_by_id.return_value = mock_current_role
    mock_auth_repository.get_by_username.return_value = None
    mock_user_created = Mock()
    mock_auth_repository.create_user.return_value = mock_user_created
    service = AuthService(auth_repository=mock_auth_repository, role_repository=mock_role_repository)

    result = service.register(mock_create_user_dto, mock_current_user)

    assert result == mock_user_created
    assert mock_role_repository.get_by_id.call_count == 2 
    mock_role_repository.get_by_id.assert_has_calls([
        call(1),
        call(2)   
    ])
    mock_auth_repository.get_by_username.assert_called_once_with(mock_create_user_dto.email)

def test_register_with_not_admin():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_current_role = Mock()
    mock_current_user = {"role_id": 2}
    mock_current_role.name = "EMPLOYEE"
    mock_create_user_dto = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="[EMAIL_ADDRESS]",
        password="password",
        role_id=2
    )
    mock_role_repository.get_by_id.return_value = mock_current_role
    service = AuthService(mock_auth_repository, mock_role_repository)

    with pytest.raises(HTTPException) as exc_info:
        service.register(mock_create_user_dto, mock_current_user)
    
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You don't have permission to create this role"
    assert mock_auth_repository.get_by_username.call_count == 0
    assert mock_auth_repository.create_user.call_count == 0
    assert mock_role_repository.get_by_id.call_count == 1
    mock_role_repository.get_by_id.assert_called_once_with(2)
    
def test_register_with_existing_user():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_current_role = Mock()
    mock_current_user = {"role_id": 1}
    mock_current_role.name = "ADMIN"
    mock_create_user_dto = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="[EMAIL_ADDRESS]",
        password="password",
        role_id=2
    )
    mock_role_repository.get_by_id.return_value = mock_current_role
    mock_auth_repository.get_by_username.return_value = Mock()
    service = AuthService(mock_auth_repository, mock_role_repository)

    with pytest.raises(HTTPException) as exc_info:
        service.register(mock_create_user_dto, mock_current_user)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "User already exists"
    assert mock_auth_repository.get_by_username.call_count == 1
    assert mock_auth_repository.create_user.call_count == 0
    assert mock_role_repository.get_by_id.call_count == 1
    mock_role_repository.get_by_id.assert_called_once_with(1)
    mock_auth_repository.get_by_username.assert_called_once_with(mock_create_user_dto.email)

def test_register_with_nonexistent_role():
    mock_auth_repository = Mock()
    mock_role_repository = Mock()
    mock_current_role = Mock()
    mock_current_user = {"role_id": 1}
    mock_current_role.name = "ADMIN"
    mock_create_user_dto = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        email="[EMAIL_ADDRESS]",
        password="password",
        role_id=5
    )
    mock_role_repository.get_by_id.side_effect = [
        mock_current_role,
        None               
    ]
    mock_auth_repository.get_by_username.return_value = None

    service = AuthService(mock_auth_repository, mock_role_repository)

    with pytest.raises(HTTPException) as exc_info:
        service.register(mock_create_user_dto, mock_current_user)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Role not found"
    assert mock_role_repository.get_by_id.call_count == 2
    mock_auth_repository.create_user.assert_not_called()
    mock_role_repository.get_by_id.assert_has_calls([
        call(1),
        call(5)   
    ])
   