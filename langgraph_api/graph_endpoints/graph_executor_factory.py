from typing import TypeVar, Type, List, Generic
import json
import azure.functions as func
from pydantic import BaseModel

from langgraph.graph.state import CompiledStateGraph
from langgraph_func.graph_helpers.wrappers import validate_body
from langgraph_func.graph_endpoints.registry import Endpoint, registry
from langgraph_func.logger import get_logger
from langgraph_func.graph_endpoints.graph_executor_service import GraphExecutorService
from langgraph_func.graph_helpers.call_subgraph import FUNCTION_KEY
logger = get_logger()

TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class EndpointGenerator(Generic[TInput, TOutput]):
    """
    Generates and registers an extraction endpoint on a given blueprint.
    Usage:
        gen = EndpointGenerator(blueprint, graph, InModel, OutModel)
        gen.generate_and_register("summarize", ["POST"]) \
           .generate_and_register("translate", ["POST"])
    """

    def __init__(
        self,
        blueprint,
        graph: CompiledStateGraph,
        input_model: Type[TInput],
        output_model: Type[TOutput],
        auth_level: func.AuthLevel,
        description: str,
        blueprint_description: str,
        blueprint_name: str
    ):
        self.blueprint = blueprint
        self.graph = graph
        self.input_model = input_model
        self.output_model = output_model
        self.auth_level = auth_level
        self.description = description
        self.blueprint_description = blueprint_description
        self._service = GraphExecutorService[TInput, TOutput](graph, output_model)
        self.blueprint_name = blueprint_name

    def _create_route(self, name: str, methods: List[str], path: str) -> func.HttpRequest:
        logger.debug(f"Defining HTTP route handler for '{name}'")

        @self.blueprint.function_name(name=name)
        @self.blueprint.route(
            route=path,
            methods=methods,
            auth_level=self.auth_level
        )
        @validate_body(self.input_model)
        async def handle_extraction_request(req: func.HttpRequest) -> func.HttpResponse:
            code = req.params.get("code")
            token_key = FUNCTION_KEY.set(code)
            try:
                body = req.validated_body
                logger.debug(f"{name} - Received body: {body}")
                result = await self._service.execute(body)
                logger.debug(f"{name} - Extraction result: {result}")
                return func.HttpResponse(
                    result.model_dump_json(),
                    status_code=200,
                    mimetype="application/json"
                )
            except Exception as e:
                logger.error(f"{name} - Error during extraction: {e}")
                return func.HttpResponse(
                    json.dumps({"error": str(e)}),
                    status_code=500,
                    mimetype="application/json"
                )
            finally:
                FUNCTION_KEY.reset(token_key)

        return handle_extraction_request

    def _register(self, name: str, methods: List[str], path: str) -> None:
        logger.debug(f"Registering endpoint '{name}' in API registry")
        registry.add(
            Endpoint(
                name=name,
                path=f"/api/{path}",
                methods=methods,
                auth_level=self.auth_level.name if hasattr(self.auth_level, "name") else str(self.auth_level),
                input_schema=self.input_model.model_json_schema(),
                output_schema=self.output_model.model_json_schema(),
                mermaid=self.graph.get_graph().draw_mermaid(with_styles=False),
                description=self.description,
                blueprint=self.blueprint_name,
                blueprint_description=self.blueprint_description
            )
        )

    def generate_and_register(self,
                              name: str,
                              methods: List[str],
                              path: str
                              ) -> "EndpointGenerator":
        """
        Create the decorated Azure Function route *and* register it.
        Returns self to allow chaining.
        """
        self._create_route(name, methods, path)
        self._register(name, methods, path)
        return self
