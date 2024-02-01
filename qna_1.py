"""
this code has the following funtions
    1. gemini response
    2. create questions
    3. create answer
    4. check accuracy - not correct 
    5. maintain chat history- read and write
    6. find difficulty level- WIP
    7. make size of ai_answer- around same as user_answer
    8. calculate skill + difficulty wise knowledge point(1-10(highest))
    9. stop function- 
    10. start with more general questions?- what question- then go with examples based question- 
    11. size of generated question and answer
    12. inter realted topics
    13. user can select behavior or conception skill?- start of app

    create app- deploy it
"""

import time
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

## load all our environment variables
load_dotenv() 

#Get api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Genimi response
def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def generate_question(topic, difficulty="basis", chat_history=""):
    #Prompt Template
    input_prompt="""
    Hey Act Like a skilled or very experience interviewer with a deep understanding of {}.
    Your task is to design conceptual questions based on the skill mentioned, difficulty level and previous history chat. 
    input:
    topic to ask question from: {}
    difficulty level: {}
    chat history:{}
    Output: 1 Question character size(max 100)
    only put question
    """.format(topic,difficulty,chat_history, topic)

    response=get_gemini_repsonse(input_prompt)
    #print(response) 
    return response
    

def generate_answer(topic,question,ans_len=20):
    #Prompt Template -change
    input_prompt="""
    Hey Act Like a skilled or very experience professional
    with a deep understanding of {}. Your task is to provide the answer to the given question. 
    Question: {}
    Output: Answer to the question given (char limit {})
    """.format(topic, question,ans_len)

    response=get_gemini_repsonse(input_prompt)
    #print(response) 
    return response
    

def check_answer(generated_answer, user_answer):
    #change
    input_prompt="""
    Hey Act check how accuracte is the user answer based on the answer provided by AI. output the accuracy as integer. 
    User answer: {}
    AI answer: {}
    Output: accuracy: [integer]
    """.format(user_answer,generated_answer)

    response=get_gemini_repsonse(input_prompt)
    #print(response) 
    return response

def save_chat_log(question, user_answer, accuracy,Ai_answer):
    with open('chat_log.txt', 'a') as log_file:
        log_file.write(f"Question: {question}\nUser Answer: {user_answer}\nAccuracy: {accuracy}\Generative_answer: {Ai_answer}\n\n")

def read_chat_log():
    with open('chat_log.txt', 'r') as log_file:
        return log_file.read()

def ask_question(topic, question_type="conceptual", difficulty= "basis"):
    chat_history = read_chat_log()[:1000]
    question = generate_question(topic,difficulty, chat_history)
    print(f"Gemini: {question}")

    user_answer = input("Your Answer: ")
    generated_answer = generate_answer(question )
    print(generated_answer)
    accuracy = check_answer(generated_answer, user_answer)

    save_chat_log(question, user_answer, accuracy, generated_answer)
    return accuracy

#topics = ["SQL"]
#difficulty_level = ["Basis", "Medium","Hard"]
#difficulty = "Basis"

#function function to find difficulty level
