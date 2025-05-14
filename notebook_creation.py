import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from entities.basic_entities import Content
from prompts.notebook_prompts import CONTENT_GENERATION_PROMPT, SUBTOPICS_GENERATION_PROMPT

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano")

topics = "dicionarios, listas e tuplas"

template = ChatPromptTemplate.from_template(SUBTOPICS_GENERATION_PROMPT)

chain = template | llm

response = chain.invoke(
    {
        "topics": topics
    }
)

prompt_notebook_template = ChatPromptTemplate.from_template(CONTENT_GENERATION_PROMPT)

structured_llm = llm.with_structured_output(Content)

notebook_chain = prompt_notebook_template | structured_llm

response = notebook_chain.invoke(
    {
        "language": "pt-BR",
        "content": "Dicionários",
        "topic": "Definição e criação de dicionários"
    }
)

generated_cells = {
    "cells": [
        {
            "cell_type": "markdown",
            "source":
                response.markdown.source
            ,
            "metadata": {
                "id": ""
            }
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {
                "id": ""
            },
            "outputs": [],
            "source": response.code.source
        }
        ]
}

print(json.dumps(generated_cells["cells"], indent=4, ensure_ascii=False))

