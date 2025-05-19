import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from entities.basic_entities import ContentTopics
from prompts.notebook_prompts import SUBTOPICS_GENERATION_PROMPT

load_dotenv()

def create():
    llm = ChatOpenAI(model="gpt-4.1-nano")

    topic = "listas"

    subtopics_template = ChatPromptTemplate.from_template(SUBTOPICS_GENERATION_PROMPT)

    structured_llm = llm.with_structured_output(ContentTopics)

    chain = subtopics_template | structured_llm

    response = chain.invoke(
        {
            "topic": topic
        }
    )

    print(response.subtopics)


if __name__ == "__main__":
    create()