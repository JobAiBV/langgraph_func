import json
import azure.functions as func
from langgraph_func.graph_endpoints.registry import registry
from pathlib import Path
from langgraph_func.settings import settings
def register_swagger_routes(
    bp: func.Blueprint,
    *,
    title: str,
    version: str,
    auth_level: func.AuthLevel,
    ui_route: str
) -> None:
    """
    Registers two HTTP-triggered Azure Functions on the given Blueprint:
     - GET /{json_route}    -> returns OpenAPI JSON
     - GET /{ui_route}      -> returns Swagger UI HTML

    :param bp:          azure.functions.Blueprint instance
    :param title:       Title to pass into registry.build_openapi()
    :param version:     Version to pass into registry.build_openapi()
    :param auth_level:  Function auth level for both endpoints
    :param json_route:  URL path for the OpenAPI JSON
    :param ui_route:    URL path for the Swagger UI
    :param swagger_html_filename: name of the HTML file in the same folder
    """
    json_route = settings.json_route
    fn_name_json = f"serve_{json_route.replace('.', '_')}"
    fn_name_ui = f"serve_{ui_route}"

    # OpenAPI JSON endpoint
    @bp.function_name(fn_name_json)
    @bp.route(route=json_route, methods=["GET"], auth_level=auth_level)
    async def _serve_openapi(req: func.HttpRequest) -> func.HttpResponse:  # noqa: F811
        spec = registry.build(title=title, version=version)
        return func.HttpResponse(
            json.dumps(spec, indent=2), status_code=200, mimetype="application/json"
        )

    # Swagger UI HTML endpoint
    @bp.function_name(fn_name_ui)
    @bp.route(route=ui_route, methods=["GET"], auth_level=auth_level)
    async def _serve_swagger_ui(req: func.HttpRequest) -> func.HttpResponse:  # noqa: F811
        html_path = Path(__file__).parent / settings.swagger_html_file
        if not html_path.exists():
            return func.HttpResponse("Swagger HTML not found", status_code=500)
        return func.HttpResponse(
            html_path.read_text(encoding="utf-8"),
            status_code=200,
            mimetype="text/html",
        )
