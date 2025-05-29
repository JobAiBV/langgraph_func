
from pydantic import BaseModel
from langgraph.graph import StateGraph, START
import azure.functions as func

from typing import Optional

from agentpkg import FuncAppBuilder, BlueprintBuilder


class Input(BaseModel):
    input_text: str


class Output(BaseModel):
    update: Optional[str] = None


class MergedState(Input, Output):
    pass



def test(state: MergedState) -> dict:
    """
    Wrapper function to invoke the subgraph (func_title_extractor) via Azure Function.
    """
    return {
        "update": "ok"
    }


# Build the graph
compiled_graph = StateGraph(input = Input, output = Output)\
    .add_node("test", test)\
    .add_edge(START, "test")\
    .set_finish_point("test") \
    .compile(name="test_graph")

def create_app() -> FuncAppBuilder:
    """
    Create and configure the Azure Function App with all necessary blueprints.

    Returns:
        FuncAppBuilder: The configured function app builder.
    """
    app_builder = FuncAppBuilder()
    test_bp = BlueprintBuilder().add_endpoint(
        graph=compiled_graph,
        input_type=Input,  # Replace with actual input type
        output_type=Output,  # Replace with actual output type
        auth_level=func.AuthLevel.ANONYMOUS  # Adjust as necessary
    )

    # Register blueprints
    app_builder.register_blueprint(test_bp.blueprint)

    return app_builder.func_app

app = create_app()