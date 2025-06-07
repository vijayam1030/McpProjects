# Import type hints for better code documentation
from typing import Any
# Import httpx for making async HTTP requests
import httpx
# Import FastMCP server framework
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server with "weather" as the service name
mcp = FastMCP("weather")

# Base URL for the National Weather Service API
NWS_API_BASE = "https://api.weather.gov"
# User agent string for API requests
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    # Set required headers for NWS API requests
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    # Create an async HTTP client context
    async with httpx.AsyncClient() as client:
        try:
            # Make GET request with timeout and headers
            response = await client.get(url, headers=headers, timeout=30.0)
            # Raise exception for bad status codes
            response.raise_for_status()
            # Return JSON response data
            return response.json()
        except Exception:
            # Return None if any error occurs
            return None
        
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    # Extract properties from the feature
    props = feature["properties"]
    # Return formatted string with alert details
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    # Construct API URL for the specified state
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    # Fetch alert data from NWS API
    data = await make_nws_request(url)

    # Handle case where data couldn't be fetched or is invalid
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    # Handle case where no alerts are active
    if not data["features"]:
        return "No active alerts for this state."

    # Format each alert and join them with separators
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    # Return the message with a prefix
    return f"Resource echo: {message}"