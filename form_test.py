import streamlit as st

def show_page():
    # Define available skills
    skills = st.session_state.skills_ouput

    # Define available difficulty levels
    difficulty_levels = ["Easy", "Medium", "Hard"]

    # Create form to select skills, difficulty levels, and number of questions
    selected_skills = st.multiselect("Select skills:", skills)
    selected_difficulty = st.selectbox("Select difficulty level:", difficulty_levels)
    num_questions = st.number_input("Select number of questions (0-10):", min_value=1, max_value=10, value=5)

    # Custom button to add missing skills
    if st.button("Add Custom Skill"):
        custom_skill = st.text_input("Enter custom skill:")
        if st.button("Enter"):
            st.write(custom_skill)
            skills.append(custom_skill)

    # Display selected options
    #st.write("Selected Skills:", selected_skills)
    if st.button("Next.."):
        if selected_skills == []:
            st.error("Please add some skills!")
        else:
            st.session_state.selected_skills = selected_skills
            st.session_state.selected_difficulty = selected_difficulty
            st.session_state.num_questions = num_questions
            st.session_state.page_index = 2
    #st.write("Selected Difficulty Level:", selected_difficulty)
    #st.write("Number of Questions:", num_questions)
