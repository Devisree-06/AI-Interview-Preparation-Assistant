import streamlit as st
import google.generativeai as genai
import re

# -----------------------------
# Gemini Configuration
# -----------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 220px;
    font-size: 18px;
}

.stTextArea textarea {
    border-radius: 10px;
}

h1 {
    color: #0E4D92;
}
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.title("🤖 AI Interview Assistant")

    st.markdown("---")

    st.write("### Features")

    st.write("✅ HR Interview")
    st.write("✅ Python Interview")
    st.write("✅ AI Interview")
    st.write("✅ SQL Interview")
    st.write("✅ JAVA Interview")
    st.write("✅ DSA Interview")
    st.write("✅ Gemini Evaluation")
    st.write("✅ Final Score")

st.title("🤖 AI Interview Preparation Assistant")
st.write("Practice interview questions and get AI-powered feedback.")

# -----------------------------
# Question Bank
# -----------------------------
progress = st.progress(0)
questions = {
    "HR": [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?"
    ],
    "Python": [
        "What is Python?",
        "Explain list and tuple.",
        "What is Object-Oriented Programming?"
    ],
    "AI": [
        "What is Machine Learning?",
        "Difference between AI and ML?",
        "Explain supervised learning."
    ],
    "SQL":[
        "What is SQL?",
        "Explain JOIN.",
        "What is normalization?"
    ],

    "Java":[
        "Explain JVM.",
        "What is inheritance?",
        "Difference between JDK and JRE?"
    ],

    "DSA":[
        "What is Stack?",
        "Explain Queue.",
        "Binary Search?"
    ]
}

# -----------------------------
# Session State
# -----------------------------
if "started" not in st.session_state:
    st.session_state.started = False

# -----------------------------
# User Details
# -----------------------------
name = st.text_input("Enter your Name")
uploaded_resume = st.file_uploader(
    "Upload Resume (Optional)",
    type=["pdf", "docx"]
)
if uploaded_resume:
    st.success("Resume uploaded successfully!")
    st.info("AI can analyze your resume and generate personalized questions.")

category = st.selectbox(
    "Select Interview Category",
    ["HR", "Python", "AI", "SQL", "Java", "DSA"]
)
# -----------------------------
# Start Interview
# -----------------------------
if st.button("Start Interview"):
    st.session_state.started = True

# -----------------------------
# Interview Section
# -----------------------------
if st.session_state.started:

    st.success(f"Welcome {name}!")
    st.subheader(f"{category} Interview")

    answers = {}

    for i, question in enumerate(questions[category]):
        progress.progress((i + 1) / len(questions[category]))
        st.write(f"Progress: {i+1}/{len(questions[category])}")
        st.subheader(question)
        answers[question] = st.text_area(
            "Your Answer",
            key=f"answer_{i}"
        )
    # -------------------------
# Evaluate Button
# -------------------------
if st.button("Evaluate Interview"):

    total_score = 0
    answered = 0

    st.header("📊 Interview Evaluation")

    for question, answer in answers.items():

        if answer.strip() == "":
            st.warning(f"Please answer: {question}")
            continue

        answered += 1

        prompt = f"""
You are an expert technical interviewer.

Evaluate the following answer.

Question:
{question}

Candidate Answer:
{answer}

Return in this format:

Score: X/10

Strengths:
- point 1
- point 2

Weaknesses:
- point 1
- point 2

Suggestions:
- point 1
- point 2
"""

        response = model.generate_content(prompt)

        result = response.text

        st.markdown("---")
        st.subheader(question)
        st.write(result)

        # Extract score
        match = re.search(r'(\d+)\s*/\s*10', result)

        if match:
            total_score += int(match.group(1))

    # -------------------------
    # Final Score
    # -------------------------

    if answered > 0:
        average = total_score / answered
    else:
        average = 0

    if average >= 8:
        performance = "Excellent 🌟"
    elif average >= 6:
        performance = "Good 👍"
    else:
        performance = "Needs Improvement 📚"

    st.markdown("---")
    st.header("🏆 Final Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Score", f"{average:.1f}/10")

    with col2:
        st.metric("Questions Answered", answered)

    with col3:
        st.metric("Performance", performance)

    if average >= 8:
        st.success("Excellent Performance 🌟")

    elif average >= 6:
        st.info("Good Performance 👍")

    else:
        st.error("Needs Improvement 📚")

    st.balloons()

    st.write(
        f"Thank you **{name}** for using the AI Interview Preparation Assistant!"
    )

    # -------------------------
    # Download Report
    # -------------------------

    report = f"""
AI Interview Preparation Assistant

Name : {name}

Category : {category}

Questions Answered : {answered}

Average Score : {average:.1f}/10

Performance : {performance}

Thank you for using AI Interview Preparation Assistant.
"""

    st.download_button(
        label="📄 Download Report",
        data=report,
        file_name="Interview_Report.txt",
        mime="text/plain"
    )
    from datetime import datetime
    st.write("Date:", datetime.now().strftime("%d-%m-%Y"))

if st.button("🔄 Restart Interview"):
    st.session_state.started = False
    st.rerun()

st.markdown("---")
st.caption("Developed by DEVISREE R,  Edunet Foundation 6 Weeks AI Internship Project")
