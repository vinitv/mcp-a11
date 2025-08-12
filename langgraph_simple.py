#!/usr/bin/env python3
"""
Simple LangGraph Application for Repair Cost Assistant
A working LangGraph demo that shows the concepts without complex MCP integration
"""

import asyncio
import subprocess
import json
from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END

# Define the state structure
class RepairState(TypedDict):
    messages: List[Dict[str, str]]
    user_query: str
    repair_info: Dict[str, Any]
    current_step: str

# Simple tool functions that call MCP tools via subprocess
async def call_mcp_tool(tool_name: str, **kwargs) -> str:
    """Call MCP tool using subprocess approach"""
    try:
        # Create a simple Python script to call the MCP tool
        script = f"""
import asyncio
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.getcwd())

# Load environment variables
load_dotenv()

# Import the tool function directly from server.py
from server import {tool_name}

async def main():
    try:
        # Debug: Check API key availability for repair_cost
        if "{tool_name}" == "repair_cost":
            api_key = os.getenv("REPAIR_API_KEY")
            print(f"DEBUG: API key available: {{bool(api_key)}}", file=sys.stderr)
        
        result = {tool_name}({', '.join(f'"{v}"' if isinstance(v, str) else str(v) for v in kwargs.values())})
        print(result)
    except Exception as e:
        print(f"Error: {{e}}")
        import traceback
        print(f"Traceback: {{traceback.format_exc()}}", file=sys.stderr)

asyncio.run(main())
"""
        
        # Write the script to a temporary file and run it
        with open("temp_call.py", "w") as f:
            f.write(script)
        
        # Run the script
        result = subprocess.run(
            ["uv", "run", "python", "temp_call.py"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        # Clean up
        import os
        if os.path.exists("temp_call.py"):
            os.remove("temp_call.py")
        
        if result.returncode == 0:
            # Include debug info if available
            debug_info = ""
            if result.stderr:
                debug_info = f" (Debug: {result.stderr.strip()})"
            return result.stdout.strip() + debug_info
        else:
            return f"Error: {result.stderr}"
            
    except Exception as e:
        return f"Error calling tool: {str(e)}"

# Tool functions for LangGraph
async def get_repair_cost(state: RepairState) -> RepairState:
    """Get repair cost using MCP tool"""
    try:
        user_query = state["user_query"].lower()
        
        # Simple parsing
        repair_types = ["electrical_panel_replacement", "hvac_installation", "hvac_repair", 
                       "air_conditioning_repair", "furnace_replacement", "roof_leak_repair"]
        
        found_repair = None
        for repair in repair_types:
            if repair.replace("_", " ") in user_query:
                found_repair = repair
                break
        
        # Extract zip code
        import re
        zip_match = re.search(r'\b\d{5}\b', user_query)
        zip_code = zip_match.group() if zip_match else "90210"
        
        if found_repair:
            # Call MCP tool
            result = await call_mcp_tool("repair_cost", repair_type=found_repair, zip_code=zip_code)
            
            state["repair_info"] = {
                "repair_type": found_repair,
                "zip_code": zip_code,
                "cost_estimate": result
            }
            
            state["messages"].append({
                "role": "assistant",
                "content": f"[Tool: repair_cost] Here's the cost estimate for {found_repair.replace('_', ' ')} in {zip_code}:\n{result}"
            })
        else:
            state["messages"].append({
                "role": "assistant",
                "content": "[Tool: repair_cost] Please specify a repair type (like 'electrical panel replacement') and a zip code."
            })
    
    except Exception as e:
        state["messages"].append({
            "role": "assistant",
            "content": f"[Tool: repair_cost] Sorry, I encountered an error: {str(e)}"
        })
    
    return state

async def search_repair_info(state: RepairState) -> RepairState:
    """Search for repair information using web search"""
    try:
        search_query = f"home repair costs {state['user_query']}"
        result = await call_mcp_tool("web_search", query=search_query)
        
        state["messages"].append({
            "role": "assistant",
            "content": f"[Tool: web_search] Here's information about {state['user_query']}:\n{result[:200]}..."
        })
    
    except Exception as e:
        state["messages"].append({
            "role": "assistant",
            "content": f"[Tool: web_search] Sorry, I encountered an error: {str(e)}"
        })
    
    return state

async def roll_dice_for_fun(state: RepairState) -> RepairState:
    """Roll dice for fun"""
    try:
        result = await call_mcp_tool("roll_dice", notation="2d6", num_rolls=1)
        
        state["messages"].append({
            "role": "assistant",
            "content": f"[Tool: roll_dice] 🎲 Just for fun, I rolled some dice: {result}"
        })
    
    except Exception as e:
        state["messages"].append({
            "role": "assistant",
            "content": f"[Tool: roll_dice] Sorry, I encountered an error: {str(e)}"
        })
    
    return state

# Router function
def route_to_tool(state: RepairState) -> str:
    """Route to appropriate tool based on user input"""
    query = state["user_query"].lower()
    
    # Check for repair cost requests
    repair_keywords = ["cost", "price", "estimate", "how much", "repair", "replacement", "installation"]
    if any(keyword in query for keyword in repair_keywords):
        return "get_repair_cost"
    
    # Check for information requests
    info_keywords = ["what is", "tell me about", "information", "search", "find"]
    if any(keyword in query for keyword in info_keywords):
        return "search_repair_info"
    
    # Default to dice rolling
    return "roll_dice_for_fun"

# Create the LangGraph workflow
def create_repair_assistant():
    """Create the repair assistant workflow"""
    
    # Create the graph
    workflow = StateGraph(RepairState)
    
    # Add nodes
    workflow.add_node("get_repair_cost", get_repair_cost)
    workflow.add_node("search_repair_info", search_repair_info)
    workflow.add_node("roll_dice_for_fun", roll_dice_for_fun)
    
    # Set the entry point
    workflow.set_entry_point("get_repair_cost")
    
    # Add edges to end
    workflow.add_edge("get_repair_cost", END)
    workflow.add_edge("search_repair_info", END)
    workflow.add_edge("roll_dice_for_fun", END)
    
    return workflow.compile()

# Main application
async def main():
    """Main application loop"""
    print("🔧 Welcome to the LangGraph Repair Cost Assistant!")
    print("I can help you with:")
    print("- Repair cost estimates")
    print("- General repair information")
    print("- And even roll some dice for fun!")
    print("Type 'quit' to exit.\n")
    
    # Create the workflow
    app = create_repair_assistant()
    
    # Initialize state
    state = RepairState(
        messages=[],
        user_query="",
        repair_info={},
        current_step="start"
    )
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Thanks for using the Repair Cost Assistant! 👋")
                break
            
            # Update state
            state["user_query"] = user_input
            state["messages"].append({
                "role": "user",
                "content": user_input
            })
            
            # Run the workflow
            print("🤔 Processing your request...")
            
            # Determine which tool to use
            tool_choice = route_to_tool(state)
            print(f"🔧 Using tool: {tool_choice}")
            
            # Execute the appropriate tool
            if tool_choice == "get_repair_cost":
                result = await get_repair_cost(state)
            elif tool_choice == "search_repair_info":
                result = await search_repair_info(state)
            else:
                result = await roll_dice_for_fun(state)
            
            # Display the response
            if result["messages"]:
                last_message = result["messages"][-1]
                if last_message["role"] == "assistant":
                    print(f"Assistant: {last_message['content']}")
            
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print("\nThanks for using the Repair Cost Assistant! 👋")
            break
        except Exception as e:
            print(f"Sorry, I encountered an error: {e}")
            print("Please try again.\n")

if __name__ == "__main__":
    asyncio.run(main())