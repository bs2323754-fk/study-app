import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_icon="📚",
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Groq Client ─────────────────────────────────────────────────────────────
api_key = (st.secrets.get("GROQ_API_KEY") if hasattr(st, "secrets") else None) or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

def call_groq(prompt, system="You are an expert teacher and exam analyst.", json_mode=False):
    kwargs = dict(
        model="llama-3.3-70b-versatile",
        max_tokens=2048,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d1b2a 50%, #0a1628 100%);
    min-height: 100vh;
}

section.main > div {
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
}

[data-testid="stAppViewContainer"] {
    padding: 0 !important;
}

[data-testid="block-container"] {
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    padding-top: 1rem !important;
    max-width: 100% !important;
}

h1, h2, h3 { font-family: 'Lora', serif !important; color: #e8e0f5 !important; }

.main-title {
    font-family: 'Lora', serif !important;
    font-size: 2.8rem;
    background: linear-gradient(90deg, #818cf8, #c084fc, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
    padding-top: 1rem;
}

.subtitle {
    text-align: center;
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 2rem;
    letter-spacing: 0.02em;
}

.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(129,140,248,0.15);
    border-radius: 18px;
    padding: 1.8rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
}

.exam-topic {
    background: linear-gradient(135deg, rgba(129,140,248,0.1), rgba(56,189,248,0.07));
    border: 1px solid rgba(129,140,248,0.2);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.7rem;
    color: #e2d9f3;
}

.badge {
    display: inline-block;
    padding: 0.15rem 0.65rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}
.badge-high   { background: rgba(239,68,68,0.2);  color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.badge-medium { background: rgba(234,179,8,0.2);  color: #fde047; border: 1px solid rgba(234,179,8,0.3); }
.badge-low    { background: rgba(34,197,94,0.2);  color: #86efac; border: 1px solid rgba(34,197,94,0.3); }

.study-content {
    background: rgba(8,10,26,0.8);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 14px;
    padding: 1.8rem;
    color: #cbd5e1;
    line-height: 1.8;
    white-space: pre-wrap;
    font-size: 0.95rem;
}

.score-card {
    background: linear-gradient(135deg, rgba(129,140,248,0.15), rgba(192,132,252,0.1));
    border: 1px solid rgba(129,140,248,0.3);
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

.score-number {
    font-family: 'Lora', serif;
    font-size: 5rem;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

.grade-label { color: #a78bfa; font-size: 1.4rem; font-weight: 700; margin-top: 0.5rem; }

.step-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.4rem;
    margin-bottom: 1.8rem;
}
.step-pill   { padding: 0.3rem 0.9rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.04em; }
.step-done   { background: rgba(56,189,248,0.2);   color: #7dd3fc; border: 1px solid rgba(56,189,248,0.3); }
.step-active { background: rgba(129,140,248,0.3);  color: #a5b4fc; border: 1px solid rgba(129,140,248,0.5); }
.step-pending{ background: rgba(255,255,255,0.04); color: #475569; border: 1px solid rgba(255,255,255,0.08); }

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white !important;
    border: none !important;
    border-radius: 12px;
    padding: 0.65rem 1.5rem;
    font-weight: 600;
    font-size: 0.92rem;
    transition: all 0.25s;
    width: 100%;
}
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99,102,241,0.4);
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(129,140,248,0.25) !important;
    border-radius: 12px !important;
    color: #e2d9f3 !important;
    font-size: 0.93rem !important;
    line-height: 1.6 !important;
}

div[data-testid="stRadio"] label { color: #cbd5e1 !important; font-size: 0.95rem !important; }

.answer-box {
    background: rgba(34,197,94,0.08);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #86efac;
    margin-top: 0.6rem;
    font-size: 0.9rem;
    line-height: 1.6;
}

.wrong-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    border-radius: 12px;
    padding: 0.6rem 1rem;
    color: #fca5a5;
    font-size: 0.85rem;
    margin-top: 0.3rem;
}

hr { border-color: rgba(129,140,248,0.15) !important; }

/* Hide Streamlit branding */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="manage-app-button"] { display: none !important; }
.viewerBadge_container__1QSob { display: none !important; }
.viewerBadge_link__1S137 { display: none !important; }
button[kind="header"] { display: none !important; }

.progress-info { color: #64748b; font-size: 0.85rem; text-align: right; margin-bottom: 0.5rem; }
.q-number { color: #818cf8; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.3rem; }

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(129,140,248,0.15);
    border-radius: 10px;
    padding: 0.7rem 1rem;
}
div[data-testid="stMetric"] label { color: #64748b !important; font-size: 0.8rem !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #a5b4fc !important; font-size: 1.6rem !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": "upload",
        "syllabus": "",
        "exam_topics": [],
        "current_topic_idx": 0,
        "study_content": {},
        "test_questions": [],
        "user_answers": {},
        "score": 0,
        "test_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Step Bar ────────────────────────────────────────────────────────────────
STAGE_DISPLAY = ["upload", "analyze_done", "study", "test", "results"]
STAGE_LABELS  = {"upload": "📄 Upload", "analyze_done": "🔍 Analysis",
                 "study": "📖 Study", "test": "✍️ Test", "results": "🏆 Results"}

def step_bar(current):
    idx  = STAGE_DISPLAY.index(current) if current in STAGE_DISPLAY else 0
    html = '<div class="step-bar">'
    for i, s in enumerate(STAGE_DISPLAY):
        cls   = "step-done" if i < idx else ("step-active" if i == idx else "step-pending")
        html += f'<span class="step-pill {cls}">{STAGE_LABELS[s]}</span>'
        if i < len(STAGE_DISPLAY) - 1:
            html += '<span style="color:#1e293b;font-size:0.8rem">──</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 AI Study Buddy")
    st.markdown("*Powered by Groq + LLaMA 3.3*")
    st.markdown("---")

    stage_map = {
        "upload": "📄 Syllabus Upload", "analyze": "🔍 Analyzing...",
        "analyze_done": "✅ Analysis Ready", "study": "📖 Study Session",
        "test": "✍️ Taking Test", "results": "🏆 Results",
    }
    st.markdown(f"**Current Step:** {stage_map.get(st.session_state.stage, '')}")

    if st.session_state.exam_topics:
        st.markdown("---")
        st.markdown("**📌 Topics:**")
        for i, t in enumerate(st.session_state.exam_topics):
            cur  = st.session_state.current_topic_idx
            icon = ("✅" if i < cur else ("▶️" if i == cur else "⬜")) if st.session_state.stage == "study" else "📌"
            st.markdown(f"<small>{icon} {t.get('topic','')[:34]}</small>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Start Over"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown("""
    <div style="background:rgba(129,140,248,0.07);border:1px solid rgba(129,140,248,0.15);
    border-radius:12px;padding:1rem;margin-top:1rem;color:#94a3b8;font-size:0.83rem;line-height:1.7;">
    <b>How it works:</b><br>
    1️⃣ Paste your syllabus<br>
    2️⃣ AI identifies exam topics<br>
    3️⃣ Study each topic with AI notes<br>
    4️⃣ Take MCQ + Short Answer test<br>
    5️⃣ See your score & review answers
    </div>
    """, unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">📚 AI Study Buddy</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Paste your syllabus — AI will analyze, teach, and test you</p>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# STAGE 1 — UPLOAD
# ════════════════════════════════════════════════════════════
if st.session_state.stage == "upload":
    step_bar("upload")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📄 Paste Your Syllabus")
    st.markdown("Copy and paste your full syllabus below. The AI will read it and identify the most important exam topics.")

    syllabus = st.text_area(
        "Syllabus:", height=260, label_visibility="collapsed",
        placeholder=(
            "Example:\n\n"
            "Chapter 1: Cell Biology\n"
            "  - Cell structure and organelles\n"
            "  - Mitosis and Meiosis\n\n"
            "Chapter 2: Genetics\n"
            "  - Mendel's Laws\n"
            "  - DNA replication\n..."
        ),
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Analyze My Syllabus"):
            if syllabus.strip():
                st.session_state.syllabus = syllabus.strip()
                st.session_state.stage    = "analyze"
                st.rerun()
            else:
                st.error("⚠️ Please paste your syllabus before continuing.")
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# STAGE 2 — ANALYZE
# ════════════════════════════════════════════════════════════
elif st.session_state.stage == "analyze":
    step_bar("analyze_done")
    st.markdown("### 🔍 Analyzing your syllabus...")

    with st.spinner("AI is reading your syllabus and identifying exam topics. Please wait..."):
        prompt = f"""Analyze the following syllabus. Identify the most important topics likely to appear in an exam.

SYLLABUS:
{st.session_state.syllabus}

Return a JSON object with a single key "topics" — an array where each element has:
- "topic": short clear topic name
- "importance": "High", "Medium", or "Low"
- "likely_questions": array of 3 example exam questions
- "key_concepts": array of 3-5 key concepts

Return ONLY valid JSON. No markdown, no explanation."""

        try:
            raw    = call_groq(prompt, system="You are an expert exam analyst. Return only valid JSON.", json_mode=True)
            data   = json.loads(raw)
            topics = data.get("topics", list(data.values())[0] if isinstance(data, dict) else data)
            st.session_state.exam_topics = topics
            st.session_state.stage       = "analyze_done"
            st.rerun()
        except Exception as e:
            st.error(f"Error during analysis: {e}. Please try again.")
            st.session_state.stage = "upload"
            st.rerun()

# ════════════════════════════════════════════════════════════
# STAGE 3 — ANALYSIS RESULTS
# ════════════════════════════════════════════════════════════
elif st.session_state.stage == "analyze_done":
    step_bar("analyze_done")
    topics = st.session_state.exam_topics
    st.markdown(f"### ✅ Analysis Complete — {len(topics)} Exam Topics Found")

    col_l, col_r = st.columns([3, 1])
    with col_l:
        for i, topic in enumerate(topics):
            imp       = topic.get("importance", "Medium")
            badge_cls = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(imp, "badge-medium")
            imp_icon  = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(imp, "🟡")
            likely    = topic.get("likely_questions", [])
            concepts  = topic.get("key_concepts", [])
            st.markdown(f"""
            <div class="exam-topic">
                <span class="badge {badge_cls}">{imp_icon} {imp} Priority</span>
                <b style="color:#e8e0f5;font-size:1.05rem;display:block;margin-bottom:0.5rem;">{i+1}. {topic.get('topic','')}</b>
                <div style="color:#64748b;font-size:0.82rem;margin-bottom:0.3rem;">📝 <b>Likely questions:</b> {' · '.join(likely[:2])}</div>
                <div style="color:#64748b;font-size:0.82rem;">🔑 <b>Key concepts:</b> {', '.join(concepts[:4])}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_r:
        high = sum(1 for t in topics if t.get("importance") == "High")
        med  = sum(1 for t in topics if t.get("importance") == "Medium")
        low  = sum(1 for t in topics if t.get("importance") == "Low")
        st.metric("🔴 High Priority",   high)
        st.metric("🟡 Medium Priority", med)
        st.metric("🟢 Low Priority",    low)
        st.metric("📚 Total Topics",    len(topics))

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📖 Start Study Session →"):
            st.session_state.stage             = "study"
            st.session_state.current_topic_idx = 0
            st.rerun()

# ════════════════════════════════════════════════════════════
# STAGE 4 — STUDY
# ════════════════════════════════════════════════════════════
elif st.session_state.stage == "study":
    step_bar("study")
    topics = st.session_state.exam_topics
    idx    = st.session_state.current_topic_idx

    if idx >= len(topics):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎉 All Topics Covered!")
        st.markdown(f"You have studied all **{len(topics)} topics**. Are you ready to take the test?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Take the Test!"):
                st.session_state.stage          = "test"
                st.session_state.test_questions = []
                st.session_state.user_answers   = {}
                st.session_state.test_submitted = False
                st.rerun()
        with col2:
            if st.button("🔄 Review Topics Again"):
                st.session_state.current_topic_idx = 0
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        topic      = topics[idx]
        topic_name = topic.get("topic", "")

        st.markdown(f'<div class="progress-info">Topic {idx+1} of {len(topics)}</div>', unsafe_allow_html=True)
        st.progress(idx / len(topics))
        st.markdown(f"### 📖 {topic_name}")

        if topic_name not in st.session_state.study_content:
            with st.spinner(f"Generating study notes for '{topic_name}'..."):
                prompt = f"""You are an expert teacher preparing a student for an exam.

Syllabus context:
{st.session_state.syllabus[:600]}

Teach this topic clearly:
Topic: {topic_name}
Key concepts: {', '.join(topic.get('key_concepts', []))}
Exam question types: {', '.join(topic.get('likely_questions', []))}

Write a complete study guide with these sections:
1. OVERVIEW — What is this topic? (2-3 sentences)
2. KEY CONCEPTS — Explain each concept with examples
3. IMPORTANT POINTS — Bullet points to memorize for the exam
4. EXAM TIPS — How to answer common question types
5. QUICK MEMORY TRICKS — Mnemonics or tricks to remember key facts

Use clear, simple English. Focus entirely on exam preparation."""
                st.session_state.study_content[topic_name] = call_groq(prompt)

        st.markdown('<div class="study-content">', unsafe_allow_html=True)
        st.markdown(st.session_state.study_content[topic_name])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            if idx > 0:
                if st.button("⬅️ Previous Topic"):
                    st.session_state.current_topic_idx -= 1
                    st.rerun()
        with col2:
            if st.button("✅ Got It! Next Topic →"):
                st.session_state.current_topic_idx += 1
                st.rerun()
        with col3:
            if st.button("⏭️ Skip to Test"):
                st.session_state.stage          = "test"
                st.session_state.test_questions = []
                st.session_state.user_answers   = {}
                st.session_state.test_submitted = False
                st.rerun()

# ════════════════════════════════════════════════════════════
# STAGE 5 — TEST
# ════════════════════════════════════════════════════════════
elif st.session_state.stage == "test":
    step_bar("test")

    if not st.session_state.test_questions:
        with st.spinner("Generating your test questions based on the syllabus..."):
            topics_str = "\n".join([f"- {t.get('topic','')}" for t in st.session_state.exam_topics])
            prompt = f"""Create an exam test based on this syllabus.

SYLLABUS:
{st.session_state.syllabus[:1200]}

TOPICS:
{topics_str}

Return a JSON object with exactly this structure:
{{
  "mcqs": [
    {{
      "q": "Question?",
      "options": ["A) option one", "B) option two", "C) option three", "D) option four"],
      "answer": "A) option one",
      "explanation": "Why this answer is correct."
    }}
  ],
  "short_questions": [
    {{
      "q": "Short answer question?",
      "answer": "Model answer in 2-4 sentences."
    }}
  ]
}}

Rules: 5 MCQs, 3 short questions. Each MCQ has exactly 4 options labeled A) B) C) D).
"answer" must exactly match one option. Return ONLY valid JSON."""

            try:
                raw = call_groq(prompt, system="Return only valid JSON. No markdown.", json_mode=True)
                st.session_state.test_questions = json.loads(raw)
            except Exception as e:
                st.error(f"Error generating test: {e}")
                st.stop()

    questions = st.session_state.test_questions
    mcqs      = questions.get("mcqs", [])
    short_qs  = questions.get("short_questions", [])

    st.markdown("### ✍️ Exam Test")
    st.markdown(f"**{len(mcqs)} MCQs** + **{len(short_qs)} Short Answer Questions** from your syllabus.")
    st.markdown("---")

    st.markdown("#### Part A — Multiple Choice Questions")
    for i, q in enumerate(mcqs):
        st.markdown(f'<div class="q-number">Question {i+1} of {len(mcqs)}</div>', unsafe_allow_html=True)
        st.markdown(f"**{q['q']}**")
        sel = st.radio("", q.get("options", []), key=f"mcq_{i}", index=None, label_visibility="collapsed")
        if sel:
            st.session_state.user_answers[f"mcq_{i}"] = sel
        st.markdown("")

    st.markdown("---")
    st.markdown("#### Part B — Short Answer Questions")
    for i, q in enumerate(short_qs):
        st.markdown(f'<div class="q-number">Short Answer {i+1} of {len(short_qs)}</div>', unsafe_allow_html=True)
        st.markdown(f"**{q['q']}**")
        ans = st.text_area("Your answer:", key=f"short_{i}", height=110,
                           label_visibility="collapsed", placeholder="Write your answer here...")
        if ans.strip():
            st.session_state.user_answers[f"short_{i}"] = ans
        st.markdown("")

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 Submit Test & See Results"):
            score = sum(
                1 for i, q in enumerate(mcqs)
                if st.session_state.user_answers.get(f"mcq_{i}", "") == q.get("answer", "")
            )
            st.session_state.score          = score
            st.session_state.test_submitted = True
            st.session_state.stage          = "results"
            st.rerun()

# ════════════════════════════════════════════════════════════
# STAGE 6 — RESULTS
# ════════════════════════════════════════════════════════════
elif st.session_state.stage == "results":
    step_bar("results")

    mcqs     = st.session_state.test_questions.get("mcqs", [])
    short_qs = st.session_state.test_questions.get("short_questions", [])
    score    = st.session_state.score
    total    = len(mcqs)
    pct      = int((score / total) * 100) if total else 0
    grade    = "A+" if pct >= 90 else "A" if pct >= 80 else "B" if pct >= 70 else "C" if pct >= 60 else "F"
    emoji    = "🏆" if pct >= 80 else "😊" if pct >= 60 else "📚"
    msg      = (
        "Excellent! You have mastered this syllabus."         if pct >= 90 else
        "Great job! A little more practice and you'll ace it." if pct >= 80 else
        "Good effort. Review the topics you got wrong."        if pct >= 70 else
        "Keep studying — focus on the high-priority topics."   if pct >= 60 else
        "Don't give up! Go back and review the study notes."
    )

    st.markdown(f"""
    <div class="score-card">
        <div style="font-size:3.5rem;margin-bottom:0.3rem;">{emoji}</div>
        <div class="score-number">{score} / {total}</div>
        <div class="grade-label">Grade: {grade} &nbsp;·&nbsp; {pct}%</div>
        <div style="color:#64748b;margin-top:0.7rem;font-size:0.95rem;">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 MCQ Review")
    for i, q in enumerate(mcqs):
        user_ans   = st.session_state.user_answers.get(f"mcq_{i}", "")
        correct    = q.get("answer", "")
        is_correct = user_ans == correct
        st.markdown(f"**{'✅' if is_correct else '❌'} Q{i+1}. {q['q']}**")
        if is_correct:
            st.markdown(f'<div class="answer-box">✅ Correct! {q.get("explanation","")}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="wrong-box">Your answer: {user_ans or "Not attempted"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="answer-box">✅ <b>Correct:</b> {correct}<br>💡 <b>Explanation:</b> {q.get("explanation","")}</div>', unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")
    st.markdown("### ✍️ Short Answer Review")
    for i, q in enumerate(short_qs):
        user_ans = st.session_state.user_answers.get(f"short_{i}", "")
        st.markdown(f"**Q{i+1}. {q['q']}**")
        if user_ans:
            st.markdown(f"<small style='color:#7dd3fc;'>Your answer: {user_ans}</small>", unsafe_allow_html=True)
        else:
            st.markdown("<small style='color:#fca5a5;'>Not attempted</small>", unsafe_allow_html=True)
        st.markdown(f'<div class="answer-box">✅ <b>Model Answer:</b> {q.get("answer","")}</div>', unsafe_allow_html=True)
        st.markdown("")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Retake Test"):
            st.session_state.test_questions = []
            st.session_state.user_answers   = {}
            st.session_state.score          = 0
            st.session_state.stage          = "test"
            st.rerun()
    with col2:
        if st.button("📖 Review Study Notes"):
            st.session_state.stage             = "study"
            st.session_state.current_topic_idx = 0
            st.rerun()
    with col3:
        if st.button("🆕 New Syllabus"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()
