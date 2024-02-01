"""
version 1.0:
QnA - 
    1. based on job description
    2. based on resume

Output - 
    1. type of question made by AI

Part 1:
    upload resume (list of skills & professions + add or remove skills)
"""

import streamlit as st
import os
import PyPDF2 as pdf
import json
import spacy

# get Input from user

# Resume: get text from pdf
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text


# Spacy
# Load spaCy model 
nlp = spacy.load("en_core_web_sm")

# skills
with open("skills_list.txt", "r", encoding="utf-8") as file:
    job_skills = [line.strip().lower() for line in file]

# tools
def extract_skills_from_resume(resume_text):
    # Process the resume text using spaCy
    doc = nlp(resume_text)

    # Initialize a set to store unique skills found in the resume
    found_skills = set()

    # Iterate through entities identified by spaCy
    for ent in doc.ents:
        if ent.text.lower() in job_skills:
            found_skills.add(ent.text.lower())

    return list(found_skills)

# skills
with open("professions_list.txt", "r", encoding="utf-8") as file:
    professions = [line.strip().lower() for line in file]

# tools
def extract_profession_from_resume(resume_text):
    # Process the resume text using spaCy
    doc = nlp(resume_text)

    # Initialize a set to store unique skills found in the resume
    found_professions = set()

    # Iterate through entities identified by spaCy
    for ent in doc.ents:
        if ent.text.lower() in professions:
            found_professions.add(ent.text.lower())

    return list(found_professions)

## streamlit app
def show_page():
    st.title("AI Driven Mock Interview Experience")
    st.text("Elevate Your Skills with Personalized Questions")
    jd=st.text_area("Paste the Job Description (WIP)")
    uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

    submit = st.button("Submit")

    if submit:
        if uploaded_file is not None:
            text=input_pdf_text(uploaded_file)
            st.success(f"File uploaded Successfully!")
            
            skills_ouput = extract_skills_from_resume(text)
            professions_ouput = extract_profession_from_resume(text)

            #st.write("Moving to next page")
            #st.write(professions_ouput)
            st.session_state.skills_ouput = skills_ouput + professions_ouput
            st.session_state.page_index = 1

    if st.button("Add skills Manually"):
        st.session_state.skills_ouput = []
        st.session_state.page_index = 1


