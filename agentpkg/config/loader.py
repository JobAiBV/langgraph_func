import importlib
import yaml
from typing import Any, Dict, List
from dataclasses import dataclass
from dacite import from_dict
from agentpkg.logger import get_logger
from azure.functions import AuthLevel
from langgraph.graph.state import CompiledStateGraph
from agentpkg.config.models import GraphConfig, BlueprintConfig, FuncAppConfig

logger = get_logger(__name__)

class ConfigurationError(Exception):
    """Raised when the YAML config is invalid or missing required attributes."""


@dataclass
class LoadedGraph:
    name: str
    path: str
    auth: AuthLevel            # strongly typed
    input: Any
    output: Any
    compiled_graph: CompiledStateGraph
    description: str           # graph-level description


@dataclass
class LoadedBlueprint:
    name: str
    path: str
    description: str
    graphs: List[LoadedGraph]


class GraphLoader:
    @staticmethod
    def load(name: str, cfg: GraphConfig) -> LoadedGraph:
        logger.debug(f"The name is {name} and the config is {cfg!r}")
        # 1) Import the source module
        try:
            module = importlib.import_module(cfg.source)
        except ImportError as e:
            raise ConfigurationError(f"[{name}] cannot import '{cfg.source}': {e}")

        # 2) Fetch helper
        def fetch(attr_name: str) -> Any:
            if not hasattr(module, attr_name):
                raise ConfigurationError(f"[{name}] module '{cfg.source}' is missing '{attr_name}'")
            return getattr(module, attr_name)

        # 3) Pull in graph pieces
        Input  = fetch(cfg.input_attr)
        Output = fetch(cfg.output_attr)
        cg     = fetch(cfg.graph_attr)

        # 4) Validate & convert auth
        auth_name = cfg.auth.strip().upper()
        if auth_name not in AuthLevel.__members__:
            valid = ", ".join(AuthLevel.__members__.keys())
            raise ConfigurationError(
                f"[{name}] invalid auth '{cfg.auth}'. Must be one of: {valid}"
            )
        auth_level = AuthLevel[auth_name]

        return LoadedGraph(
            name=name,
            path=cfg.path,
            auth=auth_level,
            input=Input,
            output=Output,
            compiled_graph=cg,
            description=cfg.description
        )


def load_funcapp_config(path: str) -> List[LoadedBlueprint]:
    """
    Loads a FuncAppConfig YAML and returns a dict mapping each blueprint name
    to its LoadedBlueprint (including description and its LoadedGraphs).
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    try:
        cfg = from_dict(data_class=FuncAppConfig, data=raw)
    except Exception as e:
        raise ConfigurationError(f"Invalid YAML structure: {e}")

    result: List[LoadedBlueprint] = []
    errors: List[str] = []

    for bp_name, bp_cfg in cfg.blueprints.items():
        logger.debug(f"Loading blueprint '{bp_name}' – {bp_cfg.description!r}")
        loaded_graphs: List[LoadedGraph] = []

        for graph_name, graph_cfg in bp_cfg.graphs.items():
            try:
                lg = GraphLoader.load(graph_name, graph_cfg)
                loaded_graphs.append(lg)
            except ConfigurationError as ce:
                errors.append(str(ce))

        result.append(LoadedBlueprint(
            name=bp_name,
            path=bp_cfg.path,
            description=bp_cfg.description,
            graphs=loaded_graphs
        )
        )

    if errors:
        raise ConfigurationError("Configuration errors:\n" + "\n".join(errors))

    return result
