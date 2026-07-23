import pytest
from unittest.mock import Mock
from app.api.v1.actions.service import ActionService
from app.api.v1.actions.schemas import CreateActionDTO
from fastapi import HTTPException

def test_get_action_by_id():
    mock_action_repository = Mock()
    mock_action = Mock()
    mock_action_repository.get_action_by_id.return_value = mock_action
    service = ActionService(mock_action_repository)

    result = service.get_action_by_id(1)

    assert result == mock_action
    mock_action_repository.get_action_by_id.assert_called_once_with(1)

def test_get_action_by_id_not_found():
    mock_action_repository = Mock()
    mock_action_repository.get_action_by_id.return_value = None
    service = ActionService(mock_action_repository)

    with pytest.raises(HTTPException) as excinfo:
       service.get_action_by_id(1)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Action not found"
    mock_action_repository.get_action_by_id.assert_called_once_with(1)

def test_create_action():
    mock_action_repository = Mock()
    mock_action_repository.get_action_by_name.return_value = None
    mock_action = Mock()
    mock_action_repository.create_action.return_value = mock_action
    dto = CreateActionDTO(name= "Create")
    service = ActionService(mock_action_repository)

    result = service.create_action(dto)

    assert result == mock_action
    mock_action_repository.get_action_by_name.assert_called_once_with(dto.name)


def test_create_action_already_exists():
    mock_action_repository = Mock()
    mock_action = Mock()
    mock_action_repository.get_action_by_name.return_value = mock_action
    dto = CreateActionDTO(name= "Create")
    service = ActionService(mock_action_repository)

    with pytest.raises(HTTPException) as excinfo:
        service.create_action(dto)

    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == f"Action {dto.name} already exists"
    mock_action_repository.create_action.assert_not_called()

def test_delete_action():
    mock_action_repository = Mock()
    mock_action = Mock()
    mock_action.action_logs = []
    mock_action_repository.get_action_by_id.return_value = mock_action
    mock_action_repository.delete_action.return_value = mock_action    
    service = ActionService(mock_action_repository)

    result = service.delete_action(1)

    assert result == mock_action
    mock_action_repository.get_action_by_id.assert_called_once_with(1)
    mock_action_repository.delete_action.assert_called_once_with(mock_action)

def test_delete_action_has_logs():
    mock_action_repository = Mock()

    mock_log = Mock()
    mock_action = Mock()
    mock_action.action_logs = [mock_log]

    mock_action_repository.get_action_by_id.return_value = mock_action
    service = ActionService(mock_action_repository)
    with pytest.raises(HTTPException) as excinfo:
        service.delete_action(1)

    assert excinfo.value.status_code == 409
    assert excinfo.value.detail == "Action has logs"
    mock_action_repository.get_action_by_id.assert_called_once_with(1)
    mock_action_repository.delete_action.assert_not_called()


    


 