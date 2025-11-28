"""
Base Question Generation Module

This Module is responsible for generating base role related questions against given job
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from pydantic import SecretStr
from .output import BaseQuestionOuput
from .types import ExpRange
from .prompts import BASE_QUESTION_GENERATION_SYSTEM_PROMPT, BASE_QUESTION_GENERATION_HUMAN_PROMPT

class QuestionGenerator:
    def __init__(self, model_name: str) -> None:
        load_dotenv()
        self.model = self._init_model(model_name)

    def _init_model(self, model_name : str):
        """
        Initialize the ChatOpenAI Instance
        Args:
            model_name : name of the openai model
        Returns:
            Model with structured Ouptut
        """
        model = ChatOpenAI(
            model=model_name,
            api_key=SecretStr(self._validate()),
            temperature=0
        )
        structured_model = model.with_structured_output(BaseQuestionOuput)
        return structured_model

    def _validate(self)->str:
        """Validate api key in the environment"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            raise ValueError("No Api Key found, Set Environment Variable 'OPENAI_API_KEY'")
        return api_key
    
    def _create_prompt(self, role : str, exp_range : ExpRange, description : str)->ChatPromptTemplate:
        """Create Human and System prompt"""
        min_exp = exp_range.get('min_exp')
        max_exp = exp_range.get('max_exp')
        formatted_exp = f"{min_exp} - {max_exp}"
        prompt = ChatPromptTemplate.from_messages([
            ('system', BASE_QUESTION_GENERATION_SYSTEM_PROMPT.format(role=role, max_experience=max_exp)),
            ('human', BASE_QUESTION_GENERATION_HUMAN_PROMPT.format(role = role, exp_range = formatted_exp, description = description))
        ])
        return prompt
    
    def invoke(self, role : str, exp_range : ExpRange, description : str ):
        """
        Invoke the model and get structured list of questions
        Args:
            role : Title of the job
            exp_range : range to experience for min to max
            description : The job description for the role
        Returns:
            The Structured List of questions
        """
        if not role or not exp_range or not description:
            raise ValueError(f"Required {"role" if not role else ""}, {"exp_range" if not exp_range else ""}, {"description" if not description else ""}")
        prompt = self._create_prompt(role, exp_range, description)
        result = self.model.invoke(prompt.format_messages())
        return result
