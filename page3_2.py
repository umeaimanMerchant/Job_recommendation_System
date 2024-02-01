##page 3 code- 3 models

import streamlit as st
from qna_1 import *
import speech_recognition as sr

# Obtain audio from the microphone
recognizer = sr.Recognizer()

# global variables
question = ""
user_answer = ""
accuracy = 0

# Variable to check if recording is in progress
recording_in_progress = False

def start_recording(recording_in_progress):
    user_output = ""
    print("Recoding started")
    # Infinite loop for continuous recording
    chunk_count = 0 # Adjust the duration of each recording chunk

    # Infinite loop for continuous recording
    
    with sr.Microphone() as source:
        #st.text("Say something!")
        if recording_in_progress:

            try:
                # Listen for the specified chunk duration
                audio = recognizer.listen(source,  timeout=5)
                recognized_text = recognizer.recognize_google(audio)
                st.text(" - " + recognizer.recognize_google(audio))
                user_output += recognized_text + " "
            except sr.UnknownValueError:
                st.text("Could not understand audio")
            except sr.WaitTimeoutError:
                st.text("Timeout. No speech detected in the last")

    return user_output

def stop_recording():
    start_recording(False)
    st.text("recording stoped")
    

def set_state(i):
    st.session_state.stage = i


def show_page():
    global question
    global user_answer
    global accuracy
    if 'stage' not in st.session_state:
        st.session_state.stage = 2

    
    st.title("Gemini Chatbot")

    topics = ["SQL", "Python"]
    
    st.write("Let's start with the mock interview!")
    topic = topics[0]
    start = st.button("Start", on_click=set_state, args=[4])

    # create question
    if st.session_state.stage == 4:    
        chat_history = read_chat_log()[:1000]
        
        question = generate_question(topic, chat_history=chat_history)
        st.session_state.question = question
        st.write(f"Question: {question}")
        st.button("Start Recording", on_click=set_state, args=[5])

    #start recording
    if st.session_state.stage == 5:  
        # Initialize variables
        recording_in_progress = False

        st.write(f"Question: {st.session_state.question}")
        st.write("Stop recording : only once you can see your answer on screen)")
        start = st.button("Start Recording")
        st.session_state.user_answer = ""
        stop_button = st.button("Stop Recording ", on_click=set_state, args=[6])
        if start:
            st.text("Recording in progress...")
            recording_in_progress = True
            
            user_answer = start_recording(True)
            print(user_answer)
            st.session_state.user_answer = user_answer +""

        
    # stop recording
    if st.session_state.stage == 6:  
    
        stop_recording()
        #global user_answer
        #global question
        
        st.text("Recording stopped.")
        st.write(f"Question: {st.session_state.question}")
        st.write(f"Answer: {st.session_state.user_answer}")

        ans_len = len(st.session_state.user_answer)
        ai_answer = generate_answer(st.session_state.question, "SQL", ans_len + 10)
        st.write(f"correct Answer: {ai_answer}")

        accuracy = check_answer(ai_answer, st.session_state.user_answer)
        st.write(f"Accuracy: {accuracy}")
        
        save_chat_log(st.session_state.question, st.session_state.user_answer, accuracy, ai_answer)

                

    if st.session_state.stage >= 7:
        st.text("Gemini: That's the end of our questions. Thank you for participating!")

#if __name__ == "__main__":
#    main()
