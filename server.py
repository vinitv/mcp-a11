from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os

load_dotenv()

mcp = FastMCP("websearch-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

if __name__ == "__main__":
    mcp.run(transport="stdio")