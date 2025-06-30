from mcp.server.fastmcp import FastMCP

# Initialize the server name 
mcp=FastMCP('Math')

@mcp.tool()
def add(a:int,b:int)->int:
    """ 
    Add two numbers 
    """
    return a+b 

@mcp.tool()
def multiply(a:int,b:int)->int:
    """
    multiply two numbers 
    """
    return a*b

@mcp.tool()
def divide(a:int,b:int)-> int:
    """ 
    divide two numbers
    """
    return a/b 

@mcp.tool()
def subtract(a:int,b:int)->int:
    """ 
    subtract two numbers
    """
    return a-b 

# transport='stdio' argument tells the server to: 
# Use standard input/output (stdin and stdout) to receive and respond to tool function calls
if __name__=='__main__':
    mcp.run(transport='stdio') 
