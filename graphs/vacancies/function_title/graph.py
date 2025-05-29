from typing import List, Dict
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import ChatOpenAI
from agentpkg.graphs.vacancies.function_title.prompts import EXTRACT_PROMPT, SUGGEST_EXTRA_PROMPT, VALIDATE_PROMPT
from agentpkg.graph_helpers.graph_builder_helpers import parse_json
from agentpkg.logger import get_logger
from agentpkg.prompt_templates.clean_output import RETURN_VALID_JSON

logger = get_logger()
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

class Input(BaseModel):
    vacancy_text: str

class Output(BaseModel):
    function_titles: List[str] = None
    potential_function_titles: List[str] = None

class MergedState(Input, Output):
    retries: int = 0


def extract_title_node(state: MergedState) -> Dict:
    logger.info("Extracting main function title.")
    response = llm.invoke(EXTRACT_PROMPT.format_messages(vacancy=state.vacancy_text,valid_json=RETURN_VALID_JSON))
    return parse_json(response.content)

def suggest_extra_titles_node(state: MergedState) -> Dict:
    logger.info("Suggesting additional possible function titles.")
    response = llm.invoke(SUGGEST_EXTRA_PROMPT.format_messages(vacancy=state.vacancy_text,valid_json=RETURN_VALID_JSON))
    return parse_json( response.content)

def validate_titles_node(state: MergedState) -> Dict:
    logger.info("Validating the function titles.")
    response = llm.invoke(VALIDATE_PROMPT.format_messages(
        vacancy=state.vacancy_text,
        titles=state.function_titles,
        suggestions=state.potential_function_titles,
        valid_json=RETURN_VALID_JSON
    ))
    if "FALSE" in response.content.upper() and state.retries < 2:
        logger.warning("Validation failed. Retrying...")
        return {"retries": state.retries + 1}
    logger.info("Validation successful.")
    return {}

# -------------------------------
# Graph (Chained)
# -------------------------------
compiled_graph = (
    StateGraph(input=Input, output=Output)
    .add_node("extract", extract_title_node)
    .add_node("suggest_extra", suggest_extra_titles_node)
    .add_node("validate", validate_titles_node)
    .set_entry_point("extract")
    .add_edge(START, "extract")
    .add_edge("extract", "suggest_extra")
    .add_edge("suggest_extra", "validate")
    .add_conditional_edges(
        "validate",
        lambda state: "validate" if state.retries < 2 and len(state.function_titles) == 0 else END,
        {
            "validate": "extract",
            END: END
        }
    )
    .set_finish_point("validate")  # <-- FIXED THIS LINE
    .compile()
)



