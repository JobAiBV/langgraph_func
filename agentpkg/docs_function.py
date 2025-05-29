import json
import azure.functions as func
from agentpkg.graph_endpoints.registry import registry
from pathlib import Path

bp_docs = func.Blueprint()

@bp_docs.function_name("openapi_json")
@bp_docs.route(route="openapi.json", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
async def serve_openapi(req: func.HttpRequest) -> func.HttpResponse:
    spec = registry.build_openapi(title="Vacancy API", version="1.0.0")
    return func.HttpResponse(
        json.dumps(spec, indent=2),
        status_code=200,
        mimetype="application/json"
    )

@bp_docs.function_name("swagger_ui_docs")
@bp_docs.route(route="docs", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
async def serve_docs(req: func.HttpRequest) -> func.HttpResponse:
    html_path = Path(__file__).parent / "swagger.html"
    if not html_path.exists():
        return func.HttpResponse("Swagger HTML not found", status_code=500)
    return func.HttpResponse(
        html_path.read_text(encoding="utf-8"),
        status_code=200,
        mimetype="text/html"
    )
