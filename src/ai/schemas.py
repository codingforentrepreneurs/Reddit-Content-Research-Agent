from pydantic import BaseModel, Field

class RedditCommunitySchema(BaseModel):
    name: str = Field(description="Formatted name for Reddit")
    url: str = Field(description="The complete url of the reddit community")
    subreddit_slug: str = Field(description="The slug of the subbreddit such as r/python or r/web or r/trending")
    member_count: int | None = Field(description="Current member count, if available.")

class RedditCommunitesSchema(BaseModel):
    communities: list[RedditCommunitySchema] = Field(description="The list of reddit communites")