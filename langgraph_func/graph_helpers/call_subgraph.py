import requests
from urllib.parse import urljoin
from typing import TypeVar, Union
from pydantic import BaseModel
from langgraph_func.logger import get_logger
from typing import Callable, Any
from contextvars import ContextVar
from enum import Enum, auto

FUNCTION_KEY: ContextVar[str] = ContextVar("FUNCTION_KEY")

class FunctionKeySpec(Enum):
    """If you pass this as function_key, we’ll use INTERNAL_KEY_CONTEXT."""
    INTERNAL = auto()

KeyArg = Union[FunctionKeySpec, str, None]
logger = get_logger()

def call_azure_function(
        function_path: str,
        payload: dict,
        base_url: str,
        function_key: KeyArg = None
) -> dict:
    """
    Calls an Azure Function using a base URL and a function path.

    :param function_path: Relative path to the Azure Function (e.g., 'api/myfunction')
    :param payload: The input payload as a dictionary
    :param base_url: Base URL of the Azure Function host (default is 'http://internal')
    :param function_key: (Optional) Function key for authorization
    :return: Dictionary with 'success' and either 'data' or 'error'
    """
    function_url = urljoin(base_url.rstrip("/") + "/", function_path.lstrip("/"))

    # choose the key
    if function_key is FunctionKeySpec.INTERNAL:
        key = FUNCTION_KEY.get(None)
    elif isinstance(function_key, str):
        key = function_key
    else:
        key = None

    if key is not None:
        function_url += f"?code={key}"

    try:
        logger.debug(f"Calling Azure Function at URL: {function_url} with payload {payload} ", )
        response = requests.post(function_url, json=payload)

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Function returned status code {response.status_code}: {response.text}"
            }

    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}

T = TypeVar("T", bound=BaseModel)

def call_subgraph(
    state: T,
    function_path: str,
    payload_builder: Callable[[T], dict],
    base_url: str,
    function_key: KeyArg = None
) -> dict:
    payload = payload_builder(state)
    logger.debug("Calling Azure Function '%s' with payload: %s", function_path, payload)

    result = call_azure_function(
        function_path=function_path,
        payload=payload,
        base_url=base_url,
        function_key=function_key
    )

    if not result.get("success"):
        error_message = result.get("error", "Unknown error")
        logger.error(
            "Azure Function '%s' failed with error: %s", function_path, error_message
        )
        raise RuntimeError(f"Azure Function call failed: {error_message}")

    logger.debug(f"Azure Function {function_path} succeeded with result: {result['data']}")
    return result["data"]
