from large_language_models.large_language_model import LargeLanguageModelClient
# from large_language_models.mock_client import LargeLanguageModelClient
from weekend_simulators.weekend_simulator import WeekendSimulator
from social_media_clients.social_media_client import SocialMediaClient
import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class F1Agent:

    def __init__(self, track_name: str) -> None:
        logger.info("Starting F1Agent")
        large_language_model_client = LargeLanguageModelClient()

        weekend_simulator = WeekendSimulator(track_name=track_name)
        self.weekend_context = weekend_simulator.context

        self.social_media_client = SocialMediaClient(
            large_language_model_client=large_language_model_client,
            track_name=track_name,
            weekend_context=self.weekend_context,
        )

    def create_posts(self) -> None:
        logger.info("Creating posts...")
        for session, context in self.weekend_context.items():
            if session == "Track":
                continue

            logger.info(f"Session = {session}")

            self.weekend_context[session]["Post"] = self.social_media_client.post(
                session=session, context=context
            )

    def comments_and_likes(self) -> None:
        logger.info("Creating comments and likes...")
        for session, context in self.weekend_context.items():
            if session in ["Track", "Press Conference", "FP1", "FP2", "FP3"]:
                continue

            logger.info(f"Session = {session}")

            self.weekend_context[session]["Fan Interaction"] = (
                self.social_media_client.comment_and_like(
                    session=session, context=context
                )
            )

    def write_weekend_context_to_json(self) -> None:
        json_data = json.dumps(self.weekend_context, indent=10)

        # Write the JSON data to a file
        with open("weekend_context.json", "w") as file:
            file.write(json_data)

    def run(self) -> None:
        self.create_posts()
        self.comments_and_likes()
        self.write_weekend_context_to_json()

    def visualize(self):
        self.streamlit_frontend.run()


if __name__ == "__main__":
    track = "Silverstone"
    f1_agent = F1Agent(track_name=track)
    f1_agent.run()
