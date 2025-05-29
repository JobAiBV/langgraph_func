# Helper Functions

Several small helpers make it easier to build graphs.

## `call_subgraph`

Use this function to invoke another Azure Function that exposes a graph. It builds the payload from your current state and handles errors for you.

```python
result = call_subgraph(
    state=my_state,
    function_path="func_title_extractor",
    payload_builder=lambda s: {"vacancy_text": s.vacancy_text},
    base_url=settings.function_base_url,
    function_key=FunctionKeySpec.INTERNAL,
)
```

If the remote function returns an error, `call_subgraph` raises a `RuntimeError`.

## `skip_if_locked`

Sometimes you want to skip a node when running a graph. Decorate the node function with `skip_if_locked("node_name")` and include a `locked_nodes` list in your state. If the name is present, the node simply returns an empty dictionary.

```python
@skip_if_locked("education_agent")
def subgraph_wrapper_education(state: MergedState) -> dict:
    return call_subgraph(
        base_url=settings.function_base_url,
        state=state,
        function_path="education_agent",
        payload_builder=lambda s: {"vacancy_text": s.vacancy_text},
        function_key=FunctionKeySpec.INTERNAL,
    )
```

This makes your graphs flexible without scattering conditional logic throughout your code.
