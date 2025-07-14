from mcp.server.fastmcp import FastMCP

# initialize MCP and give servername name 
mcp=FastMCP('math')

@mcp.tool()
def add(a:int,b:int)->int:
    """ 
    Add two numbers 
    """
    return a+b 

@mcp.tool()
def multiply(a:float,b:float)->float:
    """ 
    multiply two numbers 
    """
    return a*b 

@mcp.tool()
def divide(a:float,b:float)->float:
    """ 
    dicide two numbers 
    """
    return a/b 

@mcp.tool()
def subtract(a:int,b:int)->int:
    """ 
    subtract two numbers 
    """
    return a-b 

# the transport='studio' argument tells the server to:
# Use standard input/output (stdin and stdout) to receive and respond to tool function calls 
# try to use server locally 
if __name__=="__main__":
    mcp.run(transport='stdio')