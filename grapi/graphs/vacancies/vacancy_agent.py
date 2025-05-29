from grapi.logger import get_logger
from pydantic import BaseModel
from langgraph.graph import StateGraph, START
from grapi.graph_helpers.call_subgraph import call_subgraph, FunctionKeySpec
from grapi.settings import settings
from typing import Optional

from grapi.graph_helpers.wrappers import skip_if_locked

logger = get_logger()
# Define the input and output schemas
class Input(BaseModel):
    vacancy_text: str
    locked_nodes: list[str] = []


class Output(BaseModel):
    function_titles: Optional[list[str]] = None
    potential_function_titles: Optional[list[str]] = None
    final_education_verdict: Optional[list[str]] = None
    final_level: Optional[str] = None
    accepted: Optional[bool] = None


class MergedState(Input, Output):
    pass



@skip_if_locked("func_title_extractor")
def subgraph_wrapper_extractor(state: MergedState) -> dict:
    """
    Wrapper function to invoke the subgraph (func_title_extractor) via Azure Function.
    """
    return call_subgraph(
        base_url=settings.function_base_url,
        state=state,
        function_path="func_title_extractor",
        payload_builder=lambda s: {"vacancy_text": s.vacancy_text},
        function_key=FunctionKeySpec.INTERNAL
    )

@skip_if_locked("education_agent")
def subgraph_wrapper_education(state: MergedState) -> dict:
    """
    Wrapper function to invoke the subgraph (func_title_extractor) via Azure Function.
    """
    return call_subgraph(
        base_url=settings.function_base_url,
        state=state,
        function_path="education_agent",
        payload_builder=lambda s: {"vacancy_text": s.vacancy_text},
        function_key=FunctionKeySpec.INTERNAL
    )



# Build the graph
compiled_graph = StateGraph(input = Input, output = Output)\
    .add_node("extract_title", subgraph_wrapper_extractor)\
    .add_node("education", subgraph_wrapper_education)\
    .add_edge(START, "extract_title")\
    .add_edge(START, "education")\
    .set_finish_point("extract_title") \
    .set_finish_point("education") \
    .compile()