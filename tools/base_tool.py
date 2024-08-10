#!/usr/bin/env python3
import json
from typing import List

class ToolParameter:
    def __init__(self, name: str, description: str, type: str, required: bool) -> None:
        self.name = name
        self.description = description
        self.type = type
        self.required = required

    def to_json(self) -> str:
        param = {
            f"{self.name}": {
                "type": self.type, 
                "description": self.description            
            }
        }
        return json.dumps(param)

    def to_dict(self):
        param = {
            f"{self.name}": {
                "type": self.type, 
                "description": self.description            
            }
        }
        return param


class ToolParameters:
    def __init__(self, parameters: List[ToolParameter]) -> None:
        self.parameters = parameters

    def to_json(self) -> str:
        required = []
        properties = {}
        for param in self.parameters:
            if param.required:
                required.append(param.name)
            properties.update(param.to_dict())

        params = {
            "type": "object",
            "properties": properties,
            "required": required
        }
        return json.dumps(params)

    def to_dict(self):
        required = []
        properties = {}
        for param in self.parameters:
            if param.required:
                required.append(param.name)
            properties.update(param.to_dict())

        params = {
            "type": "object",
            "properties": properties,
            "required": required
        }
        return params 


class Tool:
    def __init__(self, name: str, description: str, parameters: ToolParameters) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters 

    def to_json(self) -> str:
        tool_dict = {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters.to_dict()
        }
        return json.dumps(tool_dict)

    def to_dict(self):
        tool_dict = {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters.to_dict()
        }
        return tool_dict


class ToolsArray:
    def __init__(self, tools: List[Tool]) -> None:
        self.tools = tools

    def to_json(self) -> str:
        tools_arr = []
        for tool in self.tools:
            tools_arr.append(tool.to_dict())
        return json.dumps(tools_arr)

    def to_dict(self):
        tools_arr = []
        for tool in self.tools:
            tools_arr.append(tool.to_dict())
        return tools_arr


if __name__ == "__main__":
    city_to_lat_long_parameter = ToolParameter(name="city", description="The city to get the latitude and longitude for.", type="string", required=True)
    city_to_lat_long_parameters = ToolParameters(parameters=[city_to_lat_long_parameter])
    city_to_lat_long_tool = Tool(name="CityToLatLong", description="Get the latitude and longitude for a given city.", parameters=city_to_lat_long_parameters)

    print_content_to_user_parameter = ToolParameter(name="content", description="The content of the output string to print.", type="string", required=True)
    print_content_to_user_parameters = ToolParameters(parameters=[print_content_to_user_parameter])
    print_content_to_user_tool = Tool(name="PrintContentToUser", description="Print the string to the user.", parameters=print_content_to_user_parameters)

    all_tools = ToolsArray(tools=[city_to_lat_long_tool, print_content_to_user_tool])
    print(all_tools.to_json())
