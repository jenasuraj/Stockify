from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage,AIMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START,END
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
from langchain.agents import create_react_agent,AgentExecutor
from langchain_tavily import TavilySearch
from langchain_core.prompts import PromptTemplate
import re
import yfinance as yf
import praw
import pandas as pd
import json
reddit = praw.Reddit(client_id="YwkiOjMYzWuXo32YTO418g",
                     client_secret="HhNxSCRM4x3_U-6347oXZLhAtIkZ2g",
                     user_agent="stockify")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
class UserData(BaseModel):
    companyname: str
    companytype: str
    companyexchange:str


llm = init_chat_model("meta-llama/llama-4-scout-17b-16e-instruct", model_provider="groq")
tavily = TavilySearch(max_results=3, topic="general")
tools=[tavily]

class State(TypedDict):
    messages: Annotated[list, add_messages]
    stockName:str
    stockType:str
    technicalData:str
    exhistingName:str
    finalRegexChecker:str


template = '''Answer the following questions as best you can. You have access to the following tools:
{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

You are an expert financial assistant specialized in Indian stock markets (BSE and NSE). Your task is to accurately identify the correct stock ticker symbol for Indian companies based on the exchange specified (BSE or NSE).

Instructions:
1. First check if the input contains a company name. If not, immediately return ```Company name absent```
2. For valid requests, analyze the input which will be in formats like "TCS BSE", "RELIANCE NSE", or similar.
3. For stock symbol parsing:
   - For BSE: ```COMPANY_NAME.BO``` (Bombay Stock Exchange)
   - For NSE: ```COMPANY_NAME.NS``` (National Stock Exchange)
4. Follow this process:
   a) First determine if you know the symbol directly (for major companies)
   b) If unsure, use available tools to research
   c) Verify the company name and exchange
   d) If exchange isn't specified, default to NSE
5. Special cases to consider:
   - Some companies have different market names (e.g., "Tata Consultancy Services" → "TCS")
   - Some tickers include numbers (e.g., "SBIN" for State Bank of India)
   - Be precise as similar companies might exist

Important Rules:
- If no company name is detected, return immediately: ```Company name absent```
- For the FINAL ANSWER, provide ONLY the correctly formatted ticker symbol wrapped in triple backticks
- No additional text or explanation in the final answer
- If using tools, extract just the relevant symbol information

Example:
Question: "Hey which company should be better to invest"
Final Answer: ```Company name absent```

Question: "TCS BSE"
Thought: I know TCS is listed on BSE as TCS.BO
Final Answer: ```TCS.BO```

Question: "Reliance Industries NSE"
Thought: I need to verify the exact symbol
Action: tavily
Action Input: "What is the NSE ticker symbol for Reliance Industries?"
Observation: Reliance Industries is listed as RELIANCE on NSE
Final Answer: ```RELIANCE.NS```

Now process this request:

Question: {input}
Thought:{agent_scratchpad}'''
parse_prompt =PromptTemplate.from_template(template) 
parse_agent = create_react_agent(llm=llm,tools=tools,prompt=parse_prompt)
parse_agent_executer = AgentExecutor(agent=parse_agent,tools=tools)


def stock_parsing_node(state:State):
    print("IN NODE-1")
    exhisting_name =state["stockName"] 
    job = "Search the official indian stock name of "+state["stockName"]
    stockType = state["stockType"]
    result = parse_agent_executer.invoke({"input":job})
    parsing_data = result['output']
    parsed_data = re.findall(r"```([\s\S]*?)```", parsing_data)
    print("parsed company name is -->",parsed_data)
    return {
        "messages":state["messages"]+[AIMessage(content=f"The parsed company name is {parsed_data}")],
        "stockName":parsed_data,
        "stockType":stockType, 
        "exhistingName":exhisting_name      
           }



def technical_node(state:State):
    print("IN NODE-2")
    company_name = state["stockName"][0] 
    company = yf.Ticker(company_name)
    pe_ratio = company.info.get("trailingPE")
    roe =  company.info.get("returnOnEquity")
    eps =  company.info.get("trailingEps")
    market_cap = company.info.get("marketCap")
    technical_data = f"the technical data of {company_name} is PE_RATIO:{pe_ratio},ROE:{roe},EPS:{eps},MARKET_CAP:{market_cap}"
    return {
        "messages":state["messages"]+[AIMessage(content=technical_data )],
        "stockName":company_name,
        "stockType":state["stockType"],
        "technicalData":technical_data,
        "exhistingName":state["exhistingName"]
        }

 

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
    tavily_data = tavily.invoke({"query":query})
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



