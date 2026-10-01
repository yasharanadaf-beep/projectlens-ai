import streamlit as st
from extractor import extract_text
from agent import analyze_project

st.set_page_config(page_title="ProjectLens", page_icon="🔎", layout="wide")

st.markdown('''<style>
.stApp {background:#f7f9fc;}
.title {font-size:42px;font-weight:800;color:#17324d;}
.sub {font-size:18px;color:#5d6b7a;}
.card {background:white;padding:20px;border-radius:14px;border:1px solid #e5eaf0;margin:10px 0;}
.score {font-size:28px;font-weight:800;color:#17324d;}
</style>''', unsafe_allow_html=True)

st.markdown('<div class="title">🔎 PROJECTLENS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">AI-powered Project Evaluation & Improvement Agent</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload your project report", type=["pdf", "pptx"])

if uploaded:
    st.success(f"Uploaded: {uploaded.name}")
    if st.button("🤖 Analyze Project", type="primary", use_container_width=True):
        with st.spinner("Reading and analyzing your project..."):
            text = extract_text(uploaded)
            if not text.strip():
                st.error("No readable text was found in the file.")
                st.stop()
            result = analyze_project(text)
            st.session_state["result"] = result

result = st.session_state.get("result")

if result:
    if result.get("error"):
        st.error(result["error"])
        if result.get("raw_response"):
            with st.expander("Technical details"):
                st.write(result["raw_response"])
        st.stop()

    st.divider()
    st.header(result.get("project_name", "Project Evaluation"))
    st.markdown(f'<div class="card"><b>Summary</b><br>{result.get("summary","")}</div>', unsafe_allow_html=True)

    health = int(result.get("project_health", 0))
    st.subheader("📊 Project Health")
    st.progress(max(0, min(health, 100)) / 100)
    st.markdown(f'<div class="score">{health} / 100</div>', unsafe_allow_html=True)

    st.subheader("Score Breakdown")
    scores = result.get("scores", {})
    cols = st.columns(3)
    for i, (name, value) in enumerate([
        ("Problem", scores.get("problem",0)),
        ("Technology", scores.get("technology",0)),
        ("Innovation", scores.get("innovation",0)),
        ("Feasibility", scores.get("feasibility",0)),
        ("Completeness", scores.get("completeness",0)),
        ("Presentation", scores.get("presentation",0))
    ]):
        with cols[i % 3]:
            st.markdown(f'<div class="card"><b>{name}</b><br><span class="score">{value}/100</span></div>', unsafe_allow_html=True)

    st.subheader("🟢 Project Strengths")
    for x in result.get("strengths", []): st.write("•", x)

    st.subheader("🔴 Critical Issues")
    for x in result.get("critical_issues", []):
        st.markdown(f"**{x.get('issue','')}** — {x.get('severity','')}  
{x.get('why_it_matters','')}")

    st.subheader("🐞 Potential Technical / Logic Issues")
    for x in result.get("potential_bugs", []):
        st.markdown(f"**{x.get('bug','')}** — {x.get('severity','')}  
{x.get('explanation','')}")

    st.subheader("📌 Missing Components")
    for x in result.get("missing_components", []): st.write("•", x)

    st.subheader("🛠️ Improvements Needed")
    for x in result.get("improvements", []):
        st.markdown(f"**{x.get('area','')}** — {x.get('priority','')}  
Current: {x.get('current_problem','')}  
Suggestion: {x.get('suggestion','')}")

    st.subheader("💡 Recommended Features")
    for x in result.get("recommended_features", []): st.write("•", x)

    st.subheader("🎯 Project Improvement Action Plan")
    for x in result.get("action_plan", []):
        st.markdown(f"**Step {x.get('step','')}:** {x.get('action','')} — {x.get('priority','')}")

    st.subheader("📝 Final Evaluation")
    st.markdown(f'<div class="card">{result.get("final_summary","")}</div>', unsafe_allow_html=True)
