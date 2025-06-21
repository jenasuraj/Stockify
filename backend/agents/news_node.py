from state.state import State
from langchain.agents import create_react_agent,AgentExecutor
from langchain_core.prompts import PromptTemplate
from llm.llm import llm
from tools.tools import tools
from langchain_core.messages import HumanMessage,AIMessage
import re
from tools.tools import reddit
import pandas as pd





chain = PromptTemplate.from_template("""
You have User's data:{data}.
You have user's question: {query}.                                     
read the data and find relevant information regarding stocks and current market.
Answer precisely with 4-5 lines.                                                                          
""")
def news_node(state:State):
    print("IN NODE-3")
    company_name=state["exhistingName"]
    technical_data = state["technicalData"]    
    query = f"What is the current market and news going on regarding {company_name} stock"
    tavily_data = tools[0].invoke({"query":query})
    llm_response_tavily = chain.invoke({"data":tavily_data,"query":query})
    subreddit = reddit.subreddit('IndianStockMarket')
    data = []
    for post in subreddit.search(company_name, sort='new', limit=10): 
            data.append({
                'Type': 'Post',
                'Post_id': post.id,
                'Title': post.title,
                'Author': post.author.name if post.author else 'Unknown',
                'Timestamp': post.created_utc,
                'Text': post.selftext,
                'Score': post.score,
                'Total_comments': post.num_comments,
                'Post_URL': post.url
            })
            if post.num_comments > 0:
                post.comments.replace_more(limit=5)
                for comment in post.comments.list():
                    data.append({
                        'Type': 'Comment',
                        'Post_id': post.id,
                        'Title': post.title,
                        'Author': comment.author.name if comment.author else 'Unknown',
                        'Timestamp': pd.to_datetime(comment.created_utc, unit='s'),
                        'Text': comment.body,
                        'Score': comment.score,
                        'Total_comments': 0,
                        'Post_URL': None
                    })
    user_query = f"Make a detailed overview regarding the stockprice, current company:{company_name} future and all, all depth data like literally everything."                   
    system_prompt = (
     "You have to go through detailed analysis of a stock condition and provide the detailed overview."
     f"for the company:{company_name} the current values like pe/ratio ,roe etc are:{technical_data}" 
     f"You are allowed to use 2 data i.e 1-Reddit data:{data} and 2-tavily i.e:{llm_response_tavily}"
     f"Combine these data very precisely and answer a very detailed analysis i.e the background of {company_name} and should a person invest or not etc."
     )
    result = llm.invoke([
     {"role": "system", "content": system_prompt},
     {"role": "user", "content": user_query}
     ])        
    return {
        "messages":state["messages"]+[AIMessage(content=result.content)],
        "stockName":state["stockName"],
        "stockType":state["stockType"],
        "technicalData":state["technicalData"],
        "exhistingName":state["exhistingName"]       
           }
