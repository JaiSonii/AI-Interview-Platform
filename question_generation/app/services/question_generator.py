from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import SecretStr
from .helpers.output import BaseQuestionOutput
from .helpers.types import ExpRange
from .helpers.prompts import BASE_QUESTION_GENERATION_SYSTEM_PROMPT, BASE_QUESTION_GENERATION_HUMAN_PROMPT
from dotenv import load_dotenv
import os

class QuestionGenerator:
    def __init__(self, model_name: str = "gpt-4o") -> None:
        load_dotenv()
        self.model = self._init_model(model_name)

    def _init_model(self, model_name: str):
        """Initialize the ChatOpenAI Instance with Structured Output"""
        model = ChatOpenAI(
            model=model_name,
            api_key=SecretStr(self._validate()),
            temperature=0.1 # Low temp for consistent, strictly structured results
        )
        # Binds the Pydantic schema to the model output
        return model.with_structured_output(BaseQuestionOutput)

    def _validate(self) -> str:
        """Validate api key in the environment"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key is None:
            raise ValueError("No Api Key found. Set Environment Variable 'OPENAI_API_KEY'")
        return api_key
    
    def _create_prompt(self, role: str, exp_range: ExpRange, description: str) -> ChatPromptTemplate:
        """Create Human and System prompt"""
        min_exp = exp_range.get('min_exp')
        max_exp = exp_range.get('max_exp')
        formatted_exp = f"{min_exp} - {max_exp} years"
        
        # We inject role/experience into System Prompt for stronger persona adherence
        prompt = ChatPromptTemplate.from_messages([
            ('system', BASE_QUESTION_GENERATION_SYSTEM_PROMPT.format(role=role)),
            ('human', BASE_QUESTION_GENERATION_HUMAN_PROMPT.format(
                role=role, 
                exp_range=formatted_exp, 
                description=description
            ))
        ])
        return prompt
    
    def invoke(self, role: str, exp_range: ExpRange, description: str):
        """
        Generates the static Roadmap for the job posting.
        """
        # Improved Error Handling
        missing_fields = []
        if not role: missing_fields.append("role")
        if not exp_range: missing_fields.append("exp_range")
        if not description: missing_fields.append("description")
        
        if missing_fields:
            raise ValueError(f"Missing required arguments: {', '.join(missing_fields)}")

        prompt = self._create_prompt(role, exp_range, description)
        
        result = self.model.invoke(prompt.format_messages())
        return result