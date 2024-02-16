##page 3 code- 3 models

import streamlit as st
from qna_1 import *
import speech_recognition as sr
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# Obtain audio from the microphone
recognizer = sr.Recognizer()

# global variables
question = ""
user_answer = ""
accuracy = 0
no_question = 0

# Variable to check if recording is in progress
recording_in_progress = False

def stop_recording():
    st.text("recording stoped")
    

def set_state(i):
    st.session_state.stage = i

def show_page():
    global question
    global user_answer
    global accuracy
    if 'stage' not in st.session_state:
        st.session_state.stage = 2

    
    st.title("Intervista")

    topics = st.session_state.selected_skills
    if len(topics) ==0:
        st.session_state.page_index = 0
    
    st.write("Let's start with the mock interview!")
    topic = topics[0]
    start = st.button("Start", on_click=set_state, args=[4])
            
    # create question
    if st.session_state.stage == 4: 
        chat_history = read_chat_log()[:1000]
        global no_question   
        if st.session_state.num_questions < no_question:
            st.write("Intervista: That's the end of our questions. Thank you for participating!")
            if st.button("Exit"):
                st.session_state.page_index = 4
        else:
            no_question = no_question+1
            
            question = generate_question(topic, difficulty=st.session_state.selected_difficulty, chat_history=chat_history)
            st.session_state.question = question
            st.write(f"Question: {question}")
            st.button("Start Recording", on_click=set_state, args=[5])

    #start recording
    if st.session_state.stage == 5:  
        # Initialize variables
        recording_in_progress = False

        st.write(f"{st.session_state.question}")
        #start = st.button("Start Recording")
        st.session_state.user_answer = ""
        
        stt_button = Button(label="Speak", width=100)

        stt_button.js_on_event("button_click", CustomJS(code="""
            var recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
        
            recognition.onresult = function (e) {
                var value = "";
                for (var i = e.resultIndex; i < e.results.length; ++i) {
                    if (e.results[i].isFinal) {
                        value += e.results[i][0].transcript;
                    }
                }
                if ( value != "") {
                    document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
                }
            }
            recognition.start();
            """))

        result = streamlit_bokeh_events(
            stt_button,
            events="GET_TEXT",
            key="listen",
            refresh_on_update=False,
            override_height=75,
            debounce_time=0)
        
        global user_answer
        if result:
            if "GET_TEXT" in result:
                user_answer = user_answer + result.get("GET_TEXT")
                st.session_state.user_answer = user_answer
                st.write(result.get("GET_TEXT"))
        else:
            st.write(user_answer)
            st.write(".....")


        stop_button = st.button("Stop Recording ", on_click=set_state, args=[6])
        st.write("Press Speak to start recording")
        st.write("Press Stop recording: only once you can see your answer on screen)")



        
    # stop recording
    if st.session_state.stage == 6:  
    
        stop_recording()
        
        #global user_answer
        user_answer = ""
        #st.text("Recording stopped.")
        st.write(f"Question: {st.session_state.question}")
        st.write(f"Answer: {st.session_state.user_answer}")

        ans_len = len(st.session_state.user_answer)
        ai_answer = generate_answer(st.session_state.question, "SQL", ans_len + 10)
        st.write(f"correct Answer: {ai_answer}")

        accuracy = check_answer(ai_answer, st.session_state.user_answer)
        #st.write(f"Accuracy: {accuracy}")
        
        save_chat_log(st.session_state.question, st.session_state.user_answer, accuracy, ai_answer)


        

                

    if st.session_state.stage == 7:
        st.text("Gemini: That's the end of our questions. Thank you for participating!")

#if __name__ == "__main__":
#    main()
