from langchain_tavily import TavilySearch
from mcp.server.fastmcp import FastMCP
import sys

# Initialize the server name 
mcp=FastMCP('Tavily')
import os 
import dotenv
dotenv.load_dotenv()


# @mcp.tool()
# def tavily_search(question:str)->str:
#     """Use Tavily to search the web for a query."""
#     tool=TavilySearch(api_key=os.getenv('TAVILY_API_KEY'),max_results=2)
#     response=tool.invoke(question)
#     print('tavily_search:',response,file=sys.stderr)
#     return response

# if __name__=='__main__':
#     mcp.run(transport='stdio') 
@mcp.tool()
def search_web(query: str) -> str:
    try:
        with open("tavily_log.txt", "a") as f:
            f.write(f"Query received: {query}\n")

        tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"), max_results=2)
        response = tool.invoke(query)

        with open("tavily_log.txt", "a") as f:
            f.write(f"Response: {response}\n")

        return response

    except Exception as e:
        with open("tavily_log.txt", "a") as f:
            f.write(f"Error: {str(e)}\n")
        return "Tavily failed to retrieve the search result."

if __name__ == "__main__":
    mcp.run(transport="streamable-http",port=8010)
