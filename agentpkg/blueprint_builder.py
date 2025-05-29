from typing import Type

from agentpkg.graph_endpoints.graph_executor_factory import EndpointGenerator
import azure.functions as func
from agentpkg.types import TInput, TOutput
from langgraph.graph.state import CompiledStateGraph

class BlueprintBuilder:
    """A class to build and register Azure Function blueprints."""

    def __init__(self):
        self._blueprint = func.Blueprint()

    def validate_input(self, graph: CompiledStateGraph, input_type: Type[TInput]) -> "BlueprintBuilder":
        if graph.name is "LangGraph":
            raise ValueError("Graph name cannot be 'LangGraph'. Please provide a valid graph name by setting name in compiled graph")

    def add_endpoint(self,
                     graph: CompiledStateGraph,
                     input_type: Type[TInput],
                     output_type: Type[TOutput],
                     auth_level: func.AuthLevel = func.AuthLevel.ANONYMOUS
                     ) -> "BlueprintBuilder":
        """
        Adds an endpoint to the blueprint using the provided graph, input, and output models.
        """
        self.validate_input(graph, input_type)
        EndpointGenerator(
            blueprint=self._blueprint,
            graph=graph,
            input_model=input_type,
            output_model=output_type,
            auth_level=auth_level
        ).generate_and_register(graph.name, ["POST"])
        return self

    @property
    def blueprint(self):
        """
        Returns the built blueprint.
        """
        return self._blueprint