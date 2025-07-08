# Building Function Apps

The easiest way to run your graphs is by creating a small `function_app.py` module that builds the Azure Functions app.  Use `create_app_from_yaml` to load your configuration and register all graphs as HTTP triggers.

```python
from langgraph_func.func_app_builder.create_app import create_app_from_yaml

app = create_app_from_yaml("function-app.yml")
```

Place this file in the root of your Functions project. When you start the Azure Functions host (`func start --python`) the app will expose one route per graph as well as Swagger documentation under `/api/docs` and `/api/openapi.json`.

During development you can run the host locally to debug your graphs just as you would with plain `langgraph` code.
