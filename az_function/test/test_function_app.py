import sys
import os
import json
import azure.functions as func
import pytest
from unittest.mock import MagicMock, patch

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import the Azure function you're testing
from function_app import http_triggerali

@pytest.fixture
def mock_container():
    """Create a mock container for Cosmos DB."""
    return MagicMock()

@pytest.fixture
def req_without_name():
    """Create a mock HTTP request without a name in the body."""
    req_body = json.dumps({"name": "test_user"}).encode('utf-8')
    req = MagicMock(spec=func.HttpRequest)
    req.get_json.return_value = json.loads(req_body)
    req.__body_bytes = req_body  # Ensure this is bytes
    return req

@pytest.fixture
def mock_environment_variables():
    """Mock the environment variables for testing."""
    with patch.dict(os.environ, {
        "COSMOS_ENDPOINT": "https://your-cosmos-endpoint",
        "COSMOS_KEY": "your-cosmos-key"
    }):
        yield

def test_http_trigger_without_name(req_without_name, mock_container, mock_environment_variables):
    """Test case where the request does not provide a name."""
    # Mock CosmosDB response
    mock_container.read_item.return_value = {'count': 0}
    mock_container.upsert_item.return_value = None

    # Call the function
    response = http_triggerali(req_without_name)

    # Add your assertions here
    assert response.status_code == 200  # Update with expected status code

def test_http_trigger_create_new_visitor_item(req_without_name, mock_container, mock_environment_variables):
    """Test case for creating a new visitor item."""
    # Mock CosmosDB exception and create new item
    mock_container.read_item.side_effect = Exception('Item not found')
    mock_container.create_item.return_value = {'count': 1}

    # Call the function and handle the exception if you want
    try:
        response = http_triggerali(req_without_name)
        assert response.status_code == 200  # Update with expected status code
    except Exception as e:
        assert str(e) == 'Item not found'  # Expect the exception message

def test_some_other_case(req_without_name, mock_container, mock_environment_variables):
    """A placeholder for another test case."""
    pass
