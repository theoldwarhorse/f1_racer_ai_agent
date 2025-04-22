import streamlit as st


class StreamlitFrontend:

    @staticmethod
    def run():
        st.set_page_config(page_title="F1 AI Agent")

        instructions = st.Page(
            "pages/instructions/instructions.py", title="Instructions"
        )
        social_media_interactions = st.Page(
            "pages/social_media_interactions/social_media_interactions.py"
        )
        pg = st.navigation([instructions, social_media_interactions])
        pg.run()


if __name__ == "__main__":
    streamlit_frontend = StreamlitFrontend()
    streamlit_frontend.run()
