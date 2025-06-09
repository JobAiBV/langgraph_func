import requests
from urllib.parse import urljoin
from typing import Dict, Optional, Any
from enum import Enum, auto
from contextvars import ContextVar
from langgraph_func.logger import get_logger

FUNCTION_KEY: ContextVar[str] = ContextVar("FUNCTION_KEY")
logger = get_logger()

class FunctionKeySpec(Enum):
    INTERNAL = auto()  # pull key from context at call-time

AuthKey = Optional[str]  # literal key, or INTERNAL via the special enum

from pydantic import BaseModel

class AzureFunctionInvoker:
    def __init__(
        self,
        *,
        function_path: str,
        base_url: str,
        input_field_map: Dict[str, str],
        output_field_map: Optional[Dict[str, str]] = None,
        auth_key: AuthKey = None,
        timeout_seconds: Optional[float] = None,
    ):
        self.endpoint_url  = urljoin(base_url.rstrip("/") + "/", function_path.lstrip("/"))
        self.input_map     = input_field_map
        self.output_map    = output_field_map
        self.auth_key      = auth_key
        self.timeout       = timeout_seconds

    def __call__(self, payload: BaseModel) -> Dict[str, Any]:
        url = self.endpoint_url
        if self.auth_key is FunctionKeySpec.INTERNAL:
            key = FUNCTION_KEY.get(None)
        else:
            key = self.auth_key
        if key:
            url = f"{url}?code={key}"

        body: Dict[str, Any] = {}

        # Only include explicitly mapped fields
        missing = [field for field in self.input_map if not hasattr(payload, field)]
        if missing:
            raise KeyError(f"Missing required input attribute(s): {', '.join(missing)}")

        for local_name, remote_name in self.input_map.items():
            body[remote_name] = getattr(payload, local_name)


        logger.debug(f"[AzureFunctionInvoker] POST {url} with payload {body}")

        try:
            resp = requests.post(url, json=body, timeout=self.timeout)
            resp.raise_for_status()
            raw = resp.json()
        except requests.RequestException as e:
            logger.error(f"[AzureFunctionInvoker] HTTP error: {e}")
            raise RuntimeError(f"Function call failed: {e}")
        except ValueError as e:
            logger.error(f"[AzureFunctionInvoker] JSON decode error: {e}")
            raise RuntimeError(f"Invalid JSON from Function: {e}")

        if self.output_map:
            return {
                local_name: raw.get(remote_name)
                for remote_name, local_name in self.output_map.items()
            }
        else:
            return raw


        # 3) Call + parse JSON (unchanged) …
        try:
            resp = requests.post(url, json=body, timeout=self.timeout)
            resp.raise_for_status()
            raw = resp.json()
        except requests.RequestException as e:
            logger.error(f"[AzureFunctionInvoker] HTTP error: {e}")
            raise RuntimeError(f"Function call failed: {e}")
        except ValueError as e:
            logger.error(f"[AzureFunctionInvoker] JSON decode error: {e}")
            raise RuntimeError(f"Invalid JSON from Function: {e}")

        # 4) Map outputs (same as before) …
        if self.output_map:
            return {
                local_name: raw.get(remote_name)
                for remote_name, local_name in self.output_map.items()
            }
        else:
            return raw
