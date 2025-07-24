import asyncio
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq

from mcp_use import MCPAgent, MCPClient
import os 
import dotenv

dotenv.load_dotenv()

async def run_memeory_chat():
    """ 
    Run a chat using MCPAgent's built-in conversation memeory"""
    # initialize LLM with API keys 
    llm_open_ai=AzureChatOpenAI(
        azure_deployment='gpt-4o',
        api_key=os.getenv('AZURE_OPENAI_GPT_4O_API_KEY'),
        azure_endpoint=os.getenv('AZURE_OPENAI_GPT_4O_API_ENDPOINT'),
        api_version=os.getenv('AZURE_OPENAI_GPT_4O_API_VERSION')
        )

    llm_groq=ChatGroq(model='deepseek-r1-distill-llama-70b',api_key=os.getenv('GROQ_API'))

    # Config file path - change this to your config file 
    config_file='server/weather.json'

    # Create MCP client and agent with memeory enabled 
    client=MCPClient.from_config_file(config_file)
    
    # create agent with memory_enabled=True
    agent=MCPAgent(
        llm=llm_open_ai,
        client=client,
        max_steps=15,
        memory_enabled=True
    )

    print('\n===== Interactive MCP Chat =====')
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear converation history")

    try:
        # Main chat loop 
        while True:
            # Get user input 
            user_input=input('\n You: ')
        
            # Check for xit command 
            if user_input.lower() in ['exit','quit']:
                print('Ending conversation....')
                break 

            # check for clear history command 
            if user_input.lower()=='clear':
                print('Conversation history cleared.')
                continue
                
            # Get response from agent 
            print('\n Assistant: ',end='',flush=True)
            try:
                # Run the agent with user input (memory handling is automatic)
                response=await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f'\nError {e}')
    finally:
        # clean up
        if client and client.sessions:
            await client.close_all_sessions()
    
if __name__=="__main__":
    asyncio.run(run_memeory_chat())
             