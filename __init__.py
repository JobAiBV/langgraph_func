"""Utilities for building LangGraph agents and subagents."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

from .graph_helpers.call_subgraph import (
    call_azure_function,
    call_subgraph,
    FUNCTION_KEY,
    FunctionKeySpec,
)
from .graph_helpers.graph_builder_helpers import parse_json
from .graph_helpers.wrappers import validate_body, skip_if_locked
from .graph_endpoints.graph_executor_factory import EndpointGenerator
from .graph_endpoints.graph_executor_service import GraphExecutorService
from .graph_endpoints.registry import APIRegistry, Endpoint, registry
from .logger import get_logger
from .settings import settings

__all__ = [
    "call_azure_function",
    "call_subgraph",
    "FUNCTION_KEY",
    "FunctionKeySpec",
    "parse_json",
    "validate_body",
    "skip_if_locked",
    "EndpointGenerator",
    "GraphExecutorService",
    "APIRegistry",
    "Endpoint",
    "registry",
    "get_logger",
    "settings",
    "__version__",
]
