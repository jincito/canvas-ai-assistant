# Canvas AI Assistant - Quick Start Guide

Get up and running with the Canvas AI Assistant MCP Server in 5 minutes!

## Prerequisites

- Python 3.8+
- Claude Desktop (or another MCP-compatible client)

## Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/your-username/canvas-ai-assistant.git
   cd canvas-ai-assistant
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Test the installation:**
   ```bash
   python3 test_mock_client.py
   ```
   
   You should see all tests pass with green checkmarks ✓

## Configure Claude Desktop

1. **Find your config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add this configuration** (replace the path with your actual project path):
   ```json
   {
     "mcpServers": {
       "canvas-ai-assistant": {
         "command": "python3",
         "args": [
           "/absolute/path/to/canvas-ai-assistant/run_mcp_server.py"
         ],
         "env": {
           "USE_MOCK_CANVAS": "true"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Try It Out!

Ask Claude these questions (use login: `alex@example.edu`):

1. "What courses am I enrolled in?"
2. "What assignments are due in the next week?"
3. "Do I have any missing assignments?"
4. "What are my current grades?"
5. "Show me recent announcements"

## Mock Student Logins

- `alex@example.edu` - 3 courses, various assignments
- `jordan@example.edu` - 2 courses

## What's Next?

- Read the full [MCP Server Guide](docs/mcp-server-guide.md)
- Explore the [mock data](mock_data/canvas_data.json)
- Check out the [architecture docs](docs/architecture.md)

## Troubleshooting

**Server not connecting?**
- Verify the absolute path in your config is correct
- Check that `python3` is in your PATH
- Look for errors in Claude Desktop's developer console

**"Student not found"?**
- Use `alex@example.edu` or `jordan@example.edu`
- Make sure the mock data file exists

**Need help?**
- Run `python3 test_mock_client.py` to verify setup
- Check the [MCP Server Guide](docs/mcp-server-guide.md)
- Review the main [README](README.md)
