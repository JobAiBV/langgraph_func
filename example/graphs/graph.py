from pydantic import BaseModel
from langgraph.graph import StateGraph, START

from typing import Optional


class Input(BaseModel):
    text: str


class Output(BaseModel):
    updates: Optional[str] = None


class MergedState(Input, Output):
    pass



def test(state: MergedState) -> dict:
    """
    Wrapper function to invoke the subgraph (func_title_extractor) via Azure Function.
    """
    return {
        "updates": state.text * 2
    }


# Build the graph
compiled_graph = StateGraph(input = Input, output = Output)\
    .add_node("test", test)\
    .add_edge(START, "test")\
    .set_finish_point("test") \
    .compile(name="test_graph")