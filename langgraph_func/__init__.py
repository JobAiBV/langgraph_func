"""Utilities for building LangGraph agents and subagents."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

from langgraph_func.graph_helpers.call_subgraph import (
    AzureFunctionInvoker,
    FUNCTION_KEY,
    FunctionKeySpec,
)
from langgraph_func.graph_helpers.graph_builder_helpers import parse_json
from langgraph_func.graph_helpers.wrappers import validate_body, skip_if_locked
from langgraph_func.graph_endpoints.graph_executor_factory import EndpointGenerator
from langgraph_func.graph_endpoints.graph_executor_service import GraphExecutorService
from langgraph_func.graph_endpoints.registry import APIRegistry, Endpoint, registry
from langgraph_func.logger import get_logger
from langgraph_func.func_app_builder.func_app_builder import FuncAppBuilder
from langgraph_func.func_app_builder.blueprint_builder import BlueprintBuilder
from langgraph_func.func_app_builder.func_app_builder import FuncAppBuilder
from langgraph_func.yml_config.models import FuncAppConfig
from langgraph_func.yml_config.loader import load_funcapp_config

__all__ = [
    "AzureFunctionInvoker",
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
