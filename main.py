"""

"""
# main_app.py
import streamlit as st
import importlib
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


def main():
    # Italian name
    #st.set_page_config(page_title="Intervista", page_icon=":rocket:")
    # Define the list of pages
    pages = [ "page1", "page2", "page3", "form_test","report"]
    page_index = st.session_state.get("page_index", 0)

    
    # Dynamically import and run the current page
    module_name = pages[page_index]
    module = importlib.import_module(module_name)
    module.show_page()

    if 'home' not in st.session_state:
        st.session_state.home = 0
    # Use a sidebar to display navigation buttons
    st.sidebar.title("Navigation")

    if st.sidebar.button("Home"):
        # if condition-signed in already***
        st.session_state.home = 5
        st.session_state.page_index = 0
        pass
    
    # Button to navigate to Page 1
    if st.sidebar.button("Login"):
        st.session_state.home = 0

    if st.session_state.home == 0:
        authenticator.login()


        if st.session_state["authentication_status"]:            
            #st.write(f'Welcome *{st.session_state["name"]}*')
            st.session_state.home = 5
            st.session_state.page_index =0
            #st.title('Some content')
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')

    if st.sidebar.button("Sign up"):
         st.session_state.home = 2 

    if st.session_state.home == 2:
        st.title("Join to Intervista")
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)

            if email_of_registered_user:
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('User registered successfully')
                st.session_state.home = 0
        except Exception as e:
            st.error(e)
    
    
    # Button to navigate to Page 2
    if st.sidebar.button("About"):
        #st.session_state.home = 1
        st.session_state.page_index = 4

            # logout
        
    if st.session_state["authentication_status"]:
        if st.sidebar.button("Log out"):
            #st.session_state["authentication_status"] = None
            authenticator.logout()
            st.success('log out successfully')
            st.session_state.home = 0


if __name__ == "__main__":
    main()
