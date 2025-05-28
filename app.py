import streamlit as st
from utils.quiz_generator import extract_text, text_to_questions_pipeline

st.set_page_config(page_title="MCQ Generator", page_icon="📝")

if "questions" not in st.session_state:
    st.session_state.questions = None
if "text" not in st.session_state:
    st.session_state.text = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "page" not in st.session_state:
    st.session_state.page = "quiz"

def reset_quiz():
    st.session_state.questions = None
    st.session_state.text = None
    st.session_state.user_answers = {}
    st.session_state.page = "quiz"

if st.session_state.page == "quiz":
    st.title("MCQ Generator")

    uploaded_file = st.file_uploader("Upload a PDF, DOCX or TXT file", type=["pdf", "docx", "txt"])
    max_choice = st.slider("How many questions to generate?", min_value=1, max_value=20, value=10)

    if uploaded_file:
        if st.button("Generate Questions"):
            st.session_state.text = extract_text(uploaded_file)
            st.session_state.questions = text_to_questions_pipeline(st.session_state.text, max_choice=max_choice)
            st.session_state.user_answers = {}

    if st.session_state.questions:
        st.subheader("Generated Questions")

        with st.form("mcq_form"):
            for q_id, q in st.session_state.questions.items():
                st.write(f"**Q{q_id+1}:** {q['question']}")
                options = q['options']
                choice = st.radio(
                    f"Choose your answer for Q{q_id+1}:",
                    options=list(options.values()),
                    key=f"q{q_id}"
                )
                st.session_state.user_answers[q_id] = choice
                st.markdown("---")

            submitted = st.form_submit_button("Check Answers")

        if submitted:
            st.session_state.page = "results"
            st.rerun()

elif st.session_state.page == "results":
    st.title("Results")

    correct_count = 0
    total = len(st.session_state.questions)
    st.markdown(f"### You got **{correct_count}** out of **{total}** correct.")
    for q_id, q in st.session_state.questions.items():
        correct_key = q['answer']
        correct_answer = q['options'][correct_key]
        selected = st.session_state.user_answers.get(q_id)

        st.write(f"**Q{q_id+1}:** {q['question']}")

        if selected == correct_answer:
            st.success(f"✅ Your answer: {selected}")
            correct_count += 1
        else:
            st.error(f"❌ Your answer: {selected}")
            st.success(f"✅ Correct answer: {correct_answer}")

        st.markdown("---")

    

    if st.button("Retake Quiz"):
        reset_quiz()
        st.rerun()
