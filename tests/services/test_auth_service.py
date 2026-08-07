from app.api.v1.auth.service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from unittest.mock import Mock, patch
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


