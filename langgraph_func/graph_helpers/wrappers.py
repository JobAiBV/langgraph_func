import inspect
import asyncio
from functools import wraps
from pydantic import BaseModel, ValidationError
import azure.functions as func
from langgraph_func.logger import get_logger

logger = get_logger()
import json

def validate_body(model: type[BaseModel]):
    """
    Decorator that synchronously validates req.get_body() against the given Pydantic model,
    then invokes the wrapped function. If the wrapped function returns a coroutine,
    it's executed via asyncio.run. Ensures compatibility with Azure Functions sync handlers.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(req: func.HttpRequest, *args, **kwargs):
            # Validate request body
            try:
                validated = model.model_validate_json(req.get_body())
                logger.debug(f"Request body: {validated}")
                req.validated_body = validated
            except ValidationError as e:
                logger.error(f"Validation error: {e.json()}")
                return func.HttpResponse(
                    e.json(),
                    status_code=422,
                    mimetype="application/json"
                )
            # Call the wrapped function
            result = fn(req, *args, **kwargs)
            # If the handler is async, run it to completion
            if inspect.iscoroutine(result):
                return asyncio.run(result)
            return result
        return wrapper
    return decorator

def skip_if_locked(node_name: str):
    """
    Check the state.input if the current node is locked. If so return empty dict otherwise return output of the function
    """
    def decorator(func):
        def wrapper(state: BaseModel):
            if not hasattr(state, 'locked_nodes'):
                raise AttributeError("State does not have 'locked_nodes' attribute.")
            if node_name in state.locked_nodes:
                logger.info(f"Node '{node_name}' is locked, skipping.")
                return {}

            return func(state)
        return wrapper
    return decorator
