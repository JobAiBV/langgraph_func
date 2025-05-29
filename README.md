`langgraph_func` makes any LangGraph graph available as an Azure Function without changing how you build the graph itself. Every graph can act as a standalone API endpoint or be called as a subgraph from another graph.

Documentation lives in the `docs` folder. The most important topics are:
- [Graph structure](docs/source/01-graph-structure.md)
- [Function app deployment](docs/source/02-deployment.md)
- [YAML configuration](docs/source/03-yaml-function-app.md)
- [Helper functions](docs/source/04-helper-functions.md)


For more info:

You don’t need a separate file on PyPI—PyPI just renders whatever you point it to as your project’s README. With Poetry that’s almost always the `README.md` (or `README.rst`) in the **root** of your repo. So:

1. **Open `README.md` at the project root** (the same one next to `pyproject.toml`).

2. **Add your docs badge/link** at the top, for example:

   ```md
   # langgraph-func

   [![Documentation Status](https://your-org.github.io/langgraph-func/badge.svg)](https://your-org.github.io/langgraph-func/)

   LangGraph Azure Function Agents
   ```

3. (Optional) In `pyproject.toml` explicitly tell Poetry where your README is, so PyPI picks it up:

   ```toml
   [tool.poetry]
   # …
   readme = "README.md"
   ```

4. Commit & bump your version, then re-publish. When PyPI rebuilds the page for that new release it will pull in your updated `README.md`, badge and all.
