import azure.functions as func
from azure.functions import AuthLevel

from langgraph_func.docs_builder import register_swagger_routes


class FuncAppBuilder:
    """A class to build and register Azure Function blueprints."""

    def __init__(self):
        self._func_app = func.FunctionApp()

    def add_docs(self,
                 title: str,
                 version: str,
                 auth_level: AuthLevel,
                 ui_route: str
                 ):
        bp_docs = func.Blueprint()
        register_swagger_routes(title= title, bp=bp_docs,version=version, auth_level=auth_level,ui_route=ui_route)
        self._func_app.register_blueprint(bp_docs)
        return self

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
