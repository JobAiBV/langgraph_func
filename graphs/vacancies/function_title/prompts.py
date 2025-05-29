from langchain.prompts import ChatPromptTemplate



EXTRACT_PROMPT = ChatPromptTemplate.from_template("""\
Je bent een assistent die functietitels uit vacatures haalt. Geef een lijst terug met functietitels in geldig JSON-formaat.

Vacaturetekst:
{vacancy}

Geef de functietitels als: {{"function_titles": ["..."]}}
{valid_json}

""")

SUGGEST_EXTRA_PROMPT = ChatPromptTemplate.from_template("""\
Je bent een assistent die extra mogelijke functietitels suggereert op basis van een vacaturetekst. Denk breed en creatief.

Vacaturetekst:
{vacancy}

Geef de suggesties als: {{"potential_function_titles": ["..."]}}
{valid_json} 

""")
VALIDATE_PROMPT = ChatPromptTemplate.from_template("""\
Je controleert of de volgende functietitels goed passen bij de vacaturetekst. Als ze onjuist of onvolledig zijn, zeg 'false', anders 'true'.

Vacaturetekst:
{vacancy}

Gevonden functietitels:
{titles}

Suggesties:
{suggestions}

Geef je antwoord als: {{"is_valid": true}}

{valid_json} 

""")
