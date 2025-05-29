from dataclasses import dataclass
from typing import Dict, List


# ─────────────────────────────────────────────────────────────────────────────
# 1) Custom exception for yml_config errors
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationError(Exception):
    """Raised when the YAML yml_config is invalid or missing required attributes."""


# ─────────────────────────────────────────────────────────────────────────────
# 2) Pure data classes
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class GraphConfig:
    path: str
    source: str
    auth: str                 # must be one of AuthLevel names: ANONYMOUS | FUNCTION | ADMIN
    input_attr: str = "Input"
    output_attr: str = "Output"
    graph_attr: str = "compiled_graph"
    description: str = ""     # Human-readable description of what this graph does


@dataclass
class BlueprintConfig:
    path: str
    graphs: Dict[str, GraphConfig]
    description: str = ""     # Human-readable description of this blueprint


@dataclass
class SwaggerConfig:
    title: str
    auth: str                 # must be one of AuthLevel names: ANONYMOUS | FUNCTION | ADMIN
    version: str = "1.0.0"
    ui_route: str = "docs"

@dataclass
class FuncAppConfig:
    blueprints: Dict[str, BlueprintConfig]
    swagger: SwaggerConfig