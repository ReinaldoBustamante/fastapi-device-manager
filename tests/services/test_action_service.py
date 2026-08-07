import pytest
from unittest.mock import Mock
from app.api.v1.actions.service import ActionService
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



    


 