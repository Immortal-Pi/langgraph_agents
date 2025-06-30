from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
load_dotenv()

import asyncio


async def main():
    client=MultiServerMCPClient(
        {
            'math':{
                'command':'python',
                'args':['MCP_demp/mathserver.py'], ##Ensure correct absolute path 
                'transport':'stdio',
            },
            'weather':{
                'url':'http://127.0.0.1:8000/mcp',
                'transport':'streamable_http'
            },
            'tavily':{
                'command':'python',
                'args':['MCP_demp/tavily.py'], ##Ensure correct absolute path 
                'transport':'stdio',
            }

        }
    )

    import os 
    # os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
    # os.environ['AZURE_OPENAI_GPT_4O_API_KEY']=os.getenv('AZURE_OPENAI_GPT_4O_API_KEY')

    tools=await client.get_tools()
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
        {'messages':[{'role':'user','content':'whats the latest AI news on helthcare?'}]}
    )
    print('Math response:',math_response['messages'][-1].content)

asyncio.run(main())