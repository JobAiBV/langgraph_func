from sys import prefix
from typing import Type

from langgraph_func.graph_endpoints.graph_executor_factory import EndpointGenerator
import azure.functions as func
from langgraph_func.types import TInput, TOutput
from langgraph.graph.state import CompiledStateGraph

class BlueprintBuilder:
    """A class to build and register Azure Function blueprints."""

    def __init__(self, path: str, description: str, name: str):
        self.blueprint_path = path
        self._blueprint = func.Blueprint()
        self._description = description
        self._name = name

    def add_endpoint(self,
                     name: str,
                     path: str,
                     graph: CompiledStateGraph,
                     input_type: Type[TInput],
                     output_type: Type[TOutput],
                     description: str,
                     auth_level: func.AuthLevel = func.AuthLevel.ANONYMOUS,

                     ) -> "BlueprintBuilder":
        """
        Adds an endpoint to the blueprint using the provided graph, input, and output models.
        """
        EndpointGenerator(
            blueprint=self._blueprint,
            graph=graph,
            input_model=input_type,
            output_model=output_type,
            auth_level=auth_level,
            description=description,
            blueprint_description=self._description,
            blueprint_name = self._name
        ).generate_and_register(name, ["POST"], f"{self.blueprint_path}/{path}")
        return self

    @property
    def blueprint(self):
        """
        Returns the built blueprint.
        """
        return self._blueprint