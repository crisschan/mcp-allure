# MCP-Allure

MCP-Allure is a MCP server that reads Allure reports and returns them in LLM-friendly formats.

# Motivation

As AI and Large Language Models (LLMs) become increasingly integral to software development, there is a growing need to bridge the gap between traditional test reporting and AI-assisted analysis. Traditional Allure test report formats, while human-readable, aren't optimized for LLM consumption and processing.

MCP-Allure addresses this challenge by transforming Allure test reports into LLM-friendly formats. This transformation enables AI models to better understand, analyze, and provide insights about test results, making it easier to:

- Generate meaningful test summaries and insights
- Identify patterns in test failures
- Suggest potential fixes for failing tests
- Enable more effective AI-assisted debugging
- Facilitate automated test documentation generation

By optimizing test reports for LLM consumption, MCP-Allure helps development teams leverage the full potential of AI tools in their testing workflow, leading to more efficient and intelligent test analysis and maintenance.

# Problems Solved
- **Efficiency**: Traditional test reporting formats are not optimized for AI consumption, leading to inefficiencies in test analysis and maintenance.
- **Accuracy**: AI models may struggle with interpreting and analyzing test reports that are not in a format optimized for AI consumption.
- **Cost**: Converting test reports to LLM-friendly formats can be time-consuming and expensive.

# Key Features
- **Conversion**: Converts Allure test reports into LLM-friendly formats.
- **Optimization**: Optimizes test reports for AI consumption.
- **Efficiency**: Converts test reports efficiently.
- **Cost**: Converts test reports at a low cost.
- **Accuracy**: Converts test reports with high accuracy.

# Installation 

To install mcp-repo2llm using uv:
```
{
  "mcpServers": {
    "mcp-allure-server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/Users/crisschan/workspace/pyspace/mcp-allure/mcp-allure-server.py"
      ]
    }
  }
}
```
# Tool
##  get_allure_report

- Reads Allure report and returns JSON data
- Input:
  - report_dir: Allure HTML report path
- Return:
  - String, formatted JSON data, like this:
```
{
    "test-suites": [
        {
            "name": "test suite name",
            "title": "suite title",
            "description": "suite description",
            "status": "passed",
            "start": "timestamp",
            "stop": "timestamp",
            "test-cases": [
                {
                    "name": "test case name",
                    "title": "case title",
                    "description": "case description",
                    "severity": "normal",
                    "status": "passed",
                    "start": "timestamp",
                    "stop": "timestamp",
                    "labels": [

                    ],
                    "parameters": [

                    ],
                    "steps": [
                        {
                            "name": "step name",
                            "title": "step title",
                            "status": "passed",
                            "start": "timestamp",
                            "stop": "timestamp",
                            "attachments": [

                            ],
                            "steps": [

                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

```
