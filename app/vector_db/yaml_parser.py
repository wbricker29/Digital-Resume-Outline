import yaml
from pathlib import Path
from typing import cast
from app.vector_db.types import ReferenceData


def parse_reference_yaml_to_chunks(reference_data: ReferenceData) -> list[dict]:
    """Parse reference.yaml into optimized vector database chunks."""
    chunks = []
    resume = reference_data.get("resume", {})
    prof_profile = reference_data.get("professional_profile", {})
    if "professional_summary" in resume:
        summary = resume["professional_summary"]
        chunks.append(
            {
                "id": summary.get("section_id", "professional_summary"),
                "type": "summary",
                "content": summary.get("text", ""),
                "metadata": {
                    "section": "professional_summary",
                    "tags": ", ".join(summary.get("tags", [])),
                },
            }
        )
    if "core_competencies" in resume:
        comp = resume["core_competencies"]
        for cat_key, cat_value in comp.items():
            if isinstance(cat_value, dict) and "skills" in cat_value:
                skills_text = (
                    f"{cat_key.replace('_', ' ').title()}:\n"
                    + """
""".join([f"- {skill}" for skill in cat_value["skills"]])
                )
                chunks.append(
                    {
                        "id": cat_value.get("section_id", f"competencies_{cat_key}"),
                        "type": "competencies",
                        "content": skills_text,
                        "metadata": {
                            "section": "core_competencies",
                            "category": cat_key,
                            "tags": ", ".join(cat_value.get("tags", [])),
                        },
                    }
                )
    if "experience" in resume:
        for exp_company in resume["experience"]:
            if "positions" in exp_company:
                for position in exp_company["positions"]:
                    pos_text = f"{position.get('title', 'Position')} at {exp_company.get('company', 'Company')}\n"
                    pos_text += f"Duration: {position.get('start', '')} to {position.get('end', 'Present')}\n\n"
                    if "achievements" in position:
                        pos_text += """Key Achievements:
""" + """
""".join([f"- {ach}" for ach in position["achievements"]])
                    chunks.append(
                        {
                            "id": position.get(
                                "section_id",
                                f"exp_{exp_company.get('company')}_{position.get('title')}",
                            ),
                            "type": "experience",
                            "content": pos_text,
                            "metadata": {
                                "section": "experience",
                                "company": exp_company.get("company", ""),
                                "title": position.get("title", ""),
                                "tags": ", ".join(exp_company.get("tags", [])),
                            },
                        }
                    )
    if "projects_and_consulting" in resume:
        for project in resume["projects_and_consulting"]:
            proj_text = f"Project: {project.get('title', 'Title')}\n"
            proj_text += f"{project.get('description', '')}"
            chunks.append(
                {
                    "id": project.get("section_id"),
                    "type": "project",
                    "content": proj_text,
                    "metadata": {
                        "section": "projects",
                        "title": project.get("title", ""),
                    },
                }
            )
    if "education" in resume:
        for edu in resume["education"]:
            edu_text = f"{edu.get('degree', 'Degree')} from {edu.get('institution', 'Institution')}\n"
            edu_text += f"Graduation: {edu.get('graduation_date', 'N/A')}"
            chunks.append(
                {
                    "id": edu.get("section_id"),
                    "type": "education",
                    "content": edu_text,
                    "metadata": {
                        "section": "education",
                        "institution": edu.get("institution", ""),
                    },
                }
            )
    for key in ["career_objectives", "value_proposition", "professional_approach"]:
        if key in prof_profile and isinstance(prof_profile[key], dict):
            item = prof_profile[key]
            chunks.append(
                {
                    "id": item.get("section_id", key),
                    "type": key.replace("_", " ").title(),
                    "content": item.get("text", ""),
                    "metadata": {"section": "professional_profile", "category": key},
                }
            )
    if "signature_projects" in prof_profile:
        sig_proj_container = prof_profile["signature_projects"]
        if "projects" in sig_proj_container:
            for project in sig_proj_container["projects"]:
                chunks.append(
                    {
                        "id": f"sig_proj_{project.get('name').replace(' ', '_').lower()}",
                        "type": "signature_project",
                        "content": f"{project.get('name')}: {project.get('description')}",
                        "metadata": {
                            "section": "signature_projects",
                            "title": project.get("name", ""),
                        },
                    }
                )
    return chunks