from state.state import State
from langchain.agents import create_react_agent,AgentExecutor
from langchain_core.prompts import PromptTemplate
from llm.llm import llm
from tools.tools import tools
from langchain_core.messages import HumanMessage,AIMessage
import re


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
