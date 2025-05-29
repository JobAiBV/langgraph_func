# Building a Function App from YAML

The easiest way to host your graphs is to describe them in a YAML file and load it with `create_app_from_yaml`.
Below is a minimal configuration:

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

Save this file (for example `function-app.yml`) and create the app:

```python
from langgraph_func.func_app_builder.create_app import create_app_from_yaml

app = create_app_from_yaml("function-app.yml")
```

`create_app_from_yaml` internally loads the configuration, builds the blueprints and registers all endpoints:

```python
loaded_blueprints, loaded_swagger = load_funcapp_config(config_path)
app_builder = FuncAppBuilder().add_docs(
    title=loaded_swagger.title,
    auth_level=loaded_swagger.auth,
    version=loaded_swagger.version,
    ui_route=loaded_swagger.ui_route,
)
# ...register graphs...
```

Run your Azure Functions host and your API will expose routes under `/api` with automatically generated Swagger documentation.
