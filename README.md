# Rec-MCP: Recreation & Campground Search

A Model Context Protocol (MCP) server that provides tools for finding camping facilities and recreational areas using Recreation.gov's Recreation Information Database (RIDB) API and Google Maps Geocoding API.

## Features

- 🏕️ **Find Camping Facilities**: Search for campgrounds and recreational facilities near any location
- 🌍 **Geocoding Support**: Convert city names to coordinates using Google Maps API
- 🔍 **Flexible Search**: Customize search radius, result limits, and activity types. Change your prompts to locate reservable vs. first-come, first-serve campgrounds, etc.
- 📊 **Rich Data**: Get detailed facility information including contact details, amenities, and image URLs
- 🛠️ **MCP Integration**: Works seamlessly with MCP clients


### Prerequisites

- Python 3.12 or higher
- API keys for:
  - [Recreation.gov API](https://ridb.recreation.gov/) (RIDB)
  - [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/start)

### Setup

1. Clone the repository
2. Install dependencies
  - `uv add requests python-dotenv mcp`
3. Create a `.env` file in the project root:
   - env RIDB_API_KEY=your_recreation_gov_api_key_here 
   - GOOGLE_GEOCODE_KEY=your_google_maps_api_key_here
4. Run the server
   - `uv --directory /your_file_path/rec_mcp/ run ridb_mcp_server.py`

### Testing the MCP Server
Use the MCP Inspector to ensure the MCP Server is working before integrating it into any clients. 

Install MCP inspector globally
`npm install -g @modelcontextprotocol/inspector`

Run the inspector
`mcp-inspector uv run python ridb_mcp_server.py`

### Integrating the MCP Server with Clients
The MCP Server can be integrated into clients such as Claude Desktop and VSCode.

For Claude Desktop, add the server to the claude_desktop_config.json file.

### Credits

JetBrains AI Pro generated 90 % of the code written for this project in PyCharm.


