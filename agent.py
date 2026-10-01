import os
import json

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
    if genai is None:
        return {"error": "google-genai is not installed. Check requirements.txt and redeploy."}

    api_key = get_api_key()
    if not api_key:
        return {"error": "GEMINI_API_KEY is missing. Add it in Streamlit Cloud Secrets."}

    project_text = project_text[:32000]

    prompt = f'''You are ProjectLens, an AI evaluator for student software projects.
Analyze ONLY the supplied project information. Do not invent facts.
If source code is not supplied, do not claim actual code bugs.
Return ONLY valid JSON.

Use exactly:
{{
"project_name":"","summary":"","project_health":0,
"scores":{{"problem":0,"technology":0,"innovation":0,"feasibility":0,"completeness":0,"presentation":0}},
"strengths":[],
"critical_issues":[{{"issue":"","why_it_matters":"","severity":""}}],
"potential_bugs":[{{"bug":"","explanation":"","severity":""}}],
"missing_components":[],
"improvements":[{{"area":"","current_problem":"","suggestion":"","priority":""}}],
"recommended_features":[],
"action_plan":[{{"step":1,"action":"","priority":""}}],
"final_summary":""
}}

PROJECT INFORMATION:
{project_text}'''

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        text = (response.text or "").strip()
        if text.startswith("```"):
            text = text.replace("```json", "", 1).replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {"error": "Gemini returned invalid JSON.", "raw_response": text}
    except Exception as e:
        return {"error": f"Gemini analysis failed: {e}"}
