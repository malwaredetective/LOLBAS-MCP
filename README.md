# LOLBAS-MCP
![python](https://img.shields.io/badge/python-3.11%2B-blue)
![MCP Server](https://img.shields.io/badge/MCP-Server-blueviolet)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A Model Context Protocol (MCP) server that acts as a bridge between Large Language Models (LLMs) and the [LOLBAS Project API](https://lolbas-project.github.io/), allowing automated queries for living-off-the-land binaries and scripts.  

> This MCP Server is configured to run locally via STDIO.

## Quickstart Guide

### 1. Clone the Repository

```bash
git clone https://github.com/malwaredetective/LOLBAS-MCP.git
cd LOLBAS-MCP
```

### 2. Set Up a Python Virtual Environment

```bash
python3 -m venv venv

# Run this command to activate your Python Virtual Environment within Linux/macOS
source venv/bin/activate

# Run this command to activate your Python Virtual Environment within Windows
venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the MCP Server within your preferred MCP Client

- Install your preferred MCP Client.
- Depending on your MCP Client, the steps to configure the [LOLBAS-MCP](lolbas-mcp-server.py) server may differ. A standard configuration is listed within this projects [mcp.json](mcp.json) file.

> Note: When executing the MCP server from within a Python Virtual Environment, the startup command may differ depending on your Operating System.

## MCP Tools

### list_binaries
Return a list of all binaries/scripts found within the LOLBAS project.

```json
{
  "type": "object",
  "properties": {}
}
```

### list_categories
Return a list of all unique operational categories within LOLBAS, for example: Download, Execute, Tamper. These categories represent the main techniques or use cases associated with living-off-the-land binaries and scripts.

```json
{
  "type": "object",
  "properties": {}
}
```

### query_file
Query LOLBAS for a specific binary/script by name.

```json
{
  "type": "object",
  "properties": {
    "file_name": {
      "description": "The name of the file to query, for example: 'certutil.exe', 'mshta.exe', etc.",
      "type": "string"
    }
  },
  "required": [
    "file_name"
  ]
}
```

### query_category
Query LOLBAS for all binaries/scripts that include at least one command in a given category, for example: Download, Execute, Copy.

```json
{
  "type": "object",
  "properties": {
    "category": {
      "description": "The category of commands to search for, for example: 'Download', 'Execute', etc.",
      "type": "string"
    }
  },
  "required": [
    "category"
  ]
}
```

### refresh_cache
Refresh your local cache with the latest updates from the LOLBAS project.

```json
{
  "type": "object",
  "properties": {}
}
```

## License

This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software in accordance with the MIT License terms.