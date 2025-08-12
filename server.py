from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
import requests
import json
from dice_roller import DiceRoller

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

# Repair Cost API configuration
REPAIR_API_BASE_URL = os.getenv("REPAIR_API_BASE_URL")
REPAIR_API_KEY = os.getenv("REPAIR_API_KEY")


@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

@mcp.tool()
def repair_cost(repair_type: str, zip_code: str) -> str:
    """Get repair cost estimate for home repairs"""
    try:
        url = f"{REPAIR_API_BASE_URL}/api/v1/repair-cost/{repair_type}"
        headers = {"x-api-key": REPAIR_API_KEY}
        params = {"zip_code": zip_code, "scope": "average"}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        cost = data["cost_estimate"]
        return f"${cost['low']:,} - ${cost['high']:,} (avg: ${cost['average']:,}) for {repair_type.replace('_', ' ')} in {zip_code}"
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")