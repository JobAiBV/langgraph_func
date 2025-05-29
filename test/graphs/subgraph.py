from pydantic import BaseModel
from langgraph.graph import StateGraph, START
from typing import Optional
from langraph_api.graph_helpers.call_subgraph import call_subgraph,FunctionKeySpec
from .settings import settings

class Input(BaseModel):
    input_text: str


class Output(BaseModel):
    child_update: Optional[str] = None


class MergedState(Input, Output):
    pass



def test(state: MergedState) -> dict:
    """
    Wrapper function to invoke the subgraph (func_title_extractor) via Azure Function.
    """
    output = call_subgraph(
        state=state,
        function_path="blueprint_a/graphA",
        payload_builder=lambda s: {"input_text": s.input_text}, # send the input text as input text to the child
        base_url=settings.function_base_url, # take base_url of own api since it is in same url (change for other func app)
        function_key=FunctionKeySpec.INTERNAL, # use key from parent call as function key

    )
    return {
        "child_update": output["update"]
    }


# Build the graph
compiled_graph = StateGraph(input = Input, output = Output)\
    .add_node("test", test)\
    .add_edge(START, "test")\
    .set_finish_point("test")\
    .compile()