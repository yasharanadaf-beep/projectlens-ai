import streamlit as st
import html

from extractor import extract_text
from agent import analyze_project


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ProjectLens",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
"""<style>

.stApp {
    background: #f6f8fc;
    color: #172033;
}

.main .block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stAppViewContainer"] {
    background: #f6f8fc !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}


/* ================= HERO ================= */

.hero {
    background: linear-gradient(135deg, #ffffff 0%, #eef4ff 100%);
    border: 1px solid #dbe4f0;
    border-radius: 22px;
    padding: 32px 36px;
    margin-bottom: 28px;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #111827 !important;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 17px;
    color: #64748b !important;
    margin-top: 8px;
}


/* ================= SECTION TITLE ================= */

.section-title {
    font-size: 24px;
    font-weight: 750;
    color: #111827 !important;
    margin-top: 30px;
    margin-bottom: 15px;
}


/* ================= GENERAL CARD ================= */

.dashboard-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    color: #172033 !important;
}

.dashboard-card * {
    color: #172033 !important;
}


/* ================= HEALTH ================= */

.health-card {
    background: linear-gradient(135deg, #ffffff, #eef6ff);
    border: 1px solid #dbeafe;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 15px;
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.08);
}

.health-number {
    font-size: 44px;
    font-weight: 800;
    color: #2563eb !important;
}

.health-label {
    font-size: 14px;
    color: #64748b !important;
    font-weight: 600;
}


/* ================= SCORE CARDS ================= */

.score-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    min-height: 105px;
    margin-bottom: 12px;
    box-shadow: 0 5px 15px rgba(15, 23, 42, 0.04);
}

.score-name {
    font-size: 14px;
    font-weight: 600;
    color: #64748b !important;
}

.score-value {
    font-size: 27px;
    font-weight: 800;
    color: #111827 !important;
    margin-top: 8px;
}


/* ================= STRENGTH ================= */

.success-card {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 5px solid #22c55e;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    color: #14532d !important;
}

.success-card * {
    color: #14532d !important;
}


/* ================= CRITICAL ISSUE ================= */

.issue-card {
    background: #fff5f5;
    border: 1px solid #fecaca;
    border-left: 5px solid #ef4444;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    color: #7f1d1d !important;
}

.issue-card * {
    color: #7f1d1d !important;
}


/* ================= WARNING ================= */

.warning-card {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 5px solid #f59e0b;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    color: #78350f !important;
}

.warning-card * {
    color: #78350f !important;
}


/* ================= IMPROVEMENT ================= */

.improvement-card {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-left: 5px solid #3b82f6;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 13px;
    color: #172033 !important;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
}

.improvement-card * {
    color: #172033 !important;
}

.improvement-title {
    font-size: 18px;
    font-weight: 750;
    color: #1d4ed8 !important;
}


/* ================= FEATURE ================= */

.feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 13px;
    padding: 16px 18px;
    margin-bottom: 10px;
    color: #334155 !important;
}

.feature-card * {
    color: #334155 !important;
}


/* ================= ACTION ================= */

.action-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    color: #172033 !important;
}

.action-card * {
    color: #172033 !important;
}

.step-number {
    display: inline-block;
    background: #2563eb;
    color: white !important;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    text-align: center;
    line-height: 30px;
    font-weight: 700;
    margin-right: 8px;
}


/* ================= FINAL ================= */

.final-card {
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    border: 1px solid #cbd5e1;
    border-radius: 18px;
    padding: 25px;
    margin-top: 10px;
    color: #172033 !important;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
}

.final-card * {
    color: #172033 !important;
}


/* ================= SIDEBAR ================= */

[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}

[data-testid="stSidebar"] * {
    color: #172033 !important;
}


/* ================= FILE UPLOADER ================= */

[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 8px;
}


/* ================= BUTTON ================= */

.stButton > button {
    border-radius: 12px;
    border: 1px solid #2563eb;
    background: #2563eb;
    color: white !important;
    font-weight: 700;
    min-height: 48px;
}

.stButton > button:hover {
    background: #1d4ed8;
    border-color: #1d4ed8;
}


/* ================= METRICS ================= */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
}


/* ================= NORMAL TEXT ================= */

p,
label {
    color: #334155;
}


/* ================= DIVIDER ================= */

hr {
    border-color: #e2e8f0 !important;
}

</style>""",
unsafe_allow_html=True
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_text(value):
    if value is None:
        return ""
    return html.escape(str(value))


