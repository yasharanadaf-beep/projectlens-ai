import os
import json
import time

try:
    import streamlit as st
except ImportError:
    st = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from google import genai
except ImportError:
    genai = None


def get_api_key():
    key = os.getenv("GEMINI_API_KEY")

    if not key and st is not None:
        try:
            key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            key = None

    return key


def analyze_project(project_text):

    # Check Google SDK
    if genai is None:
        return {
            "error": "google-genai is not installed. Check requirements.txt."
        }

    # Get API key
    api_key = get_api_key()

    if not api_key:
        return {
            "error": "GEMINI_API_KEY is missing. Add it in Streamlit Cloud Secrets."
        }

    # Limit input size
    project_text = project_text[:32000]

    prompt = f"""
You are ProjectLens, an AI evaluator for student software projects.

Analyze ONLY the supplied project information.

Do not invent facts.

If source code is not provided, do not claim actual code bugs.
Instead, identify possible technical, design, logic, or implementation risks.

Return ONLY valid JSON.

Use exactly this structure:

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

PROJECT INFORMATION:

{project_text}
"""

    # Create Gemini client
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        return {
            "error": f"Could not initialize Gemini: {e}"
        }

    # Retry temporary 503 errors
    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            text = (response.text or "").strip()

            # Remove markdown JSON fences if Gemini adds them
            if text.startswith("```json"):
                text = text[7:]

            if text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            return json.loads(text)

        except json.JSONDecodeError:

            return {
                "error": "Gemini returned an invalid JSON response.",
                "raw_response": text
            }

        except Exception as e:

            error_text = str(e)

            # Retry temporary server overload
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < max_attempts - 1:

                    wait_time = 3 * (2 ** attempt)

                    time.sleep(wait_time)

                    continue

                return {
                    "error": (
                        "Gemini is temporarily experiencing high demand. "
                        "Please wait a little and try Analyze Project again."
                    )
                }

            # Handle rate limit
            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                return {
                    "error": (
                        "Gemini API rate limit reached. "
                        "Please wait for the quota to reset or check your "
                        "Gemini API usage limits."
                    )
                }

            # Other errors
            return {
                "error": f"Gemini analysis failed: {e}"
            }

    return {
        "error": "Gemini analysis could not be completed."
    }
