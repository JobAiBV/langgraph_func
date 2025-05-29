"""Utilities for building LangGraph agents and subagents."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

from langraph_api.graph_helpers.call_subgraph import (
    call_azure_function,
    call_subgraph,
    FUNCTION_KEY,
    FunctionKeySpec,
)
from langraph_api.graph_helpers.graph_builder_helpers import parse_json
from langraph_api.graph_helpers.wrappers import validate_body, skip_if_locked
from langraph_api.graph_endpoints.graph_executor_factory import EndpointGenerator
from langraph_api.graph_endpoints.graph_executor_service import GraphExecutorService
from langraph_api.graph_endpoints.registry import APIRegistry, Endpoint, registry
from langraph_api.logger import get_logger
from langraph_api.func_app_builder.func_app_builder import FuncAppBuilder
from langraph_api.func_app_builder.blueprint_builder import BlueprintBuilder
from langraph_api.func_app_builder.func_app_builder import FuncAppBuilder
from langraph_api.yml_config.models import FuncAppConfig
from langraph_api.yml_config.loader import load_funcapp_config

__all__ = [
    "call_azure_function",
    "call_subgraph",
    "FUNCTION_KEY",
    "FunctionKeySpec",
    "parse_json",
    "skip_if_locked",
    "FuncAppBuilder",
    "BlueprintBuilder",
    "FuncAppConfig",
    "load_funcapp_config",
    "__version__",
]
