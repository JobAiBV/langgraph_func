# langgraph-func

[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://jobaibv.github.io/langgraph_func/)

**Expose LangGraph workflows as Azure Function HTTP endpoints.**

## Installation

```bash
poetry add langgraph_func
```

*Requires Python ≥3.10, LangGraph, Azure Functions SDK.*

## Define a Workflow

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

compiled_graph = StateGraph(input=Input, output=Output) \
    .add_node("test", test) \
    .add_edge(START, "test") \
    .set_finish_point("test") \
    .compile(name="test_graph")
```

## Configuration (function-app.yml)

```yaml
swagger:
  title: Test Function App
  version: 1.0.0-beta
  auth: FUNCTION
  ui_route: docs

blueprints:
  blueprint_a:
    path: blueprint_a
    description: |
      Groups related graphs.
    graphs:
      graphA:
        path: graphA
        source: graphs.graph
        auth: FUNCTION
        description: |
          GraphA ingests raw input.
      parentGraph:
        path: parentGraph
        source: graphs.parent_graph
        auth: FUNCTION
        description: |
          Calls a subgraph from a parent.
```

## Run in Azure Functions

```python
from langgraph_func.func_app_builder.create_app import create_app_from_yaml
app = create_app_from_yaml("function-app.yml")
```

Deploy with `func azure functionapp publish <APP_NAME>`.

## Calling Subgraphs

```python
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
```

## Documentation

See [GitHub Pages](https://jobaibv.github.io/langgraph_func/) for full API reference and examples.
