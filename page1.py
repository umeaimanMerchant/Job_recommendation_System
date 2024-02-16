"""
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
    st.header("Welcome to Intervista")
    #st.text("Elevate Your Skills with Personalized Interview Training")

    if 'home' not in st.session_state:
        st.session_state.home = 0

    # choose type of input
    if st.session_state.home == 5: 

        if st.session_state["authentication_status"]:            
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.text("Elevate Your Skills with Personalized Interview Training")
            resume = st.button("Interview me on Resume and Job Description")
            if resume:
                st.session_state.home = 6

            position = st.button("Interview me on Skills")
            if position:
                st.session_state.page_index = 1

        else:
            st.write("Please log in or Sign up!")





    # About section****
    if st.session_state.home == 1: 
        st.title("Intervista:")
        


   

    ##  Resume 
    if st.session_state.home == 6:     
        st.text("Elevate Your Skills with Personalized Interview Training")   
        back = st.button("Back")

        if back:
            st.session_state.home = 5

         ## Take input job desc****

        jd=st.text_area("Paste the Job Description")

        # Resume
        uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

        submit = st.button("Next")

        if submit:
            jd_skills_ouput=[]
            resume_skills_ouput = []
            if jd != "":
                print(jd)
                skills_ouput = extract_skills_from_resume(jd)
                professions_ouput = extract_profession_from_resume(jd)

                #st.write("Moving to next page")
                #st.write(professions_ouput)
                jd_skills_ouput = skills_ouput + professions_ouput
                print(jd_skills_ouput)
            if uploaded_file is not None:
                text=input_pdf_text(uploaded_file)
                st.success(f"File uploaded Successfully!")
                
                skills_ouput = extract_skills_from_resume(text)
                professions_ouput = extract_profession_from_resume(text)
                resume_skills_ouput = skills_ouput + professions_ouput
                print(resume_skills_ouput)
                #st.write("Moving to next page")
                #st.write(professions_ouput)

            skills = jd_skills_ouput + resume_skills_ouput
            if len(skills) >0:
                st.session_state.skills_ouput = skills
                print("move to 2")
                st.session_state.stage = 0
                st.session_state.page_index = 3
            else:
                st.write("Please upload resume or enter job description!")
