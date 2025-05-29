from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List
from collections import defaultdict
import json, zlib, base64

def mermaid_live_link(code: str, theme: str = "default") -> str:
    payload = json.dumps(
        {"code": code, "mermaid": {"theme": theme}},
        separators=(",", ":"),
    ).encode()
    compressed = zlib.compress(payload, level=9)
    token = base64.urlsafe_b64encode(compressed).decode()
    return f"https://mermaid.live/edit#pako:{token}"

@dataclass(frozen=True, slots=True)
class Endpoint:
    name: str
    path: str
    methods: List[str]
    auth_level: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    mermaid: str
    description: str
    blueprint: str
    blueprint_description: str

    def with_titled_schemas(self) -> Endpoint:
        """Return a copy with 'title' keys added to schemas."""
        inp = {**self.input_schema,  "title": f"{self.name}_Input"}
        out = {**self.output_schema, "title": f"{self.name}_Output"}
        return Endpoint(
            name=self.name,
            path=self.path,
            methods=self.methods,
            auth_level=self.auth_level,
            input_schema=inp,
            output_schema=out,
            mermaid=self.mermaid,
            description=self.description,
            blueprint=self.blueprint,
            blueprint_description=self.blueprint_description,
        )

    def to_operation(self, method: str) -> Dict[str, Any]:
        in_ref = f"#/components/schemas/{self.input_schema['title']}"
        out_ref = f"#/components/schemas/{self.output_schema['title']}"
        return {
            "tags": [self.blueprint],
            "summary": self.name,
            "description": (
                f"{self.description}\n\n"
                f"[View diagram]({mermaid_live_link(self.mermaid)})"
            ),
            "operationId": self.name,
            "requestBody": {
                "required": True,
                "content": {"application/json": {"schema": {"$ref": in_ref}}},
            },
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {"application/json": {"schema": {"$ref": out_ref}}},
                }
            },
        }

    def to_schemas(self) -> Dict[str, Any]:
        return {
            self.input_schema["title"]: self.input_schema,
            self.output_schema["title"]: self.output_schema,
        }

@dataclass
class APIRegistry:
    endpoints: List[Endpoint] = field(default_factory=list)

    def add(self, ep: Endpoint) -> None:
        self.endpoints.append(ep.with_titled_schemas())

    def build(self, title="Azure-Function LangGraph APIs", version="1.0.0"):
        paths = defaultdict(dict)
        schemas: Dict[str, Any] = {}
        tags: Dict[str, str] = {}

        for ep in self.endpoints:
            # collect schemas
            schemas.update(ep.to_schemas())
            # collect tags
            tags[ep.blueprint] = ep.blueprint_description
            # build one operation per HTTP verb
            for m in ep.methods:
                paths[ep.path][m.lower()] = ep.to_operation(m)

        return {
            "openapi": "3.1.0",
            "info": {"title": title, "version": version},
            "tags": [
                {"name": name, "description": desc}
                for name, desc in tags.items()
            ],
            "paths": dict(paths),
            "components": {
                "schemas": schemas,
                "securitySchemes": {}  # fill as you like
            },
        }

# usage:
registry = APIRegistry()
