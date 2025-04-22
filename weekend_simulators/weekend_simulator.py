from weekend_simulators.config import Config
import random


class WeekendSimulator(Config):

    def __init__(self, track_name: str):
        self.context = {
            "Track": track_name,
            "Press Conference": self.press_conference(),
            "FP1": self.practice(),
            "FP2": self.practice(),
            "FP3": self.practice(),
            "Qualifying": self.qualifying(),
            "Sprint Race": self.race(),
            "Race": self.race(),
        }

    def press_conference(self) -> dict:
        return {"Weather": self.get_weather(), "Result Last Year": self.get_result()}

    def practice(self) -> dict:
        return {"Weather": self.get_weather(), "Result": self.get_result()}

    def qualifying(self) -> dict:
        qualifying = {
            "Weather": self.get_weather(),
            "Result": self.get_result(),
            "New Record": False,
        }

        if qualifying["Result"] == "1":
            if qualifying["Weather"] != "Wet":
                qualifying["New Record"] = random.choice([True, False])
        else:
            qualifying["Fastest"] = random.choice(self.other_drivers)

        return qualifying

    def race(self) -> dict:
        race = {"Weather": self.get_weather(), "Result": self.get_result()}

        if race["Result"] != "1":
            race["Winner"] = random.choice(self.other_drivers)

        return race

    def get_weather(self) -> str:
        return random.choices(
            list(self.weather_key_words.keys()),
            weights=list(self.weather_key_words.values()),
            k=1,
        )[0]

    def get_result(self) -> str:
        return random.choices(
            list(self.finishing_result.keys()),
            weights=list(self.finishing_result.values()),
            k=1,
        )[0]


if __name__ == "__main__":
    weekend_simulation = WeekendSimulator("Silverstone")
    print(weekend_simulation.context)
