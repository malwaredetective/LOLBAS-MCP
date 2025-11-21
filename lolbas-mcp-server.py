from fastmcp import FastMCP
from typing import Annotated
import requests
import logging

logging.basicConfig(level=logging.INFO)

MCP_SERVER_NAME = "lolbas-mcp-server"
API_URL = "https://lolbas-project.github.io/api/lolbas.json"

mcp = FastMCP(MCP_SERVER_NAME)

class LOLBASApi:
    def __init__(self, api_url=API_URL):
        self.api_url = api_url
        self._cache = None

    def _get_lolbas_data(self):
        if self._cache is not None:
            return self._cache
        try:
            resp = requests.get(self.api_url, verify=True, timeout=10)
            resp.raise_for_status()
            self._cache = resp.json()
            return self._cache
        except Exception as e:
            logging.error(f"Failed to fetch LOLBAS data: {e}")
            raise

    def find_by_name(self, file_name: str):
        try:
            data = self._get_lolbas_data()
            for entry in data:
                if entry.get("Name", "").upper() == file_name.upper():
                    return entry
            return {"Error": f"{file_name} was not found in LOLBAS! Check the file name including extension."}
        except Exception as e:
            return {"Error": f"Could not query LOLBAS: {str(e)}"}

    def find_by_category(self, category: str):
        try:
            data = self._get_lolbas_data()
            results = []
            for entry in data:
                matching_cmds = [
                    cmd for cmd in entry.get("Commands", [])
                    if cmd.get("Category", "").lower() == category.lower()
                ]
                if matching_cmds:
                    results.append({
                        "Name": entry.get("Name"),
                        "Description": entry.get("Description"),
                        "Commands": matching_cmds
                    })
            if results:
                return results
            else:
                return {"Error": f"No LOLBAS entries found with category '{category}'."}
        except Exception as e:
            return {"Error": f"Could not query LOLBAS: {str(e)}"}

    def list_binaries(self):
        try:
            data = self._get_lolbas_data()
            return sorted({entry.get("Name") for entry in data if entry.get("Name")})
        except Exception as e:
            return {"Error": f"Could not retrieve LOLBAS binaries: {str(e)}"}

    def list_categories(self):
        try:
            data = self._get_lolbas_data()
            categories = set()
            for entry in data:
                for cmd in entry.get("Commands", []):
                    category = cmd.get("Category")
                    if category:
                        categories.add(category)
            return sorted(categories)
        except Exception as e:
            return {"Error": f"Could not retrieve LOLBAS categories: {str(e)}"}

    def refresh_cache(self):
        """Force refresh the LOLBAS data cache from the API."""
        self._cache = None
        try:
            self._get_lolbas_data()
            return {"status": "OK", "message": "Cache refreshed successfully."}
        except Exception as e:
            return {"status": "ERROR", "message": f"Cache refresh failed: {str(e)}"}

lolbas = LOLBASApi()

@mcp.tool(description="Return a list of all binaries/scripts found within the LOLBAS project.")
def list_binaries():
    return lolbas.list_binaries()

@mcp.tool(description="Return a list of all unique operational categories within LOLBAS, for example: Download, Execute, Tamper. These categories represent the main techniques or use cases associated with living-off-the-land binaries and scripts.")
def list_categories():
    return lolbas.list_categories()

@mcp.tool(description="Query LOLBAS for a specific binary/script by name.")
def query_file(file_name: Annotated[str, "The name of the file to query, for example: 'certutil.exe', 'mshta.exe', etc."]):
    return lolbas.find_by_name(file_name)

@mcp.tool(description="Query LOLBAS for all binaries/scripts that include at least one command in a given category, for example: Download, Execute, Copy.")
def query_category(category: Annotated[str, "The category of commands to search for, for example: 'Download', 'Execute', etc."]):
    return lolbas.find_by_category(category)

@mcp.tool(description="Refresh your local cache with the latest updates from the LOLBAS project.")
def refresh_local_cache():
    return lolbas.refresh_cache()

if __name__ == "__main__":
    logging.info(f"Starting MCP server: {MCP_SERVER_NAME}")
    mcp.run()