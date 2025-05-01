#!/usr/bin/env python
"""
MCP client that connects to an MCP server, loads tools, and runs a chat loop using Google Gemini LLM.
"""

import asyncio
import os
import sys
import json
from contextlib import AsyncExitStack
from typing import Optional, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

# Custom JSON encoder for objects with `content` attr
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, "content"):
            return {"type": o.__class__.__name__,
                    "content": o.content}
        return super().default(o)
    

# Instantiate Google Gemini LLM with deterministic output and retry logic