import importlib
import yaml
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass
from dacite import from_dict
from langgraph_func.logger import get_logger
from azure.functions import AuthLevel
from langgraph.graph.state import CompiledStateGraph
from langgraph_func.yml_config.models import (
    GraphConfig,
    BlueprintConfig,
    FuncAppConfig,
    SwaggerConfig,
)

logger = get_logger(__name__)


class ConfigurationError(Exception):
    """Raised when the YAML yml_config is invalid or missing required attributes."""


# ─────────────────────────────────────────────────────────────────────────────
# 1) Loaded-model dataclasses
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class LoadedGraph:
    name: str
    path: str
    auth: AuthLevel            # strongly typed
    input: Any
    output: Any
    compiled_graph: CompiledStateGraph
    description: str


@dataclass
class LoadedBlueprint:
    name: str
    path: str
    description: str
    graphs: List[LoadedGraph]


@dataclass
class LoadedSwagger:
    title: str
    auth: AuthLevel
    version: str
    ui_route: str


# ─────────────────────────────────────────────────────────────────────────────
# 2) GraphLoader stays the same
# ─────────────────────────────────────────────────────────────────────────────

class GraphLoader:
    @staticmethod
    def load(name: str, cfg: GraphConfig) -> LoadedGraph:
        logger.debug(f"The name is {name} and the yml_config is {cfg!r}")
        try:
            module = importlib.import_module(cfg.source)
        except ImportError as e:
            raise ConfigurationError(f"[{name}] cannot import '{cfg.source}': {e}")

        def fetch(attr_name: str) -> Any:
            if not hasattr(module, attr_name):
                raise ConfigurationError(
                    f"[{name}] module '{cfg.source}' is missing '{attr_name}'"
                )
            return getattr(module, attr_name)

        Input  = fetch(cfg.input_attr)
        Output = fetch(cfg.output_attr)
        cg     = fetch(cfg.graph_attr)

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


# ─────────────────────────────────────────────────────────────────────────────
# 3) load_funcapp_config now returns (List[LoadedBlueprint], LoadedSwagger)
# ─────────────────────────────────────────────────────────────────────────────

def load_funcapp_config(path: str) -> Tuple[List[LoadedBlueprint], LoadedSwagger]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # Deserialize into your dataclasses
    try:
        cfg = from_dict(data_class=FuncAppConfig, data=raw)
    except Exception as e:
        raise ConfigurationError(f"Invalid YAML structure: {e}")

    # ** Build the LoadedSwagger **
    sw = cfg.swagger
    # normalize + validate auth_level
    auth_name = (
        sw.auth_level.name
        if isinstance(sw.auth, AuthLevel)
        else str(sw.auth).strip().upper()
    )
    if auth_name not in AuthLevel.__members__:
        valid = ", ".join(AuthLevel.__members__.keys())
        raise ConfigurationError(
            f"[swagger] invalid auth_level '{sw.auth_level}'. Must be one of: {valid}"
        )
    loaded_swagger = LoadedSwagger(
        title=sw.title,
        version=sw.version,
        auth=AuthLevel[auth_name],
        ui_route=sw.ui_route,
    )

    # ** Build the blueprints **
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
        ))

    if errors:
        raise ConfigurationError("Configuration errors:\n" + "\n".join(errors))

    return result, loaded_swagger
