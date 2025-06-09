import requests
from urllib.parse import urljoin
from typing import TypeVar, Union, Generic, Dict, Optional
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

T = TypeVar("T", bound=BaseModel)

class AzureFunctionInvoker(Generic[T]):
    """
    A callable node that invokes an Azure Function synchronously
    via HTTP POST and returns its JSON payload.
    """
    def __init__(
        self,
        function_path: str,
        base_url: str,
        payload_builder: Callable[[T], Dict[str, Any]],
        function_key: Optional[FunctionKeySpec] = None,
        timeout: Optional[float] = None,
    ):
        self.function_path = function_path
        self.base_url = base_url.rstrip("/") + "/"
        self.payload_builder = payload_builder
        self.function_key = function_key
        self.timeout = timeout

    def __call__(self, state: T) -> Dict[str, Any]:
        """
        Build payload from `state`, POST to the Function, and return the parsed JSON.
        This is a blocking call; if you’re in an async context wrap it with asyncio.to_thread.
        """
        # build URL
        url = urljoin(self.base_url, self.function_path.lstrip("/"))
        # append key if present in context
        if self.function_key is FunctionKeySpec.INTERNAL:
            key = FUNCTION_KEY.get(None)
        else:
            key = self.function_key if isinstance(self.function_key, str) else None

        if key:
            url = f"{url}?code={key}"

        # build JSON payload
        payload = self.payload_builder(state)
        logger.debug(f"[AzureFunctionInvoker] POST {url} with payload {payload}")

        # call and validate
        try:
            resp = requests.post(url, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            logger.error(f"[AzureFunctionInvoker] Request failed: {e}")
            raise RuntimeError(f"Azure Function call failed: {e}")
        except ValueError as e:
            logger.error(f"[AzureFunctionInvoker] Invalid JSON response: {e}")
            raise RuntimeError(f"Invalid JSON from Azure Function: {e}")

        return data
