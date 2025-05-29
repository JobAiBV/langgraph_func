from langchain.prompts import ChatPromptTemplate


EXPLICIT_PROMPT = ChatPromptTemplate.from_template("""\
Analyseer onderstaande vacaturetekst. De tekst kan in het Nederlands of in het Engels zijn geschreven. 
Bepaal welk expliciet genoemd opleidingsniveau van toepassing is. Je antwoord moet gebaseerd zijn op directe formuleringen 
die een opleidingsniveau aangeven, niet op interpretaties of indirecte signalen.

Geef als resultaat exact één van de volgende vier opties als JSON (zonder extra toelichting):
{{ "level": "WO" }}
{{ "level": "HBO" }}
{{ "level": "MBO" }}
{{ "level": "geen expliciet onderwijsniveau vernoemd" }}

{valid_json}

Vacaturetekst:
{vacancy}""")

IMPLICIT_PROMPT = ChatPromptTemplate.from_template("""\
Analyseer onderstaande vacaturetekst (in het Nederlands of Engels) op impliciete aanwijzingen voor het 
vereiste opleidingsniveau. Denk aan 'academisch denkniveau', 'hbo werk- en denkniveau', of 'praktisch ingesteld'.

Geef als resultaat exact één van de volgende vier opties als JSON:
{{ "level": "WO" }}
{{ "level": "HBO" }}
{{ "level": "MBO" }}
{{ "level": "geen impliciet onderwijsniveau gevonden" }}

{valid_json}

Vacaturetekst:
{vacancy}""")

QUALIFICATION_PROMPT = ChatPromptTemplate.from_template("""\
Onderzoek onderstaande vacaturetekst op termen die kwalificaties of certificeringen aanduiden, zoals 
'gediplomeerd', 'certified', of 'universitair profiel'. Koppel deze aan het opleidingsniveau volgens de Nederlandse context.

Geef als resultaat exact één van de volgende vier opties als JSON:
{{ "level": "WO" }}
{{ "level": "HBO" }}
{{ "level": "MBO" }}
{{ "level": "geen onderwijsniveau af te leiden" }}

{valid_json}

Vacaturetekst:
{vacancy}""")

NEGATION_PROMPT = ChatPromptTemplate.from_template("""\
Detecteer uitzonderingen of nuances in de tekst met betrekking tot opleidingsvereisten. Noem uitspraken zoals:
- 'WO-niveau uitgesloten'
- 'Geen diploma vereist'
- 'HBO of WO allebei toegestaan'

Geef het resultaat als een JSON-lijst van korte, feitelijke uitspraken (zonder bullets), bijvoorbeeld:
{{ "negations": ["Geen diploma vereist", "WO-niveau uitgesloten"] }}

Als je geen lijst vind geef 
{{ "negations": [] }}

{valid_json}

Vacaturetekst:
{vacancy}""")

CONTEXT_PROMPT = ChatPromptTemplate.from_template("""\
Bepaal op basis van functietitels of sectorcontext het meest waarschijnlijke opleidingsniveau in de 
Nederlandse arbeidsmarkt. Doe dit alleen als er geen expliciete of impliciete niveaus genoemd worden.

Geef als resultaat exact één van de volgende als JSON:
{{ "level": "WO" }}
{{ "level": "HBO" }}
{{ "level": "MBO" }}
{{ "level": "geen niveau af te leiden" }}

Geef altijd een output. ALs je niets kan vinden  geen niveau af te leiden

{valid_json}

Vacaturetekst:
{vacancy}""")

COMBINE_PROMPT = ChatPromptTemplate.from_template("""\
Hier zijn de analyse resultaten:

• Explicit: {explicit}
• Implicit: {implicit}
• Qualification: {qualification}
• Negation: {negation}
• Context: {context}

Geef als eindresultaat een JSON-object met exact twee velden:
{{ 
  "summary": "Korte uitleg in maximaal 30 woorden",
  "final_level": "WO"  // Of: HBO, MBO, Unknown
}}

{valid_json}

Geef altijd output voor beide""")
