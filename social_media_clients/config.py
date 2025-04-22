class Config:

    post_system_content = {
        "role": "system",
        "content": "You're an F1 driver writing a social media post",
    }

    comment_system_context = {
        "role": "system",
        "content": "You're an F1 driver named Speedy Quick commenting on a fan's social media post",
    }

    fan_post_context = {
        "role": "system",
        "content": "You're an F1 fan writing a social media post",
    }

    result_hashtags = {
        "1": ["#Winner", "#Win", "#Gold"],
        "2": ["#Podium", "#Second"],
        "3": ["#Podium", "#Third"],
        "6": ["#KeepPushing", "#TopSix"],
        "10": ["#TopTen", "#LetsGo"],
        "18": ["#NeverGiveUp"],
    }
