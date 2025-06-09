import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langgraph_func.func_app_builder.create_app import create_app_from_yaml

app = create_app_from_yaml("function-app.yml")
