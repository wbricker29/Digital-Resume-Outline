from typing import TypedDict, Optional


class Summary(TypedDict):
    section_id: str
    text: str
    tags: list[str]


class CompetencyCategory(TypedDict):
    section_id: str
    skills: list[str]
    tags: list[str]


class CoreCompetencies(TypedDict):
    technical_expertise: CompetencyCategory
    investment_and_finance: CompetencyCategory
    business_and_strategy: CompetencyCategory


class Position(TypedDict):
    section_id: str
    title: str
    start: str
    end: str
    achievements: list[str]


class Experience(TypedDict):
    company: str
    positions: list[Position]
    tags: list[str]


class Project(TypedDict):
    section_id: str
    title: str
    description: str


class Education(TypedDict):
    section_id: str
    institution: str
    degree: str
    graduation_date: str


class Resume(TypedDict):
    professional_summary: Summary
    core_competencies: CoreCompetencies
    experience: list[Experience]
    projects_and_consulting: list[Project]
    education: list[Education]


class ProfileItem(TypedDict):
    section_id: str
    text: str


class SignatureProject(TypedDict):
    name: str
    description: str


class SignatureProjectsContainer(TypedDict):
    projects: list[SignatureProject]


class ProfessionalProfile(TypedDict):
    career_objectives: ProfileItem
    value_proposition: ProfileItem
    professional_approach: ProfileItem
    signature_projects: SignatureProjectsContainer


class ReferenceData(TypedDict):
    resume: Resume
    professional_profile: ProfessionalProfile