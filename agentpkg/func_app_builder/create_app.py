from agentpkg.config.loader import load_funcapp_config
from agentpkg.func_app_builder.blueprint_builder import BlueprintBuilder
from agentpkg.func_app_builder.func_app_builder import FuncAppBuilder

def create_app_from_yaml(config_path: str):
    """
    Loads and validates your YAML config, then builds and returns
    the Azure Functions app with all blueprints registered.
    """
    loaded_blueprints = load_funcapp_config(config_path)
    app_builder = FuncAppBuilder()

    for bp in loaded_blueprints:
        for lg in bp.graphs:
            bb = (
                BlueprintBuilder(path=bp.path, description = bp.description, name=bp.name)
                .add_endpoint(
                    name=f"{bp.name}_{lg.name}", # prevent duplication
                    path=lg.path,
                    graph=lg.compiled_graph,
                    input_type=lg.input,
                    output_type=lg.output,
                    auth_level=lg.auth,
                    description= lg.description
                )
            )
            bb.blueprint.route_prefix = f"/{bp.name}/{lg.path}"
            app_builder.register_blueprint(bb.blueprint)

    return app_builder.func_app