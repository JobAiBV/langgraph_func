# Helper Functions

Several helpers ship with `langgraph_func` to simplify graph composition and management.

## `AzureFunctionInvoker`

`AzureFunctionInvoker` invokes another Azure Function that exposes a graph, building the payload from the current state. It handles errors automatically by raising `RuntimeError`.

### Usage Example

```python
from langgraph_func.graph_helpers.call_subgraph import AzureFunctionInvoker, FunctionKeySpec
from your_project.settings import settings

subgraph_invoker = AzureFunctionInvoker(
    function_path="test/graphA",
    base_url=settings.function_base_url,
    input_field_map={"input_text": "text"},
    output_field_map={"updates": "child_update"},
    auth_key=FunctionKeySpec.INTERNAL,
)
```

This helper allows any published graph endpoint to be seamlessly reused as a subgraph.

## `skip_if_locked`

Decorate a node with `skip_if_locked("node_name")` to conditionally skip execution based on your state. Ensure your state includes a `locked_nodes` list. If the node's name is present in `locked_nodes`, the function returns an empty dictionary, and the graph execution continues without running that node.

### Usage Example

```python
from langgraph_func.decorators import skip_if_locked
from langgraph_func.graph_helpers.call_subgraph import AzureFunctionInvoker, FunctionKeySpec
from your_project.settings import settings

education_agent_invoker = AzureFunctionInvoker(
    function_path="education_agent",
    base_url=settings.function_base_url,
    input_field_map={"vacancy_text": "vacancy_text"},
    auth_key=FunctionKeySpec.INTERNAL,
)

@skip_if_locked("education_agent")
def subgraph_wrapper_education(state: MergedState) -> dict:
    return education_agent_invoker(state)
```

