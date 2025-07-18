import json

from mcp.server.fastmcp import FastMCP
from api.ridb import find_camping_near_city

mcp = FastMCP()

@mcp.tool("find_campgrounds")
def find_campgrounds(location_name: str, radius: int = 25, limit: int = 50 ):
    """Find camping facilities near a specified location.

    Searches for camping facilities within a customizable radius of a city using the
    Recreation Information Database (RIDB) API. First geocodes the city to get coordinates,
    then searches for campgrounds and camping facilities in the surrounding area.

    Returns a JSON string containing facility information including any available image URLs.
     """

    camping_data = find_camping_near_city(location_name, radius=25, limit=10)
    return json.dumps(camping_data, indent=4)


if __name__ == "__main__":
    mcp.run()