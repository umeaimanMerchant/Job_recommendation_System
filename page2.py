import streamlit as st
import math

def show_page():
    st.title("AI Driven Mock Interview Experience")
    st.header("Current Skillset:")

    # Initialize the list only once using st.session_state
    if 'my_list' not in st.session_state:
        st.session_state.my_list = st.session_state.skills_ouput

    # Specify the number of columns
    num_columns = 3

    # Calculate the number of elements per column
    elements_per_column = math.ceil(len(st.session_state.my_list) / num_columns)

    # Use st.columns to create a layout with three columns
    columns = st.columns(num_columns)

    # Iterate over the elements and assign them to columns
    for i in range(elements_per_column):
        for j in range(num_columns):
            index = i * num_columns + j
            with columns[j]:
                if index < len(st.session_state.my_list):
                    item = st.session_state.my_list[index]
                    with st.expander(f"{item}", expanded=False):
                        # Display a delete button inside the expander
                        delete_button_key = f"delete_button_{item}"
                        if st.button("Delete", key=delete_button_key):
                            st.session_state.my_list.remove(item)
                            st.success(f"Deleted: {item}")
                            st.rerun()
                else:
                    break

    # Allow the user to add new items
    new_items = st.text_input("Add new items (comma-separated):")
    # Set a unique key for the Add button
    add_button_key = "add_button"
    if st.button("Add", key=add_button_key):
        if new_items:
            # Split the input into multiple skills
            new_skills = [skill.strip() for skill in new_items.split(",")]

            # Check for duplicates before adding to the list
            new_skills = list(set(new_skills) - set(st.session_state.my_list))

            # Add each new skill to the list
            st.session_state.my_list.extend(new_skills)
            st.success(f"Skills added: {', '.join(new_skills)}")
            
            # Update the input text and display a temporary message
            st.text_input("Add new items (comma-separated):", key="new_items", value=', '.join(new_skills))
            st.info("Temporary Message: Skill(s) added successfully.")
            
            st.rerun()

    # "Next" button to go to the next Streamlit app
    if st.button("Next", key="next_button"):
        # You can replace this with the code to launch the next Streamlit app
        st.success("Going to the next Streamlit app.")

        st.write("Moving to next page")
        #st.write(professions_ouput)
        #st.session_state.skills_ouput = skills_ouput
        return True
        
    else:
        return False


