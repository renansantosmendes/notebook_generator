from enum import Enum

from pydantic import BaseModel, Field, field_validator


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