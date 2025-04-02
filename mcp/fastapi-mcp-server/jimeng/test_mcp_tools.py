#!/usr/bin/env python
"""
Test script to verify that an MCP server is properly exposing tools.
This script connects to the MCP server, initializes a session, and requests a list of available tools.
"""

# TODO: Turn this into a pytest test

import json
import sys
import asyncio
import httpx
from urllib.parse import urljoin

# Default MCP server URL
MCP_URL = "http://localhost:8088/mcp"


# 添加认证 token
AUTH_TOKEN = "sk-zhouhui1122444"  # 替换为实际的 token

async def test_mcp_tools(url=MCP_URL):
    """Connect to the MCP server and test tool exposure."""
    print(f"Connecting to MCP server at {url}...")

    # Connect to the SSE endpoint to establish connection
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        # First establish an SSE connection
        endpoint_url = None
        base_url = url.rsplit("/", 1)[0] + "/"  # Extract base URL (everything up to the last path component)

        response_queue = asyncio.Queue()

        # Task to send requests and receive responses through the SSE channel
        async def send_request(request_data, request_id):
            # Send the request
            await client.post(endpoint_url, json=request_data)
            print(f"Sent request with ID: {request_id}")

            # Wait for the response with matching ID
            while True:
                response = await response_queue.get()
                if "id" in response and response["id"] == request_id:
                    return response
                else:
                    # Not our response, put it back in the queue for someone else
                    await response_queue.put(response)

        # Start the SSE connection
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            print("Connected to MCP server")

            # Process the SSE stream
            current_event = None

            async def process_sse_stream():
                nonlocal current_event, endpoint_url

                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue

                    if line.startswith("event:"):
                        current_event = line[len("event:") :].strip()
                        print(f"Received event: {current_event}")
                    elif line.startswith("data:"):
                        data = line[len("data:") :].strip()

                        if current_event == "endpoint":
                            endpoint_path = data
                            endpoint_url = urljoin(base_url, endpoint_path.lstrip("/"))
                            print(f"Endpoint URL: {endpoint_url}")
                        elif current_event == "message":
                            try:
                                message = json.loads(data)
                                # Pretty print the JSON message
                                print("Received message:")
                                print(json.dumps(message, indent=2))

                                # Add to queue for request handlers
                                await response_queue.put(message)
                            except json.JSONDecodeError:
                                print(f"Failed to parse message: {data}")

            # Start processing the SSE stream in the background
            background_task = asyncio.create_task(process_sse_stream())

            # Wait for the endpoint URL to be set
            while endpoint_url is None:
                await asyncio.sleep(0.1)

            try:
                # 1. Initialize request
                init_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"experimental": {}},
                        "clientInfo": {"name": "mcp-test-client", "version": "0.1.0"},
                    },
                }

                print("\nSending initialize request...")
                init_result = await send_request(init_request, 1)
                print("\nInitialization response:")
                print(json.dumps(init_result, indent=2))

                # 2. Send initialized notification
                init_notification = {"jsonrpc": "2.0", "method": "notifications/initialized"}

                await client.post(endpoint_url, json=init_notification)
                print("\nSent initialized notification")

                # 3. List tools request
                list_tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

                print("\nSending tools/list request...")
                tools_result = await send_request(list_tools_request, 2)
                print("\nTools list response:")
                print(json.dumps(tools_result, indent=2))

                # Check if we got a valid response
                if "result" in tools_result and "tools" in tools_result["result"]:
                    tools = tools_result["result"]["tools"]
                    if tools:
                        print(f"\nFound {len(tools)} tools:")
                        for i, tool in enumerate(tools):
                            print(f"{i + 1}. {tool['name']}")
                            print(f"{tool.get('description', 'No description')}")

                        # 4. Find and call the get_item_count tool
                        get_item_count_tool = None
                        for tool in tools:
                            if tool["name"] == "get_item_count":
                                get_item_count_tool = tool
                                break

                        if get_item_count_tool:
                            print(f"\nTrying to call tool: {get_item_count_tool['name']}")

                            call_tool_request = {
                                "jsonrpc": "2.0",
                                "id": 3,
                                "method": "tools/call",
                                "params": {
                                    "name": get_item_count_tool["name"],
                                    "arguments": {},  # Empty arguments for get_item_count which doesn't require any
                                },
                            }

                            print("\nSending tools/call request...")
                            tool_result = await send_request(call_tool_request, 3)
                            print("\nTool call response:")
                            print(json.dumps(tool_result, indent=2))
                        else:
                            print("\nCould not find get_item_count tool")
                    else:
                        print("\nNo tools found")
                else:
                    print("\nInvalid tools/list response format")
                
                # 添加认证 token
                AUTH_TOKEN = "your_bearer_token_here"  # 替换为实际的 token
                
                async def test_mcp_tools(url=MCP_URL):
                    """Connect to the MCP server and test tool exposure."""
                    print(f"Connecting to MCP server at {url}...")
                
                    # Connect to the SSE endpoint to establish connection
                    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
                        # First establish an SSE connection
                        endpoint_url = None
                        base_url = url.rsplit("/", 1)[0] + "/"  # Extract base URL (everything up to the last path component)
                
                        response_queue = asyncio.Queue()
                
                        # Task to send requests and receive responses through the SSE channel
                        async def send_request(request_data, request_id):
                            # Send the request
                            await client.post(endpoint_url, json=request_data)
                            print(f"Sent request with ID: {request_id}")
                
                            # Wait for the response with matching ID
                            while True:
                                response = await response_queue.get()
                                if "id" in response and response["id"] == request_id:
                                    return response
                                else:
                                    # Not our response, put it back in the queue for someone else
                                    await response_queue.put(response)
                
                        # Start the SSE connection
                        async with client.stream("GET", url) as response:
                            response.raise_for_status()
                            print("Connected to MCP server")
                
                            # Process the SSE stream
                            current_event = None
                
                            async def process_sse_stream():
                                nonlocal current_event, endpoint_url
                
                                async for line in response.aiter_lines():
                                    line = line.strip()
                                    if not line:
                                        continue
                
                                    if line.startswith("event:"):
                                        current_event = line[len("event:") :].strip()
                                        print(f"Received event: {current_event}")
                                    elif line.startswith("data:"):
                                        data = line[len("data:") :].strip()
                
                                        if current_event == "endpoint":
                                            endpoint_path = data
                                            endpoint_url = urljoin(base_url, endpoint_path.lstrip("/"))
                                            print(f"Endpoint URL: {endpoint_url}")
                                        elif current_event == "message":
                                            try:
                                                message = json.loads(data)
                                                # Pretty print the JSON message
                                                print("Received message:")
                                                print(json.dumps(message, indent=2))
                                
                                                # Add to queue for request handlers
                                                await response_queue.put(message)
                                            except json.JSONDecodeError:
                                                print(f"Failed to parse message: {data}")
                                
                                # Start processing the SSE stream in the background
                                background_task = asyncio.create_task(process_sse_stream())
                
                                # Wait for the endpoint URL to be set
                                while endpoint_url is None:
                                    await asyncio.sleep(0.1)
                
                                try:
                                    # 1. Initialize request
                                    init_request = {
                                        "jsonrpc": "2.0",
                                        "id": 1,
                                        "method": "initialize",
                                        "params": {
                                            "protocolVersion": "2024-11-05",
                                            "capabilities": {"experimental": {}},
                                            "clientInfo": {"name": "mcp-test-client", "version": "0.1.0"},
                                        },
                                    }
                
                                    print("\nSending initialize request...")
                                    init_result = await send_request(init_request, 1)
                                    print("\nInitialization response:")
                                    print(json.dumps(init_result, indent=2))
                                
                                    # 2. Send initialized notification
                                    init_notification = {"jsonrpc": "2.0", "method": "notifications/initialized"}
                
                                    await client.post(endpoint_url, json=init_notification)
                                    print("\nSent initialized notification")
                                
                                    # 3. List tools request
                                    list_tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
                
                                    print("\nSending tools/list request...")
                                    tools_result = await send_request(list_tools_request, 2)
                                    print("\nTools list response:")
                                    print(json.dumps(tools_result, indent=2))
                                
                                    # Check if we got a valid response
                                    if "result" in tools_result and "tools" in tools_result["result"]:
                                        tools = tools_result["result"]["tools"]
                                        if tools:
                                            print(f"\nFound {len(tools)} tools:")
                                            for i, tool in enumerate(tools):
                                                print(f"{i + 1}. {tool['name']}")
                                                print(f"{tool.get('description', 'No description')}")
                                
                                        # 4. 修改为测试 generate_video_mcp 工具
                                        generate_video_tool = None
                                        for tool in tools:
                                            if tool["name"] == "generate_video_mcp":
                                                generate_video_tool = tool
                                                break
                                
                                        if generate_video_tool:
                                            print(f"\nTrying to call tool: {generate_video_tool['name']}")
                                
                                            call_tool_request = {
                                                "jsonrpc": "2.0",
                                                "id": 3,
                                                "method": "tools/call",
                                                "params": {
                                                    "name": generate_video_tool["name"],
                                                    "arguments": {
                                                        "prompt": "一只可爱的小猫在玩毛线球",
                                                        "aspect_ratio": "16:9",
                                                        "duration_ms": 5000,
                                                        "fps": 24,
                                                        "authorization": f"Bearer {AUTH_TOKEN}"
                                                    },
                                                },
                                            }
                                
                                            print("\nSending tools/call request...")
                                            tool_result = await send_request(call_tool_request, 3)
                                            print("\nTool call response:")
                                            print(json.dumps(tool_result, indent=2))
                                        else:
                                            print("\nCould not find generate_video_mcp tool")
                                    else:
                                        print("\nNo tools found")
                                except:
                                    print("\nInvalid tools/list response format")
            except Exception as e:
                print(f"\nError occurred: {e}")
            finally:
                                # Clean up and cancel the background task
                                background_task.cancel()
                                try:
                                    await background_task
                                except asyncio.CancelledError:
                                    pass


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else MCP_URL
    asyncio.run(test_mcp_tools(url))