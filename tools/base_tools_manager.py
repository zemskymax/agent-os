#!/usr/bin/env python3


class BaseToolsManager:
    def __init__(self) -> None:
        self.tools = None

    def get_all_tools(self):
        tools_to_json = []

        tools = self.tools.to_dict()
        for tool in tools:
            tools_to_json.append({
                'type': 'function',
                'function': tool
            })

        return tools_to_json

    def has_tool_by_name(self, tool_name: str) -> bool:
        tools = self.tools.to_dict()
        for tool in tools:
            if tool["name"] == tool_name:
                return True

        return False
