from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List
import base64
import json
import zlib
from collections import defaultdict

def mermaid_live_link(code: str, theme: str = "default") -> str:
    payload = json.dumps({"code": code, "mermaid": {"theme": theme}}, separators=(",", ":")).encode()
    compressed = zlib.compress(payload, level=9)
    encoded = base64.urlsafe_b64encode(compressed).decode()
    return f"https://mermaid.live/edit#pako:{encoded}"


@dataclass(frozen=True, slots=True)
class Endpoint:
    name: str
    path: str
    methods: List[str]
    auth_level: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    mermaid: str

    # new fields
    description: str                # human-readable description of this operation
    blueprint: str                  # name of the blueprint this endpoint belongs to
    blueprint_description: str      # human-readable description of that blueprint

    def dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class APIRegistry:
    endpoints: List[Endpoint] = field(default_factory=list)

    def add(self, endpoint: Endpoint) -> None:
        # add title metadata
        input_schema = endpoint.input_schema.copy()
        output_schema = endpoint.output_schema.copy()
        input_schema["title"] = f"{endpoint.name}_Input"
        output_schema["title"] = f"{endpoint.name}_Output"

        # carry through the new description & blueprint info
        updated_ep = Endpoint(
            name=endpoint.name,
            path=endpoint.path,
            methods=endpoint.methods,
            auth_level=endpoint.auth_level,
            input_schema=input_schema,
            output_schema=output_schema,
            mermaid=endpoint.mermaid,
            description=endpoint.description,
            blueprint=endpoint.blueprint,
            blueprint_description=endpoint.blueprint_description,
        )
        self.endpoints.append(updated_ep)

    def list(self) -> List[Dict[str, Any]]:
        return [e.dict() for e in self.endpoints]

    def _create_operation(self, endpoint: Endpoint, method: str) -> Dict[str, Any]:
        in_ref = f"#/components/schemas/{endpoint.input_schema['title']}"
        out_ref = f"#/components/schemas/{endpoint.output_schema['title']}"

        # use endpoint.description here
        operation = {
            "tags": [endpoint.blueprint],
            "summary": endpoint.name,
            "description": endpoint.description + "\n\n" +
                           f"[View diagram]({mermaid_live_link(endpoint.mermaid)})",
            "operationId": endpoint.name,
            "requestBody": {
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"$ref": in_ref}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": out_ref}
                        }
                    }
                }
            }
        }

        return operation

    def build_openapi(
        self,
        title: str = "Azure-Function LangGraph APIs",
        version: str = "1.0.0"
    ) -> Dict[str, Any]:
        paths = defaultdict(dict)
        components: Dict[str, Any] = {"schemas": {}, "securitySchemes": {}}

        # collect unique blueprint tags
        tag_map: Dict[str, str] = {}

        for endpoint in self.endpoints:
            # add schemas
            components["schemas"][endpoint.input_schema["title"]] = endpoint.input_schema
            components["schemas"][endpoint.output_schema["title"]] = endpoint.output_schema

            # track unique blueprint name → description
            tag_map[endpoint.blueprint] = endpoint.blueprint_description

            # build operations under their path
            for method in endpoint.methods:
                op = self._create_operation(endpoint, method)
                paths[endpoint.path][method.lower()] = op

        # build top-level tags list
        tags = [{"name": name, "description": desc} for name, desc in tag_map.items()]

        return {
            "openapi": "3.1.0",
            "info": {
                "title": title,
                "version": version,
            },
            "tags": tags,
            "paths": dict(paths),
            "components": components
        }


registry = APIRegistry()
