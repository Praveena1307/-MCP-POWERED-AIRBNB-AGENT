import os
import sys
import asyncio
from typing import List
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

#use ProactorEventLoopPolicy to support subprocess
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Load environment variables
load_dotenv()

# Gemini client setup
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = "gemini-2.0-flash"

# MCP server parameters
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@openbnb/mcp-server-airbnb",
        "--ignore-robots-txt",
    ],
    env=None,
)

# Agent loop
async def agent_loop(prompt: str, client: genai.Client, session: ClientSession):
    contents = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    await session.initialize()

    mcp_tools = await session.list_tools()
    tools = types.Tool(function_declarations=[
        {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.inputSchema,
        }
        for tool in mcp_tools.tools
    ])

    response = await client.aio.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0,
            tools=[tools],
        ),
    )

    contents.append(response.candidates[0].content)

    turn_count = 0
    max_tool_turns = 5
    while response.function_calls and turn_count < max_tool_turns:
        turn_count += 1
        tool_response_parts: List[types.Part] = []

        for fc_part in response.function_calls:
            tool_name = fc_part.name
            args = fc_part.args or {}
            st.info(f"Calling MCP tool: `{tool_name}` with args: {args}")

            tool_response: dict
            try:
                tool_result = await session.call_tool(tool_name, args)
                if tool_result.isError:
                    tool_response = {"error": tool_result.content[0].text}
                else:
                    tool_response = {"result": tool_result.content[0].text}
            except Exception as e:
                tool_response = {
                    "error":  f"Tool execution failed: {type(e).__name__}: {e}"}

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=tool_name, response=tool_response
                )
            )

        contents.append(types.Content(role="user", parts=tool_response_parts))
        response = await client.aio.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=1.0,
                tools=[tools],
            ),
        )
        contents.append(response.candidates[0].content)

    if turn_count >= max_tool_turns and response.function_calls:
        st.warning("Reached maximum tool turns. Stopping.")

    return response

# Main async wrapper
async def async_main(prompt: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            return await agent_loop(prompt, client, session)

# Streamlit UI
st.set_page_config(page_title="MCP - Airbnb Agent", layout="centered")
st.title("🏡 MCP Powered Airbnb Booking")

user_prompt = st.text_area("Enter your booking request:",
                           "I want to book an apartment in Paris for 2 nights. 03/28 - 03/30")

if st.button("Run Agent"):
    with st.spinner():
        result = asyncio.run(async_main(user_prompt))
        st.success("Agent response:")
        st.markdown(result.text)
