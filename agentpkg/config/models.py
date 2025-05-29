from dataclasses import dataclass
from typing import Dict


# ─────────────────────────────────────────────────────────────────────────────
# 1) Custom exception for config errors
# ─────────────────────────────────────────────────────────────────────────────

class ConfigurationError(Exception):
    """Raised when the YAML config is invalid or missing required attributes."""


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
class FuncAppConfig:
    blueprints: Dict[str, BlueprintConfig]
