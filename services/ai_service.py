import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_research(papers, topic):

    paper_text = ""

    for i, paper in enumerate(papers, start=1):

        title = paper.get("title", "Unknown title")

        publication_info = paper.get(
            "publication_info",
            {}
        )

        summary = publication_info.get(
            "summary",
            "Unknown authors"
        )

        snippet = paper.get(
            "snippet",
            "No description available."
        )

        paper_text += f"""
Paper {i}
Title: {title}
Authors and publication: {summary}
Description: {snippet}
"""


    prompt = f"""
You are ResearchRadar, a research discovery assistant.

The user wants to research:

{topic}

Below is information retrieved from live Google Scholar search results.

{paper_text}

IMPORTANT RULES:
- Analyze ONLY the information provided above.
- Do not claim to have read the full papers.
- Do not invent findings, statistics, methods, or conclusions.
- Do not present an unsupported assumption as an established research gap.
- Clearly distinguish explicitly reported gaps from potential gaps.
- If the information is insufficient, say so.

Provide the following sections:

## Research Overview

Give a concise 3-4 sentence overview of what the retrieved literature
appears to focus on.

## Key Findings

Identify 4-6 important findings or recurring ideas supported by the
retrieved information.

## Major Research Themes

Identify 3-5 recurring themes across the papers.

## Research Gaps

Divide the gaps into two categories:

### Explicitly Reported Gaps
Only include gaps or limitations that are directly indicated by the
provided paper titles or descriptions.

### Potential Research Gaps
Suggest 2-4 areas that could be investigated further based on patterns
in the retrieved literature.

Clearly label these as potential gaps rather than established facts.

## Possible Research Questions

Based on the potential gaps, suggest 3-5 research questions that a
student could investigate.

Keep the language clear and suitable for a college student.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text