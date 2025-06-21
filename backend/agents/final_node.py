from state.state import State
from langchain.agents import create_react_agent,AgentExecutor
from langchain_core.prompts import PromptTemplate
from llm.llm import llm
from tools.tools import tools
from langchain_core.messages import HumanMessage,AIMessage
import re
import json


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
