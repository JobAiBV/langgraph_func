from pydantic import BaseModel
from langgraph.graph import StateGraph, START

from typing import Optional


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