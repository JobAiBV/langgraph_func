"""Utilities for building LangGraph agents and subagents."""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"

from agentpkg.graph_helpers.call_subgraph import (
    call_azure_function,
    call_subgraph,
    FUNCTION_KEY,
    FunctionKeySpec,
)
from agentpkg.graph_helpers.graph_builder_helpers import parse_json
from agentpkg.graph_helpers.wrappers import validate_body, skip_if_locked
from agentpkg.graph_endpoints.graph_executor_factory import EndpointGenerator
from agentpkg.graph_endpoints.graph_executor_service import GraphExecutorService
from agentpkg.graph_endpoints.registry import APIRegistry, Endpoint, registry
from agentpkg.logger import get_logger
from agentpkg.func_app_builder import FuncAppBuilder
from agentpkg.docs_function import bp_docs
from agentpkg.blueprint_builder import BlueprintBuilder
from agentpkg.func_app_builder import FuncAppBuilder

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
    "FuncAppBuilder",
    "BlueprintBuilder",
    "bp_docs",
    "__version__",
]
