# Building Function Apps

Use `FuncAppBuilder` to configure your Azure Function app along with all settings.

```python
from agentpkg import FuncAppBuilder
from agentpkg.graph_endpoints import EndpointGenerator

builder = FuncAppBuilder()
app = builder.build()

# register additional blueprints
builder.add_blueprint(my_blueprint)
```
