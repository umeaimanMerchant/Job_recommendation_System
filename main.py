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
# main_app.py
import streamlit as st
import importlib
import page1, page2

def main():
    st.set_page_config(page_title="Multi-Page App", page_icon=":rocket:")
    # Define the list of pages
    pages = [ "page1", "page2", "page3_2"]
    page_index = st.session_state.get("page_index", 0)

    
    # Dynamically import and run the current page
    module_name = pages[page_index]
    module = importlib.import_module(module_name)
    module.show_page()

    # Use a sidebar to display navigation buttons
    st.sidebar.title("Navigation")
    
    # Button to navigate to Page 1
    if st.sidebar.button("Login"):
        #st.session_state.page_index = 0
        pass
    
    # Button to navigate to Page 2
    if st.sidebar.button("About"):
        #st.session_state.page_index = 1
        pass

    if st.sidebar.button("Sign Out"):
        #st.session_state.page_index = 2
        pass
    
    st.sidebar.text("Currently not working")
if __name__ == "__main__":
    main()
