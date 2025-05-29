# Building Function Apps

Use `FuncAppBuilder` to configure your Azure Function app along with all settings.
The builder automatically registers a blueprint serving OpenAPI documentation at
`/api/docs` and `/api/openapi.json`.

```python
from langgraph_api.func_app_builder.create_app import create_app_from_yaml

app = create_app_from_yaml("function-app.yml")

```
Make sure that the file is called *function_app.py* and is located in the root of your Azure Functions project.


Run func start --p 7072 --python
