import os
import json
import time

from dotenv import load_dotenv
from google import genai


# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None
    )


# Create Gemini client
client = genai.Client(
    api_key=API_KEY
)


def analyze_project(project_text):

    prompt = f"""
You are ProjectLens, an AI Project Evaluation Agent.

Analyze the following student project like an experienced
project evaluator.

PROJECT CONTENT:
----------------
{project_text}
----------------

Evaluate:

1. Problem Statement
2. Objectives
3. Proposed Solution
4. Technology Selection
5. Methodology
6. Innovation
7. Feasibility
8. Completeness
9. Expected Outcome
10. Presentation Quality

Also identify:

- Strengths
- Critical issues
- Potential technical or logical problems
- Missing components
- Weak explanations
- Unrealistic claims
- Implementation risks
- Recommended features
- Specific improvements
- Action plan

IMPORTANT:
Do not invent information.

If something is not available in the project document,
say that the information is missing.

If no source code is provided, do not claim that you found
an actual code bug. Instead call it a potential technical
or logical issue.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "project_name": "Project name",

    "summary": "Short project summary",

    "project_health": 0,

    "scores": {{
        "problem": 0,
        "technology": 0,
        "innovation": 0,
        "feasibility": 0,
        "completeness": 0,
        "presentation": 0
    }},

    "strengths": [
        "strength 1",
        "strength 2"
    ],

    "critical_issues": [
        {{
            "issue": "Issue description",
            "why_it_matters": "Why this issue matters",
            "severity": "High"
        }}
    ],

    "potential_bugs": [
        {{
            "bug": "Potential technical or logical problem",
            "explanation": "Explanation",
            "severity": "Medium"
        }}
    ],

    "missing_components": [
        "Missing component 1",
        "Missing component 2"
    ],

    "improvements": [
        {{
            "area": "Area",
            "current_problem": "What is weak",
            "suggestion": "What should be improved",
            "priority": "High"
        }}
    ],

    "recommended_features": [
        "Feature 1",
        "Feature 2"
    ],

    "action_plan": [
        {{
            "step": 1,
            "action": "Action to perform",
            "priority": "High"
        }}
    ],

    "final_summary": "Overall evaluation in simple language"
}}
"""

    # Try Gemini up to 3 times if the server is temporarily busy
    for attempt in range(3):

        try:

            print(
                f"🤖 Sending request to Gemini... "
                f"(attempt {attempt + 1}/3)"
            )

            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input=prompt
            )

            response_text = interaction.output_text

            # Convert JSON text to Python dictionary
            try:
                return json.loads(response_text)

            except json.JSONDecodeError:

                return {
                    "project_name": "Project Evaluation",
                    "summary": "Gemini returned an unexpected format.",
                    "project_health": 0,
                    "scores": {},
                    "strengths": [],
                    "critical_issues": [],
                    "potential_bugs": [],
                    "missing_components": [],
                    "improvements": [],
                    "recommended_features": [],
                    "action_plan": [],
                    "final_summary": response_text
                }

        except Exception as e:

            if attempt < 2:

                print(
                    "⚠️ Gemini is temporarily busy. "
                    "Waiting 5 seconds before retrying..."
                )

                time.sleep(5)

            else:

                print("❌ Gemini request failed after 3 attempts.")

                raise e
