from langchain_tavily import TavilySearch
from mcp.server.fastmcp import FastMCP
import sys

# Initialize the server name 
mcp=FastMCP('Tavily')
import os 
import dotenv
dotenv.load_dotenv()


@mcp.tool()
def tavily_search(question:str)->str:
    """Use Tavily to search the web for a query."""
    tool=TavilySearch(api_key=os.getenv('TAVILY_API_KEY'),max_results=2)
    response=tool.invoke(question)
    print('tavily_search:',response,file=sys.stderr)
    return response

if __name__=='__main__':
    mcp.run(transport='stdio') 