def show_section_title(icon, title):
    st.markdown(
f"""<div class="section-title">{icon} {safe_text(title)}</div>""",
unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
"""<div style="font-size:26px;font-weight:800;color:#111827;">
🔎 ProjectLens
</div>""",
unsafe_allow_html=True
    )

    st.markdown(
"""<div style="color:#64748b;font-size:14px;margin-top:4px;margin-bottom:25px;">
AI-powered project evaluation
</div>""",
unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Analysis Mode")

    demo_mode = st.toggle(
        "⚡ Demo Mode",
        value=True
    )

    if demo_mode:
        st.info(
            "Demo Mode gives instant sample results without using Gemini."
        )
    else:
        st.warning(
            "Live AI Mode uses your Gemini API quota."
        )

    st.markdown("---")

    st.markdown("### 📋 What ProjectLens checks")

    st.markdown(
"""
- 🎯 Problem
- 💻 Technology
- 💡 Innovation
- ⚙️ Feasibility
- 📋 Completeness
- 🎨 Presentation
- 🐞 Technical risks
- 📌 Missing components
- 🛠️ Improvements
""",
unsafe_allow_html=False
    )


# =========================================================
# HERO
# =========================================================

st.markdown(
"""<div class="hero">
<div class="hero-title">🔎 ProjectLens</div>
<div class="hero-subtitle">AI-powered Project Evaluation &amp; Improvement Agent</div>
</div>""",
unsafe_allow_html=True
)


# =========================================================
# UPLOAD
# =========================================================

show_section_title(
    "📄",
    "Upload Your Project"
)

uploaded_file = st.file_uploader(
    "Upload your Project Report or PPT",
    type=["pdf", "pptx"],
    label_visibility="collapsed"
)


if uploaded_file:

    st.success(
        f"Uploaded successfully: {uploaded_file.name}"
    )

    analyze_button = st.button(
        "🚀 Analyze My Project",
        use_container_width=True
    )

    if analyze_button:

        # =================================================
        # DEMO MODE
        # =================================================

        if demo_mode:

            st.info(
                "⚡ Demo Mode: generating instant analysis..."
            )

            result = {

                "project_name": "Smart Attendance System",

                "summary": (
                    "An AI-based attendance system that uses "
                    "face recognition to automatically record "
                    "student attendance."
                ),

                "project_health": 78,

                "scores": {
                    "problem": 85,
                    "technology": 78,
                    "innovation": 68,
                    "feasibility": 82,
                    "completeness": 70,
                    "presentation": 75
                },

                "strengths": [
                    "The problem is clearly defined.",
                    "The solution can reduce manual attendance work.",
                    "The selected technologies are suitable for a student project.",
                    "The project has clear practical use."
                ],

                "critical_issues": [
                    {
                        "issue": "Student face data security is not explained.",
                        "why_it_matters": (
                            "Face data is sensitive and the project "
                            "should explain how it will be protected."
                        ),
                        "severity": "High"
                    }
                ],

                "potential_bugs": [
                    {
                        "bug": "Face recognition may fail in poor lighting.",
                        "explanation": (
                            "Lighting and camera quality can affect "
                            "recognition accuracy."
                        ),
                        "severity": "Medium"
                    }
                ],

                "missing_components": [
                    "Accuracy evaluation",
                    "Security and privacy mechanism",
                    "Testing results"
                ],

                "improvements": [
                    {
                        "area": "Security",
                        "current_problem": (
                            "The report does not explain how student "
                            "face data will be protected."
                        ),
                        "suggestion": (
                            "Add authentication and explain secure "
                            "storage of face data."
                        ),
                        "priority": "High"
                    },
                    {
                        "area": "Testing",
                        "current_problem": (
                            "No testing or accuracy results are provided."
                        ),
                        "suggestion": (
                            "Test the system under different lighting "
                            "conditions and report accuracy."
                        ),
                        "priority": "High"
                    }
                ],

                "recommended_features": [
                    "Attendance report generation",
                    "Teacher login",
                    "Search and filter attendance",
                    "Export attendance as CSV"
                ],

                "action_plan": [
                    {
                        "step": 1,
                        "action": "Add security and privacy measures.",
                        "priority": "High"
                    },
                    {
                        "step": 2,
                        "action": "Perform accuracy testing.",
                        "priority": "High"
                    },
                    {
                        "step": 3,
                        "action": "Add attendance report generation.",
                        "priority": "Medium"
                    }
                ],

                "final_summary": (
                    "The project has a clear problem and a practical "
                    "solution. The team should focus on security, "
                    "testing, accuracy evaluation, and reporting "
                    "before real deployment."
                )
            }

            st.success(
                "⚡ Demo analysis completed instantly."
            )


        # =================================================
        # LIVE AI MODE
        # =================================================

        else:

            try:

                with st.spinner(
                    "📖 Reading your project..."
                ):

                    project_text = extract_text(
                        uploaded_file
                    )

                with st.spinner(
                    "🤖 ProjectLens is analyzing your project..."
                ):

                    result = analyze_project(
                        project_text
                    )

            except Exception as e:

                error_message = str(e)

                if "429" in error_message:

                    st.error(
                        "⚠️ Gemini daily limit reached. "
                        "Please switch ON Demo Mode for your presentation."
                    )

                elif "503" in error_message:

                    st.error(
                        "⚠️ Gemini is temporarily unavailable. "
                        "Please try again later or use Demo Mode."
                    )

                else:

                    st.error(
                        "⚠️ Something went wrong while analyzing "
                        "the project."
                    )

                st.stop()


        st.session_state["analysis"] = result


# =========================================================
# RESULTS
# =========================================================

if "analysis" in st.session_state:

    result = st.session_state["analysis"]

    st.divider()


    # =====================================================
    # PROJECT HEADER
    # =====================================================

    project_name = result.get(
        "project_name",
        "Project Evaluation"
    )

    summary = result.get(
        "summary",
        ""
    )

    st.markdown(
f"""<div class="dashboard-card">
<div style="font-size:28px;font-weight:800;color:#111827;margin-bottom:8px;">
📊 {safe_text(project_name)}
</div>
<div style="font-size:16px;line-height:1.6;color:#475569;">
{safe_text(summary)}
</div>
</div>""",
unsafe_allow_html=True
    )


    # =====================================================
    # PROJECT HEALTH
    # =====================================================

    health = result.get(
        "project_health",
        0
    )

    show_section_title(
        "🎯",
        "Project Health"
    )

    st.markdown(
f"""<div class="health-card">
<div class="health-number">{health}/100</div>
<div class="health-label">Overall Project Health</div>
</div>""",
unsafe_allow_html=True
    )

    st.progress(
        min(max(int(health), 0), 100) / 100
    )


    # =====================================================
    # EVALUATION OVERVIEW
    # =====================================================

    show_section_title(
        "📈",
        "Evaluation Overview"
    )

    scores = result.get(
        "scores",
        {}
    )

    score_data = [
        ("Problem", scores.get("problem", 0)),
        ("Technology", scores.get("technology", 0)),
        ("Innovation", scores.get("innovation", 0)),
        ("Feasibility", scores.get("feasibility", 0)),
        ("Completeness", scores.get("completeness", 0)),
        ("Presentation", scores.get("presentation", 0))
    ]

    columns = st.columns(3)

    for index, (name, value) in enumerate(score_data):

        with columns[index % 3]:

            st.markdown(
f"""<div class="score-card">
<div class="score-name">{safe_text(name)}</div>
<div class="score-value">{value}/100</div>
</div>""",
unsafe_allow_html=True
            )


    # =====================================================
    # STRENGTHS
    # =====================================================

    show_section_title(
        "🟢",
        "Project Strengths"
    )

    strengths = result.get(
        "strengths",
        []
    )

    if not strengths:

        st.info(
            "No specific strengths were identified."
        )

    for strength in strengths:

        st.markdown(
f"""<div class="success-card">
<strong>✅ Strength</strong>
<br><br>
{safe_text(strength)}
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # CRITICAL ISSUES
    # =====================================================

    show_section_title(
        "🔴",
        "Critical Issues"
    )

    issues = result.get(
        "critical_issues",
        []
    )

    if not issues:

        st.success(
            "No major critical issues detected."
        )

    for issue in issues:

        st.markdown(
f"""<div class="issue-card">
<strong>🚨 {safe_text(issue.get("issue", ""))}</strong>
<br><br>
<strong>Why it matters:</strong>
<br>
{safe_text(issue.get("why_it_matters", ""))}
<br><br>
<strong>Severity:</strong>
{safe_text(issue.get("severity", ""))}
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # TECHNICAL ISSUES
    # =====================================================

    show_section_title(
        "🐞",
        "Potential Technical / Logic Issues"
    )

    bugs = result.get(
        "potential_bugs",
        []
    )

    if not bugs:

        st.info(
            "No potential technical issues were identified."
        )

    for bug in bugs:

        st.markdown(
f"""<div class="warning-card">
<strong>⚠️ {safe_text(bug.get("bug", ""))}</strong>
<br><br>
{safe_text(bug.get("explanation", ""))}
<br><br>
<strong>Severity:</strong>
{safe_text(bug.get("severity", ""))}
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # MISSING COMPONENTS
    # =====================================================

    show_section_title(
        "📌",
        "Missing Components"
    )

    missing = result.get(
        "missing_components",
        []
    )

    if not missing:

        st.success(
            "No major missing components detected."
        )

    for item in missing:

        st.markdown(
f"""<div class="issue-card">
<strong>📌 Missing Component</strong>
<br><br>
{safe_text(item)}
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # IMPROVEMENTS
    # =====================================================

    show_section_title(
        "🛠️",
        "Improvements Needed"
    )

    improvements = result.get(
        "improvements",
        []
    )

    if not improvements:

        st.info(
            "No specific improvements were suggested."
        )

    for item in improvements:

        st.markdown(
f"""<div class="improvement-card">
<div class="improvement-title">🔧 {safe_text(item.get("area", ""))}</div>
<br>
<strong>Current Problem</strong>
<br>
{safe_text(item.get("current_problem", ""))}
<br><br>
<strong>Recommended Improvement</strong>
<br>
{safe_text(item.get("suggestion", ""))}
<br><br>
<strong>Priority:</strong>
{safe_text(item.get("priority", ""))}
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # RECOMMENDED FEATURES
    # =====================================================

    show_section_title(
        "💡",
        "Recommended Features"
    )

    features = result.get(
        "recommended_features",
        []
    )

    if not features:

        st.info(
            "No additional features were recommended."
        )

    for feature in features:

        st.markdown(
f"""<div class="feature-card">
➕ <strong>{safe_text(feature)}</strong>
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # ACTION PLAN
    # =====================================================

    show_section_title(
        "🎯",
        "Project Improvement Action Plan"
    )

    actions = result.get(
        "action_plan",
        []
    )

    if not actions:

        st.info(
            "No action plan was generated."
        )

    for action in actions:

        st.markdown(
f"""<div class="action-card">
<span class="step-number">{safe_text(action.get("step", ""))}</span>
<strong>{safe_text(action.get("action", ""))}</strong>
<br><br>
<strong>Priority:</strong>
{safe_text(action.get("priority", ""))}
</div>""",
unsafe_allow_html=True
        )


    # =====================================================
    # FINAL EVALUATION
    # =====================================================

    show_section_title(
        "📝",
        "Final Evaluation"
    )

    st.markdown(
f"""<div class="final-card">
<div style="font-size:20px;font-weight:800;margin-bottom:12px;">
ProjectLens Evaluation
</div>
<div style="font-size:16px;line-height:1.7;">
{safe_text(result.get("final_summary", ""))}
</div>
</div>""",
unsafe_allow_html=True
    )


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
"""<div style="text-align:center;color:#94a3b8;font-size:13px;margin-top:45px;padding-top:20px;border-top:1px solid #e2e8f0;">
🔎 ProjectLens • AI-powered Project Evaluation &amp; Improvement Agent
</div>""",
unsafe_allow_html=True
    )