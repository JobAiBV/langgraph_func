# Graph Structure Basics

This library expects each LangGraph file to expose three things:

1. `Input` – a Pydantic model describing the input state.
2. `Output` – a Pydantic model describing the output state.
3. `compiled_graph` – the compiled `StateGraph` instance.

These names are required so the configuration loader can locate them when building a Function App.

A minimal example is shown below, taken from the test graphs:

```python
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
    return {"update": "ok"}

compiled_graph = (
    StateGraph(input=Input, output=Output)
    .add_node("test", test)
    .add_edge(START, "test")
    .set_finish_point("test")
    .compile(name="test_graph")
)
```

Every graph in your project should follow this pattern so that the YAML loader can import it correctly.

The key takeaway is that **langgraph_func does not change how you write graphs**. You build them exactly as you would when using `langgraph` directly. By keeping the same pattern, any graph can be imported and exposed as an API endpoint or reused as a subgraph in another graph.

When a graph is registered through the YAML configuration it becomes available as a normal Azure Function. Other graphs can call this function via `call_subgraph`, enabling powerful composition and easier debugging.
