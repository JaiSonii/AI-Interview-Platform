from pydantic import BaseModel, Field
from typing import Optional, List

class MonthYear(BaseModel):
    month: int = Field(..., description="Month represented as an integer from 1 to 12.")
    year: int = Field(..., description="Year represented as a four-digit integer (e.g., 2024).")

class ExperienceDuration(BaseModel):
    start: MonthYear = Field(..., description="Start month and year of the experience period.")
    end: MonthYear = Field(..., description="End month and year of the experience period.")

class Education(BaseModel):
    uni_name: str = Field(..., description="Full name of the university or educational institution.")
    start_year: int = Field(..., description="Year in which the academic program began.")
    end_year: Optional[int] = Field(None, description="Year in which the academic program ended. Optional if ongoing.")
    sgpa: float = Field(..., description="SGPA or GPA achieved during the academic program.")

class Project(BaseModel):
    name: str = Field(..., description="Official or commonly used name of the project.")
    skills: List[str] = Field(..., description="List of technologies, tools, and skills used in the project.")
    description: List[str] = Field(..., description="Bullet-point descriptions highlighting responsibilities and achievements.")

class Experience(BaseModel):
    role: str = Field(..., description="Job title or role held at the company.")
    company: str = Field(..., description="Name of the company or organization.")
    duration: ExperienceDuration = Field(..., description="Start and end period of the work experience.")
    skills: List[str] = Field(..., description="List of relevant skills or technologies used in this experience.")
    description: List[str] = Field(..., description="Bullet points describing responsibilities, contributions, and accomplishments.")

class StructuredResume(BaseModel):
    name: str = Field(..., description="Full name of the candidate.")
    total_exp: float = Field(..., description="Total years of professional experience.")
    education: Education = Field(..., description="Educational background of the candidate.")
    projects: List[Project] = Field(..., description="List of major academic or personal projects.")
    experience: List[Experience] = Field(..., description="List of professional work experiences.")
