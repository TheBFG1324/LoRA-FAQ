from mcp.server.fastmcp import FastMCP
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))  
from serve.loader import answer as local_answer

mcp = FastMCP("lora_faq_hamilton")

@mcp.tool()
def answer_faq(question: str) -> str:
    """Return a Hamilton quote related to the topic."""
    return local_answer(question)

if __name__ == "__main__":
    mcp.run(transport="stdio")
