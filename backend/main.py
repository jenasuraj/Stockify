from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage,AIMessage
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph, START,END
from fastapi.middleware.cors import CORSMiddleware
from state.state import State
from agents.final_node import final_node 
from agents.parse_node import stock_parsing_node
from agents.news_node import news_node
from agents.technical_node import technical_node


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
    #print("DOUBT",type(response))
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
