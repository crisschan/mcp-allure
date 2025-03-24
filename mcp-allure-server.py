import asyncio
from mcp.server.fastmcp import FastMCP
from allure_html import AllureSuiteParser

MCP_SERVER_NAME = "mcp-allure-server"
mcp=FastMCP(MCP_SERVER_NAME)
# mcp.start()

@mcp.tool()
async def get_allure_report(results_dir: str) -> str:
    """
    read allure report and return json data
    """
    try:
        parser = AllureSuiteParser(results_dir)
        return parser.parse()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    mcp.run(transport='stdio')