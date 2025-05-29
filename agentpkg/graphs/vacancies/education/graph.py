from pydantic import BaseModel
from typing import List, Dict
from langgraph.graph import StateGraph, START, END
from agentpkg.prompt_templates.clean_output import RETURN_VALID_JSON
from langchain.chat_models import ChatOpenAI
from agentpkg.graph_helpers.graph_builder_helpers import parse_json
from typing import List, Optional
from agentpkg.logger import get_logger
from agentpkg.graphs.vacancies.education.prompts import (
    EXPLICIT_PROMPT,
    IMPLICIT_PROMPT,
    QUALIFICATION_PROMPT,
    NEGATION_PROMPT,
    CONTEXT_PROMPT,
    COMBINE_PROMPT,
)


logger = get_logger()
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


class Input(BaseModel):
    vacancy_text: str



class Output(BaseModel):
    explicit_education: Optional[List[str]] = None
    implicit_education: Optional[List[str]] = None
    qualification_education: Optional[List[str]] = None
    negation_detected: Optional[List[str]] = None
    context_estimation: Optional[List[str]] = None
    final_education_verdict: Optional[List[str]] = None
    summary: Optional[str] = None
    final_level: Optional[str] = None


class MergedState(Input, Output):
    pass


def extract_explicit_education_node(state: MergedState) -> Dict:
    messages = EXPLICIT_PROMPT.format_messages(
        vacancy=state.vacancy_text,
        valid_json=RETURN_VALID_JSON
    )
    response = llm.invoke(messages)
    return parse_json( response.content)


def extract_implicit_education_node(state: MergedState) -> Dict:
    messages = IMPLICIT_PROMPT.format_messages(
        vacancy=state.vacancy_text,
        valid_json=RETURN_VALID_JSON
    )
    response = llm.invoke(messages)
    return parse_json( response.content)



def extract_qualification_education_node(state: MergedState) -> Dict:
    messages = QUALIFICATION_PROMPT.format_messages(
        vacancy=state.vacancy_text,
        valid_json=RETURN_VALID_JSON
    )
    response = llm.invoke(messages)
    return parse_json( response.content)



def extract_negation_exception_node(state: MergedState) -> Dict:
    messages = NEGATION_PROMPT.format_messages(
        vacancy=state.vacancy_text,
        valid_json=RETURN_VALID_JSON
    )
    response = llm.invoke(messages)
    return parse_json( response.content)



def estimate_context_education_node(state: MergedState) -> Dict:
    messages = CONTEXT_PROMPT.format_messages(
        vacancy=state.vacancy_text,
        valid_json=RETURN_VALID_JSON
    )
    response = llm.invoke(messages)
    return parse_json( response.content)



def combine_education_input_node(state: MergedState) -> Dict:
    messages = COMBINE_PROMPT.format_messages(
        explicit=state.explicit_education,
        implicit=state.implicit_education,
        qualification=state.qualification_education,
        negation=state.negation_detected,
        context=state.context_estimation,
        valid_json=RETURN_VALID_JSON
    )
    response = llm.invoke(messages)
    data = parse_json( response.content)
    return {
            "final_education_verdict": [data["summary"], data["final_level"]],
            "summary": data["summary"],
            "final_level": data["final_level"]
}


compiled_graph = (
    StateGraph(input=Input, output=Output)
    .add_node("explicit", extract_explicit_education_node)
    .add_node("implicit", extract_implicit_education_node)
    .add_node("qualification", extract_qualification_education_node)
    .add_node("negation", extract_negation_exception_node)
    .add_node("context_estimation2", estimate_context_education_node)
    .add_node("combine", combine_education_input_node)
    .set_entry_point("explicit")
    .add_edge(START, "explicit")
    .add_edge("explicit", "implicit")
    .add_edge("implicit", "qualification")
    .add_edge("qualification", "negation")
    .add_edge("negation", "context_estimation2")
    .add_edge("context_estimation2", "combine")
    .add_edge("combine", END)
    .compile()
)
