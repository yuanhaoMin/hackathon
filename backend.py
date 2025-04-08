import os
from enum import Enum

from openai import OpenAI


class Language(Enum):
    GERMAN = "German"
    ENGLISH = "English"
    SPANISH = "Spanish"


SUPPORTED_LANGUAGES = [lang.value for lang in Language]


class Message(Enum):
    AWESOME = "Awesome!"
    GREAT_POST = "Great post!"
    EXCELENTE = "¡Excelente!"
    TOLL_GEMACHT = "Toll gemacht!"
    LOVED_THIS = "Loved this."
    ME_ENCANTO = "Me encantó esto."
    SEHR_INSPIRIEREND = "Sehr inspirierend!"


class Platform(Enum):
    INSTAGRAM = "Instagram"
    LINKEDIN = "LinkedIn"
    X = "X"


def get_trending_topics(platform):
    """
    Return a list of mock trending topics based on the chosen platform.
    """
    trending_topics = {
        Platform.INSTAGRAM.value: [
            "#artist",
            "#beauty",
            "#catlovers",
            "#foodie",
            "#love",
            "#makeup",
        ],
        Platform.LINKEDIN.value: [
            "DigitalMarketing,",
            "Entrepreneurship",
            "HumanResources",
            "Innovation",
        ],
        Platform.X.value: [
            "#BlackMonday",
            "#TechTrends",
            "#TrumpTariffs",
        ],
    }
    return trending_topics.get(platform, ["General Trend"])


def generate_post(topics, platform):
    """
    Generate a mock social media post based on a topic and a chosen platform.
    """
    languages = ", ".join(SUPPORTED_LANGUAGES)
    return f"[{platform} Post] An exciting post about {topics}! Multilingual support: {languages}. #topic #example"


def get_reply_suggestions(comment):
    suggestions = {
        Message.AWESOME: ["Thanks for the support!", "Glad you liked it 😊"],
        Message.GREAT_POST: ["Thank you!", "Appreciate it a lot!"],
        Message.EXCELENTE: ["¡Muchas gracias!", "Me alegra que te haya gustado 😊"],
        Message.TOLL_GEMACHT: ["Vielen Dank!", "Freut mich, dass es dir gefällt!"],
        Message.LOVED_THIS: ["Glad you enjoyed it!", "Thanks a lot ❤️"],
        Message.ME_ENCANTO: ["¡Qué bueno que te gustó!", "Gracias por tu apoyo 🙌"],
        Message.SEHR_INSPIRIEREND: ["Danke dir!", "Das freut mich sehr 😊"],
    }
    return suggestions.get(comment, ["Thanks", "Thank you", "¡Gracias!", "Danke!"])

def get_platforms():
    platforms = [
        {
            "name": "X",
        },
        {
            "name": "Instagram",
        },
        {
            "name": "LinkedIn",
        },
        {
            "name": "Facebook",
        }
    ]
    return platforms

def get_social_media_posts():
    posts = [
        {
            "platform": "X",
            "sender": "anna_meyer89",
            "language": Language.GERMAN.value,
            "message": Message.TOLL_GEMACHT.value,
            "time": "2025-04-08 08:42",
        },
        {
            "platform": "Facebook",
            "sender": "john.smith23",
            "language": Language.ENGLISH.value,
            "message": Message.LOVED_THIS.value,
            "time": "2025-04-08 09:18",
        },
        {
            "platform": "Instagram",
            "sender": "laura_gomez",
            "language": Language.SPANISH.value,
            "message": Message.ME_ENCANTO.value,
            "time": "2025-04-08 09:55",
        },
        {
            "platform": "LinkedIn",
            "sender": "michael.schulz",
            "language": Language.GERMAN.value,
            "message": Message.SEHR_INSPIRIEREND.value,
            "time": "2025-04-08 10:02",
        },
        {
            "platform": "X",
            "sender": "jane.doe_101",
            "language": Language.ENGLISH.value,
            "message": Message.GREAT_POST.value,
            "time": "2025-04-08 10:45",
        },
        {
            "platform": "Instagram",
            "sender": "carla_martinez",
            "language": Language.SPANISH.value,
            "message": Message.EXCELENTE.value,
            "time": "2025-04-08 11:27",
        },
    ]
    return posts


def translate_reply(text, language):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-4o",
        input=f"Please translate the following text between ### into {language}. Only show the translation, no other text.\n\n###{text}###",
    )
    return response.output_text


def generate_reply(text, language, original):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    if not text:
      response = client.responses.create(
          model="gpt-4o",
          input=f"Someone replied to you on social media with the text between ###.\nPlease generate a written response in the language of {language}. Only show the formulated reply, no other text.\n###{original}###",
      )
      return response.output_text

    response = client.responses.create(
        model="gpt-4o",
        input=f"Someone replied to you on social media with the text between ###.\nWe already have a draft for a response, it comes after the original message. Please generate a written response in the selected language: {language}. Only show the formulated reply, no other text.\n###{original}###\n{text}",
    )
    return response.output_text
