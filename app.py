import streamlit as st
from extractor import extract_text
from agent import analyze_project


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ProjectLens",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f7f9fc;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        color: #17324d;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #5d6b7a;
        margin-bottom: 25px;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e5eaf0;
        margin: 10px 0;
    }

    .score {
        font-size: 28px;
        font-weight: 800;
        color: #17324d;
    }

    .section-title {
        color: #17324d;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">🔎 PROJECTLENS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered Project Evaluation & Improvement Agent</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your project report",
    type=["pdf", "pptx"],
    help="Upload a PDF project report or PowerPoint presentation."
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button(
        "🤖 Analyze Project",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Reading and analyzing your project..."):

            # Extract text from uploaded PDF/PPTX
            project_text = extract_text(uploaded_file)

            # Check whether text was extracted
            if not project_text or not project_text.strip():

                st.error(
                    "No readable text was found in this file. "
                    "Please upload a text-based PDF or PPTX."
                )

                st.stop()

            # Send the ACTUAL uploaded project to the AI
            result = analyze_project(project_text)

            # Save result in session
            st.session_state["result"] = result


# --------------------------------------------------
# DISPLAY RESULT
# --------------------------------------------------

result = st.session_state.get("result")


if result:

    # --------------------------------------------------
    # ERROR HANDLING
    # --------------------------------------------------

    if result.get("error"):

        st.error(result["error"])

        if result.get("raw_response"):

            with st.expander("Technical details"):

                st.write(result["raw_response"])

        st.stop()


    # --------------------------------------------------
    # PROJECT NAME
    # --------------------------------------------------

    st.divider()

    st.header(
        result.get(
            "project_name",
            "Project Evaluation"
        )
    )


    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    st.markdown(
        f"""
        <div class="card">
            <b>Project Summary</b><br><br>
            {result.get("summary", "")}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # PROJECT HEALTH
    # --------------------------------------------------

    st.subheader("📊 Project Health")

    health = int(
        result.get(
            "project_health",
            0
        )
    )

    # Keep health between 0 and 100
    health = max(
        0,
        min(
            health,
            100
        )
    )

    st.progress(
        health / 100
    )

    st.markdown(
        f'<div class="score">{health} / 100</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # SCORE BREAKDOWN
    # --------------------------------------------------

    st.subheader("📈 Score Breakdown")

    scores = result.get(
        "scores",
        {}
    )

    score_data = [
        (
            "Problem",
            scores.get(
                "problem",
                0
            )
        ),
        (
            "Technology",
            scores.get(
                "technology",
                0
            )
        ),
        (
            "Innovation",
            scores.get(
                "innovation",
                0
            )
        ),
        (
            "Feasibility",
            scores.get(
                "feasibility",
                0
            )
        ),
        (
            "Completeness",
            scores.get(
                "completeness",
                0
            )
        ),
        (
            "Presentation",
            scores.get(
                "presentation",
                0
            )
        )
    ]

    columns = st.columns(3)

    for index, (name, value) in enumerate(score_data):

        with columns[index % 3]:

            st.markdown(
                f"""
                <div class="card">
                    <b>{name}</b><br>
                    <span class="score">{value}/100</span>
                </div>
                """,
                unsafe_allow_html=True
            )


    # --------------------------------------------------
    # PROJECT STRENGTHS
    # --------------------------------------------------

    st.subheader("🟢 Project Strengths")

    strengths = result.get(
        "strengths",
        []
    )

    if strengths:

        for item in strengths:

            st.write(
                "•",
                item
            )

    else:

        st.info(
            "No specific strengths were identified."
        )


    # --------------------------------------------------
    # CRITICAL ISSUES
    # --------------------------------------------------

    st.subheader("🔴 Critical Issues")

    critical_issues = result.get(
        "critical_issues",
        []
    )

    if critical_issues:

        for item in critical_issues:

            st.markdown(
                f"""
                <div class="card">
                    <b>{item.get("issue", "")}</b>
                    —
                    {item.get("severity", "")}
                    <br><br>
                    {item.get("why_it_matters", "")}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "No major critical issues were identified."
        )


    # --------------------------------------------------
    # POTENTIAL TECHNICAL / LOGIC ISSUES
    # --------------------------------------------------

    st.subheader(
        "🐞 Potential Technical / Logic Issues"
    )

    potential_bugs = result.get(
        "potential_bugs",
        []
    )

    if potential_bugs:

        for item in potential_bugs:

            st.markdown(
                f"""
                <div class="card">
                    <b>{item.get("bug", "")}</b>
                    —
                    {item.get("severity", "")}
                    <br><br>
                    {item.get("explanation", "")}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No potential technical or logic issues were identified."
        )


    # --------------------------------------------------
    # MISSING COMPONENTS
    # --------------------------------------------------

    st.subheader("📌 Missing Components")

    missing_components = result.get(
        "missing_components",
        []
    )

    if missing_components:

        for item in missing_components:

            st.write(
                "•",
                item
            )

    else:

        st.success(
            "No important missing components were identified."
        )


    # --------------------------------------------------
    # IMPROVEMENTS
    # --------------------------------------------------

    st.subheader("🛠️ Improvements Needed")

    improvements = result.get(
        "improvements",
        []
    )

    if improvements:

        for item in improvements:

            st.markdown(
                f"""
                <div class="card">
                    <b>{item.get("area", "")}</b>
                    —
                    {item.get("priority", "")}
                    <br><br>

                    <b>Current Problem:</b>
                    {item.get("current_problem", "")}

                    <br><br>

                    <b>Suggestion:</b>
                    {item.get("suggestion", "")}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No specific improvements were identified."
        )


    # --------------------------------------------------
    # RECOMMENDED FEATURES
    # --------------------------------------------------

    st.subheader("💡 Recommended Features")

    recommended_features = result.get(
        "recommended_features",
        []
    )

    if recommended_features:

        for item in recommended_features:

            st.write(
                "•",
                item
            )

    else:

        st.info(
            "No additional features were recommended."
        )


    # --------------------------------------------------
    # ACTION PLAN
    # --------------------------------------------------

    st.subheader(
        "🎯 Project Improvement Action Plan"
    )

    action_plan = result.get(
        "action_plan",
        []
    )

    if action_plan:

        for item in action_plan:

            st.markdown(
                f"""
                <div class="card">
                    <b>
                        Step {item.get("step", "")}
                    </b>
                    <br><br>

                    {item.get("action", "")}

                    <br><br>

                    <b>Priority:</b>
                    {item.get("priority", "")}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No action plan was generated."
        )


    # --------------------------------------------------
    # FINAL EVALUATION
    # --------------------------------------------------

    st.subheader("📝 Final Evaluation")

    st.markdown(
        f"""
        <div class="card">
            {result.get("final_summary", "")}
        </div>
        """,
        unsafe_allow_html=True
    )
