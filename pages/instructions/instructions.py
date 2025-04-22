import streamlit as st


class Instructions:

    def __init__(self, instruction_filename: str):

        with open(instruction_filename, "r") as file:
            driver_profile = file.read()
            st.markdown(driver_profile)


readme_file = "README.md"
Instructions(instruction_filename=readme_file)
