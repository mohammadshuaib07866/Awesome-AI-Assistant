from langchain_openai import ChatOpenAI

from app.config.settings import ChatbotSettings


class ChatOpenAIModel:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            settings = ChatbotSettings()

            settings.validate()

            cls._model = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                temperature=settings.OPENAI_TEMPERATURE,
                api_key=settings.OPENAI_API_KEY,
                max_tokens=settings.OPENAI_MAX_TOKENS,
            )

        return cls._model
