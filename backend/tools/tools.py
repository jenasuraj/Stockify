from langchain_tavily import TavilySearch
import praw
reddit = praw.Reddit(client_id="YwkiOjMYzWuXo32YTO418g",
                     client_secret="HhNxSCRM4x3_U-6347oXZLhAtIkZ2g",
                     user_agent="stockify")

tavily = TavilySearch(max_results=3, topic="general")
tools=[tavily]
