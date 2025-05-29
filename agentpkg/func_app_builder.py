import azure.functions as func
from .config import Settings
from .logger import get_logger
from .docs_function import bp_docs

class FuncAppBuilder:
    """Utility to build an Azure Functions app with configured settings."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.logger = get_logger(__name__)
        self.app = func.FunctionApp(
            http_auth_level=self.settings.get_auth_level()
        )
        # register documentation endpoints automatically
        self.add_blueprint(bp_docs)

    def add_blueprint(self, bp: func.Blueprint) -> "FuncAppBuilder":
        """Register a blueprint on the underlying FunctionApp."""
        self.logger.debug("Registering blueprint %s", bp.name)
        self.app.register_blueprint(bp)
        return self

    def build(self) -> func.FunctionApp:
        """Return the configured FunctionApp."""
        return self.app
