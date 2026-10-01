import os
import json
import streamlit as st
from google import genai


# --------------------------------------------------
# GET GEMINI API KEY
# --------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None


# --------------------------------------------------
# AI ANALYSIS FUNCTION
# --------------------------------------------------

def analyze_project(project_text):

    if not API_KEY:
        return {
            "error": "Gemini API key is not configured."
        }

    try:
        client = genai.Client(api_key=API_KEY)

        prompt = f"""
You are ProjectLens, an AI-powered student project evaluator.

Analyze the project information below.

IMPORTANT RULES:
- Analyze ONLY the information provided.
- Do not invent technologies, features, results, or facts.
- If source code is not provided, do not claim that you found an actual code bug.
- For a PDF or PPT, identify potential technical, logical, design, or feasibility concerns.
- Give practical suggestions suitable for a student project.
- Return ONLY valid JSON.
- Do not use markdown.
- Do not add explanations outside the JSON.

PROJECT INFORMATION:

{project_text}


Return JSON using exactly this structure:

{{
    "project_name": "",
    "summary": "",

    "project_health": 0,

    "scores": {{
        "problem": 0,
        "technology": 0,
        "innovation": 0,
        "feasibility": 0,
        "completeness": 0,
        "presentation": 0
    }},

    "strengths": [],

    "critical_issues": [
        {{
            "issue": "",
            "why_it_matters": "",
            "severity": ""
        }}
    ],

    "potential_bugs": [
        {{
            "bug": "",
            "explanation": "",
            "severity": ""
        }}
    ],

    "missing_components": [],

    "improvements": [
        {{
            "area": "",
            "current_problem": "",
            "suggestion": "",
            "priority": ""
        }}
    ],

    "recommended_features": [],

    "action_plan": [
        {{
            "step": 1,
            "action": "",
            "priority": ""
        }}
    ],

    "final_summary": ""
}}
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        result_text = response.text.strip()

        # Remove accidental markdown code fences
        if result_text.startswith("```"):
            result_text = result_text.replace("```json", "")
            result_text = result_text.replace("```", "")
            result_text = result_text.strip()

        result = json.loads(result_text)

        return result

    except json.JSONDecodeError:
        return {
            "error": "AI returned an invalid JSON response.",
            "raw_response": result_text if "result_text" in locals() else ""
        }

    except Exception as e:
        return {
            "error": str(e)
        }
