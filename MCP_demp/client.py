from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
# from langchain_core.messages
import os 
from dotenv import load_dotenv
load_dotenv()

import asyncio

os.environ['LANGSMITH_API_KEY']=os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING']='true'
os.environ['LANGSMITH_PROJECT']='TestProject'
async def main():
    client=MultiServerMCPClient(
        {
            'math':{
                'command':'python',
                'args':['mathserver.py'], # ensure correct absulute path
                "transport":'stdio',
            },
            'weather': {
                'command':'python',
                'args':['weather.py'], # ensure correct absulute path
                "transport":'stdio',
            },
             "Tavily": {
            "command": "python",
            "args": ["tavily.py"],
            "transport": "stdio"
            }       


        }
    )

    tools=await client.get_tools()
    # for tool in tools:
    #     print(tool)
    llm_open_ai=AzureChatOpenAI(
         azure_deployment='gpt-4o',
    api_key=os.getenv('AZURE_OPENAI_GPT_4O_API_KEY'),
    azure_endpoint=os.getenv('AZURE_OPENAI_GPT_4O_API_ENDPOINT'),
    api_version=os.getenv('AZURE_OPENAI_GPT_4O_API_VERSION')
    )
    agent=create_react_agent(
        llm_open_ai,tools
    )
    math_response=await agent.ainvoke(
        {'messages':[{'role':'user','content':'what is latest news on AI? what is the stock price of NVIDIA?'}]},
         config={"return_intermediate_steps": True}
    )
    print(math_response['messages'][-1].content)

asyncio.run(main())