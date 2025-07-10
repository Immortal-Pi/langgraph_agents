from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START 
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode 
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langgraph.prebuilt import tools_condition
import os  
from dotenv import load_dotenv 
load_dotenv()


os.environ['LANGSMITH_API_KEY']=os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING']='true'
os.environ['LANGSMITH_PROJECT']='TestProject'
# setup azure open 
llm_open_ai=AzureChatOpenAI(
        azure_deployment='gpt-4o',
        api_key=os.getenv('AZURE_OPENAI_GPT_4O_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_GPT_4O_API_ENDPOINT'),
        api_version=os.getenv('AZURE_OPENAI_GPT_4O_API_VERSION')
    )

class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def make_tool_graph():
    # Graph with tool call 
    @tool
    def add(a:float,b:float):
        """ 
        add two numbers 
        """
        return a+b 

    tools=[add]
    tool_node=ToolNode([add])
    llm_with_tools=llm_open_ai.bind_tools([add])
    
    def call_llm_model(state:State):
        return {'messages':[llm_with_tools.invoke(state['messages'])]}

    # Graph 
    builder=StateGraph(State)
    builder.add_node('tool_calling_llm',call_llm_model)
    builder.add_node('tools',tool_node)

    # add edges 
    builder.add_edge(START,'tool_calling_llm')
    builder.add_conditional_edges('tool_calling_llm',tools_condition)
    builder.add_edge('tools','tool_calling_llm')
    # builder.add_edge('tools',END)

    # compile the graph

    graph=builder.compile()
    return graph

tool_agent=make_tool_graph()
