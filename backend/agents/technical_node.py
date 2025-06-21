from state.state import State
from tools.tools import tools
from langchain_core.messages import AIMessage
import yfinance as yf

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

