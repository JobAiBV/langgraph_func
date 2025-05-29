# Building Function Apps

Use `FuncAppBuilder` to configure your Azure Function app along with all settings.
The builder automatically registers a blueprint serving OpenAPI documentation at
`/api/docs` and `/api/openapi.json`.

```python
from grapi import FuncAppBuilder
from grapi.graph_endpoints import EndpointGenerator

builder = FuncAppBuilder()
app = builder.build()

# register additional blueprints
builder.add_blueprint(my_blueprint)
```
