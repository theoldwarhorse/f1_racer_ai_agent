from pages.social_media_interactions.config import Config
import streamlit as st
import json


class SocialMediaInteractions(Config):

    def page_display(self):
        st.header("Speedy Quick's Social Media Platform")

        # Select a file to get the weekend context from

        selected_option = st.selectbox(self.selection_prompt, self.options)

        with open(selected_option, "r") as file:
            data = json.load(file)
        st.subheader(f"Race weekend at {data['Track']}")

        for session, context in data.items():
            if session == "Track":
                continue

            with st.expander(f"Session: {session}"):
                st.write(f"**Speedy's Post:** {context['Post']}")
                if "Fan Interaction" in list(context.keys()):
                    st.write(f"**Fan:** {context['Fan Interaction']['Fan Post']}")
                    st.write(
                        f"**Speedy's Comment:** {context['Fan Interaction']['Comment']}"
                    )
                    if context["Fan Interaction"]["Like"]:
                        reaction = "👍"
                    else:
                        reaction = "👎"
                    st.write(f"**Speedy's Reaction:** {reaction}")


social_media_interactions = SocialMediaInteractions()
social_media_interactions.page_display()
