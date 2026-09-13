"""Exploration-only MCP server: one tool, so the transports can be compared on something real."""
import sys
from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("probe")


@mcp.tool()
def parse_to_iso(text: str, fmt: str) -> str:
    """Parse `text` with the strptime format `fmt` and return the date as YYYY-MM-DD."""
    return datetime.strptime(text, fmt).date().isoformat()


if __name__ == "__main__":
    # `python probe_server.py` -> stdio.  `python probe_server.py http 8123` -> Streamable HTTP on localhost:8123
    if sys.argv[1:2] == ["http"]:
        mcp.settings.port = int(sys.argv[2])
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")
