from typing import TypedDict\

class ExpRange(TypedDict):
    min_exp : int
    max_exp : int

class Duration(TypedDict):
    start_month : int
    start_year : int
    end_month : int
    end_year : int

class Experience(TypedDict):
    company : str
    duration: Duration
    position : str
    description : str

class Projects(TypedDict):
    name : str
    description : str

class Achievement(TypedDict):
    name : str
    description : str

class Education(TypedDict):
    uni_name : str
    Duration : Duration

class StructuredResume(TypedDict):
    name : str
    summary : str
    skills : list[str]
    experience : list[Experience]
    projects : list[Projects]
    achievements : list[Achievement]
    education : Education