parsing_template = """
You are a JSON extraction agent.

You will receive detailed stock information as plain text, including technical data (PE ratio, ROE, EPS, Market Cap), news summaries (from Reddit and other sources), and a final analysis about whether to invest.

Your task is to **extract this unstructured information** and return it as a structured JSON object in this format (pay attention to proper JSON syntax):

Wrap your entire response between triple backticks (```) for safety.

Example format:
{{
"technical_data": {{
"PE_RATIO": "...",
"ROE": "...",
"EPS": "...",
"MARKET_CAPITAL": "..."
}},
"news": {{
"news_data": "..."
}},
"conclusion": "..."
}}

Instructions:
- Carefully extract PE ratio, ROE, EPS, and Market Capital from the technical section.
- Summarize the news and social commentary (4-5 lines max) in plain paragraph text.
- In the conclusion, clearly say whether to invest or not and why — based on both technicals and news.

Now extract from the following:
{parsing_data}
"""

fp_prompt=PromptTemplate.from_template(parsing_template)
final_parsing_chain = fp_prompt | llm
def final_node(state: State):
    print("IN NODE-4")
    final_parse_data = state["messages"][-1].content
    final_parsed_data = final_parsing_chain.invoke({"parsing_data": final_parse_data})

    matches = re.findall(r"```(?:json)?\s*(.*?)```", final_parsed_data.content, re.DOTALL)
    error_message = "Failed to extract json data from backtics."
    if not matches:
        return {
             "finalRegexChecker":error_message,
             "messages":state["messages"]
               }
    try:
        finalData = json.loads(matches[0])

    except json.JSONDecodeError as e:
        return {
            "messages": state["messages"] + [AIMessage(content=f"JSON decode error: {str(e)}\nRaw content: {matches[0]}")],
        }
    return {
        "messages": state["messages"] + [AIMessage(content=json.dumps(finalData, indent=2))],  # 🔥 Fix: convert dict to string
        "finalRegexChecker":"all good"
    }


def routing(state:State):
    print("IN ROUTING NODE TO CHECK DEEP/NORMAL RESEARCH")
    typeOfStock = state["stockType"]
    if typeOfStock.lower() == 'deep research':
        return "useParse"
    else:
        return "end"
    
def routingparse(state:State):
    print("IN PARSE ROUTING NODE ")
    companyNameOrnot = state["stockName"]
    check = ''.join(companyNameOrnot)
    if check.lower() == 'company name absent' or 'company name absent'  in check.lower():
        return "end"
    else:
        return "go"

def defaultEnd_node(state:State):
    return{
        "messages":state["messages"]+[AIMessage(content="No any company name is present ! better provide a company name !")]
          }
       
def checkJsonResponse(state:State):
    response = state["finalRegexChecker"]
    print("DOUBT",type(response))
    if 'failed to extract' in response.lower():
        return "loop"
    else:
        return "finish"
    

graph_builder = StateGraph(State)
graph_builder.add_node("stockParsingNode",stock_parsing_node)
graph_builder.add_node("defaultEndNode",defaultEnd_node)
graph_builder.add_node("technicalNode",technical_node)
graph_builder.add_node("newsNode",news_node)
graph_builder.add_node("finalNode",final_node)

graph_builder.add_edge(START,"stockParsingNode")
graph_builder.add_conditional_edges("stockParsingNode",routingparse,{"end":"defaultEndNode","go":"technicalNode"})
graph_builder.add_edge("defaultEndNode",END)
graph_builder.add_edge("technicalNode","newsNode")
graph_builder.add_conditional_edges("newsNode",routing,{"useParse":"finalNode","end":END})
graph_builder.add_conditional_edges("finalNode",checkJsonResponse,{"loop":"finalNode","finish":END}) 
graph = graph_builder.compile()



@app.post("/")
async def read_root(data: UserData):
    print("Data received !:", data.companyname)
    print("data received !:",data.companytype)
    print("data received !:",data.companyexchange)
    company_name = data.companyname+" "+data.companyexchange
    initial_state = {
        "messages":[HumanMessage(content=f'Give me stock data about {data.companyname} registered at {data.companyexchange} of type {data.companytype}')],
        "stockName":company_name,
        "stockType":data.companytype
                    }
    result = graph.invoke(initial_state)
    print("final output-->",result["messages"][-1].content)
    return {"message": result["messages"][-1].content}
