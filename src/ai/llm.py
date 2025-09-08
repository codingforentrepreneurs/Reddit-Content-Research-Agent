from functools import lru_cache
from langchain.chat_models import init_chat_model

from django.conf import settings

@lru_cache
def get_gemini_model():
    return init_chat_model(
            "gemini-2.5-flash", 
            model_provider="google_genai", 
            api_key=settings.GOOGLE_GEMINI_API_KEY)