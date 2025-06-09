from typing import TypeVar, Type, List, Generic
from pydantic import BaseModel

from langgraph.graph.state import CompiledStateGraph
from langgraph_func.logger import get_logger
from langgraph_func.types import TInput, TOutput
logger = get_logger()


class GraphExecutorService(Generic[TInput, TOutput]):
    def __init__(self, graph: CompiledStateGraph, output_model: Type[TOutput]):
        self.graph = graph
        self.output_model = output_model

    async def execute(self, input_data: TInput) -> TOutput:
        logger.debug(f"Running graph '{self.graph.name}' with input: {input_data}")
        result = await self.graph.ainvoke(input_data)
        return self.output_model(**result) if result else self.output_model()
