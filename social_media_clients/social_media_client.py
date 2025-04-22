from social_media_clients.config import Config
from large_language_models.large_language_model import LargeLanguageModelClient
import re
import random
from textblob import TextBlob


class SocialMediaClient(Config):

    def __init__(
        self,
        large_language_model_client: LargeLanguageModelClient,
        track_name: str,
        weekend_context: dict,
    ):
        self.large_language_model_client = large_language_model_client
        self.track_name = track_name
        self.weekend_context = weekend_context
        self.previous_results = " Previous results"

    def post(self, session: str, context: dict) -> str:
        content = self.get_post_prompt_content(session, context)
        post = self.generate_post(content)
        post = self.add_post_hashtags(post, session, context)
        return post

    def get_post_prompt_content(self, session: str, context: dict) -> str:
        content = ""
        if session == "Press Conference":
            content = f"""
                You just finished the press conference at {self.track_name}.
                Weather forcast for the weekend says {context["Weather"]}.
                Last year you finished the race in position {context["Result Last Year"]}."""

        if session in ["FP1", "FP2", "FP3"]:
            content = f"""
                You're at {self.track_name} in {context["Weather"]} weather 
                you finished {session} in position {context["Result"]}.
                """
            self.previous_results += f""" {session}-P{context["Result"]}"""

        if session == "Qualifying":
            content = f"""
            You just qualified in position {context["Result"]}
            at {self.track_name} in {context["Weather"]} weather. """
            content += self.previous_results + "."
            self.previous_results += f""" {session}-P{context["Result"]}"""

            if context["New Record"]:
                content += " You set a new lap record!"

            if "Fastest" in list(context.keys()):
                content += f""" Congratulate {context["Fastest"]} for taking pole."""

        if session in ["Sprint Race", "Race"]:
            content = f"""You just finished the {session} in position {context["Result"]}
            at {self.track_name} in {context["Weather"]} weather."""
            content += self.previous_results
            self.previous_results += f""" {session}-P{context["Result"]}""" + "."

            if "Winner" in list(context.keys()):
                content += f""" Congratulate {context["Winner"]} for winning"""

        return content

    def generate_post(self, content: dict) -> str:
        chat = [self.post_system_content]
        prompt = {"role": "user", "content": content}
        chat.append(prompt)
        post = self.large_language_model_client.generate(chat)
        # post = "This is sentence 1. Here is two. and now its gets cut o"
        post = self.trim_last_sentence(post)
        return post

    def add_post_hashtags(self, post: str, session: str, context: dict) -> str:
        if "Press Conference" != session:
            post += f" #{session.replace(' ','')} "
            post = post.replace("#Race", "#GrandPrix")
            post += random.choice(self.result_hashtags[context["Result"]])
        else:
            post += f" #{self.track_name}"

        return post

    def comment_and_like(self, session: str, context: dict) -> dict:
        fan_post = self.get_fan_post(session, context)
        comment = self.get_comment(fan_post)
        like = self.like_fan_post(fan_post)
        return {"Fan Post": fan_post, "Comment": comment, "Like": like}

    def get_fan_post(self, session: str, context: dict) -> str:
        fan_chat = [self.fan_post_context]
        fan_content = f"""You're an F1 fan supporting Speedy Quick who just finished {session}-P{context["Result"]}."""
        fan_prompt = {"role": "user", "content": fan_content}
        fan_chat.append(fan_prompt)
        fan_post = self.large_language_model_client.generate(fan_chat)
        # fan_post = "Fan post."
        fan_post = self.trim_last_sentence(fan_post)
        return fan_post

    def get_comment(self, fan_post: str) -> str:
        chat = [self.post_system_content]
        prompt = {
            "role": "user",
            "content": f"""As formula one driver Speedy quick reply to your fan's post: {fan_post}""",
        }
        chat.append(prompt)
        comment = self.large_language_model_client.generate(chat)
        # comment = "comment in response to fan."
        comment = self.trim_last_sentence(comment)
        return comment

    @staticmethod
    def like_fan_post(fan_post: str) -> bool:
        blob = TextBlob(fan_post)
        polarity = blob.sentiment.polarity
        like = polarity > 0
        return like

    @staticmethod
    def trim_last_sentence(text: str) -> str:
        # Split the text into sentences using a regular expression
        sentences = re.split(r"(?<=[.!?])\s+", text)

        # Check if the last sentence ends with a period, exclamation mark, or question mark
        last_sentence = sentences[-1]
        if last_sentence and last_sentence[-1] in [".", "!", "?"]:
            # If the last sentence is complete, return the original text
            return text

        # If the last sentence is incomplete, remove it and join the remaining sentences
        trimmed_sentences = sentences[:-1]
        trimmed_text = " ".join(trimmed_sentences)

        return trimmed_text
