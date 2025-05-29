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
