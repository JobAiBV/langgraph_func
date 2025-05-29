# Building a Function App from YAML

The `langgraph_func` package reads a simple YAML file that lists your blueprints and graphs. Each entry points to a Python module containing the regular LangGraph definition. This approach keeps your graph code untouched while making it easy to expose as HTTP endpoints.

An example configuration looks like:

```yaml
swagger:
  title: Demo Function App
  version: 1.0.0
  auth: FUNCTION
  ui_route: docs

blueprints:
  v1:
    path: v1
    description: Example blueprint
    graphs:
      vacancy_agent:
        path: vacancy
        source: langgraph_func.graphs.vacancies.vacancy_agent
        auth: FUNCTION
        description: Extracts vacancy information
```

Each graph entry specifies the route (`path`), the module to import (`source`), the authentication level and a description used for the generated documentation.

Once the file is saved (e.g. `function-app.yml`) you can load it and start the app:

```python
from langgraph_func.func_app_builder.create_app import create_app_from_yaml

app = create_app_from_yaml("function-app.yml")
```

Internally `create_app_from_yaml` validates the YAML, builds a `BlueprintBuilder` for each blueprint and registers the graphs as Azure Functions. Swagger documentation is generated automatically from the dataclasses in the YAML file and the Pydantic models exported by your graphs.

Running the Functions host will serve the API under `/api`. Each graph can also be invoked by other graphs using `call_subgraph`, which makes them fully reusable components.
