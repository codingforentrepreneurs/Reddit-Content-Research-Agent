from functools import lru_cache
from langchain_brightdata import BrightDataSERP

from django.conf import settings 

@lru_cache
def get_serp_tool(search_engine="google"):
    return BrightDataSERP(
        bright_data_api_key=settings.BRIGHT_DATA_SERP_API_KEY,
        search_engine=search_engine,
        country="us",
        parse_results=True
    )



reddit_tools = [get_serp_tool()]