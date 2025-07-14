from mcp.server.fastmcp import FastMCP
from langchain_community.tools.tavily_search import TavilySearchResults
import os 
from dotenv import load_dotenv
# from tavily import TavilyCl

load_dotenv()

mcp=FastMCP('Tavily')

@mcp.tool()
def search_tavily(query:str)->str:
    """ 
    search the web using Tavility API and return summzarizer results
    """
    try:
        tool = TavilySearchResults(k=1)
        results = tool.run(query)
        # print(results)
        return str(results)
    except Exception as e:
        return f"Search failed due to: {str(e)}"

if __name__=="__main__":
    mcp.run(transport='stdio')