import azure.functions as func
from agentpkg.docs_builder import bp_docs
from agentpkg.config.models import FuncAppConfig
from agentpkg.func_app_builder.blueprint_builder import BlueprintBuilder

class FuncAppBuilder:
    """A class to build and register Azure Function blueprints."""

    def __init__(self):
        self._func_app = func.FunctionApp()
        self._func_app.register_functions(bp_docs)  # Register the documentation blueprint

    def register_blueprint(self, blueprint) -> "FuncAppBuilder":
        """
        Adds an endpoint to the blueprint using the provided graph, input, and output models.
        """
        self._func_app.register_functions(blueprint)
        return self

    @property
    def func_app(self):
        """
        Returns the built blueprint.
        """
        return self._func_app
