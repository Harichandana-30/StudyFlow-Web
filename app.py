import streamlit as st

st.set_page_config(page_title="StudyFlow")

st.title("📚 StudyFlow")
st.subheader("Smart Study Planner")

task = st.text_input("Enter a study task")

if st.button("Add Task"):
    st.success(f"Task Added: {task}")

st.write("Your study progress will appear here.")