import os

import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-nano")

topics = "dicionarios, listas e tuplas"

prompt = """
#################### Contexto ####################

Você é um assistente para a geração de conteúdo, seu papel é descrever
no formato de subtópicos os tópicos apresentados a seguir para que uma lista
de exercícios prática seja criada para a fixação do conteúdo da disciplina.

Enumere os principais e mais importantes subtópicos para o conteúdo a seguir:
{topics}
"""



template = ChatPromptTemplate.from_template(prompt)

chain = template | llm

response = chain.invoke(
    {
        "topics": topics
    }
)

print(response.content)

from enum import Enum

class CellTypes(Enum):
    markdown = 'markdown'
    code = 'code'

class NotebookCell(BaseModel):
    cell_type: CellTypes = Field(description='notebook cell type')

class CodeCell(NotebookCell):
    source: list[str] = Field(
        description='List of Python code lines to exemply the theorical content'
        )

    @field_validator('source')
    @classmethod
    def validate_and_split_strings(cls, value: list[str]) -> list[str]:
        """
        Validates if the input is a list with a single string containing newlines.
        If so, splits the string by newlines and returns the resulting list.
        """
        if len(value) == 1 and '\n' in value[0]:
            return [line + '\n' for line in value[0].split('\n') if len(line) > 0]

        return value


class MarkdownCell(NotebookCell):
    source: list[str] = Field(
        description='List containing topic name and explanation about what it is.'
        )

    @field_validator('source')
    @classmethod
    def validate_and_split_strings(cls, value: list[str]) -> list[str]:
        """
        Validates if the input is a list with a single string containing newlines.
        If so, splits the string by newlines and returns the resulting list.
        """
        if len(value) == 1 and '\n' in value[0]:
            return [line + '\n' for line in value[0].split('\n') if len(line) > 0]

        return value

class Content(BaseModel):
    markdown: MarkdownCell = Field(description='markdown text explaining the content')
    code: CodeCell = Field(description='python code to exemplify the content')

prompt_notebook = """
#################### Contexto ####################

Você é um assistente para a criação de conteúdos didáticos para uma disciplina.
Seu papel é gerar o conteúdo teórico e o código em python para serem adicionados
em um notebook como forma de exemplificar o que o aluno precisa aprender.

Gere sempre um par de células, sendo uma célula em markdown com o conteúdo explicativo
e outra célula com o código python, exemplificando claramente o conteúdo.

Orientações:
- Para as células em markdown adicione sempre um título resumindo o tema abordado em poucas palavras
- Use # para definir o título e coloque em negrito
- A explicação do conteudo coloque como um texto normal, podendo usar listas e/ou bullet point
- Gere o texto de explicação sempre em {language}
- Para as células de código python, gere um código que exemplifique ou explique o tópico abordado
- Todos os códigos deverão ser gerados em inglês e com nomes significativos para as variáveis

Gere as células em markdown e código python para o seguinte tópico {topic} que pertence ao tema {content}
"""

prompt_notebook_template = ChatPromptTemplate.from_template(prompt_notebook)

structured_llm = llm.with_structured_output(Content)

notebook_chain = prompt_notebook_template | structured_llm

response = notebook_chain.invoke(
    {
        "language": "pt-BR",
        "content": "Dicionários",
        "topic": "Definição e criação de dicionários"
    }
)

generated_cell = {
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

print(json.dumps(generated_cell["cells"], indent=4, ensure_ascii=False))

