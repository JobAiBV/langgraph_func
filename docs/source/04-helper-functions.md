# Helper Functions

Several helpers ship with `langgraph_func` to make graph composition straightforward.

## `call_subgraph`

`call_subgraph` invokes another Azure Function that exposes a graph. The payload is built from the current state and any errors are automatically raised as `RuntimeError`.

```python
def test(state: MergedState) -> dict:
    output = call_subgraph(
        state=state,
        function_path="test/graphA",
        payload_builder=lambda s: {"input_text": s.input_text},
        base_url=settings.function_base_url,
        function_key=FunctionKeySpec.INTERNAL,
    )
    return {"child_update": output["update"]}
```

With this helper every graph published by `langgraph_func` can be reused as a subgraph by simply calling its HTTP endpoint.

## `skip_if_locked`

Decorate a node with `skip_if_locked("node_name")` and include a `locked_nodes` list in your state. If the node name is present, the function returns an empty dictionary and the graph continues without executing that step.

```python
@skip_if_locked("<AGENT_NAME>")
def subgraph_wrapper_education(state: MergedState) -> dict:
    return call_subgraph(
        base_url=settings.function_base_url,
        state=state,
        function_path="education_agent",
        payload_builder=lambda s: {"vacancy_text": s.vacancy_text},
        function_key=FunctionKeySpec.INTERNAL,
    )
```

These utilities keep your graphs flexible and promote a clean separation of concerns.
