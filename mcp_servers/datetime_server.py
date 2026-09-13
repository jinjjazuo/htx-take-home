"""Local MCP server with one datetime tool: normalise a written date to ISO 8601 (YYYY-MM-DD)."""
from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("datetime")

# Unambiguous written-out formats only. Numeric forms like 03/04/2024 are left out on purpose:
# day-first vs month-first can't be told apart, and a silent wrong guess is worse than an error.
FORMATS = ["%d %B %Y", "%d %b %Y", "%B %d, %Y", "%b %d, %Y", "%B %d %Y", "%Y-%m-%d"]


@mcp.tool()
def normalize_date(text: str) -> str:
    """Convert ONE calendar date written in text (e.g. '16 February 2024') to ISO format YYYY-MM-DD.

    Pass only the date itself - not the surrounding sentence, and not a date range.
    """
    cleaned = " ".join(text.split()).strip(" .,;:")
    for fmt in FORMATS:
        try:
            return datetime.strptime(cleaned, fmt).date().isoformat()
        except ValueError:
            pass
    raise ValueError(f"Could not read {text!r} as a single date. Pass just one date, e.g. '16 February 2024'.")


if __name__ == "__main__":
    mcp.run(transport="stdio")
