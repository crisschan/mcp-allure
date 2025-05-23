# Generated by https://smithery.ai. See: https://smithery.ai/docs/build/project-config
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN pip install --no-cache-dir mcp[cli]>=1.5.0

# Copy application source
COPY . .

# Default command to start MCP server
CMD ["python", "mcp-allure-server.py"]
