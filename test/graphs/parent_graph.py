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
graphA_node = AzureFunctionInvoker[Input](
    function_path="blueprint_a/graphA",
    base_url=settings.function_base_url,
    payload_builder=lambda s: {"input_text": s.input_text},
    function_key=FunctionKeySpec.INTERNAL,
    timeout=10.0
)

compiled_graph = (
    StateGraph(input=Input, output=Output)
      # pass the invoker directly—LangGraph will `await graphA_node(state)`
      .add_node("call_graphA", graphA_node)
      .add_edge(START, "call_graphA")
      .set_finish_point("call_graphA")
      .compile()
)
