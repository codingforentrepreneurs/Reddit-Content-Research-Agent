from functools import lru_cache
from langgraph.prebuilt import create_react_agent
from . import llm, prompts, schemas, tools

@lru_cache
def get_reddit_agent():
    model = llm.get_gemini_model()
    prompt = prompts.reddit_agent_prompt

    reddit_agent = create_react_agent(
        model=model,  
        tools=tools.reddit_tools,
        prompt=prompt,
        response_format=schemas.RedditCommunitesSchema
    )

    return reddit_agent

reddit_agent = get_reddit_agent()

def perform_get_reddit_communites(query):
    reddit_agent = get_reddit_agent()
    results = reddit_agent.invoke(
        {"messages": [{"role": "user", "content": f"{query}"}]},
        stream_mode="values"
    )
    community_data = [x.model_dump() for x in results["structured_response"].communities]
    return community_data