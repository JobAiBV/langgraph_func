# parent_graph.py

from pydantic import BaseModel
from typing import Optional
from langgraph.graph import StateGraph, START
from langgraph_func.graph_helpers.call_subgraph import AzureFunctionInvoker
from langgraph_func.graph_helpers.call_subgraph import FunctionKeySpec
from .settings import settings

class Input(BaseModel):
    input_text: str

class Output(BaseModel):
    child_update: Optional[str] = None

# create one invoker instance
subgraph = AzureFunctionInvoker(
    function_path="blueprint_a/graphA",
    base_url=settings.function_base_url,
    input_field_map={"input_text": "text"},
    output_field_map={"updates": "child_update"},
    auth_key=FunctionKeySpec.INTERNAL,
)


compiled_graph = (
    StateGraph(input=Input, output=Output)
      .add_node("call_graphA", subgraph)
      .add_edge(START, "call_graphA")
      .set_finish_point("call_graphA")
      .compile()
)
