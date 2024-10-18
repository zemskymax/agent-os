#!/usr/bin/env python3
import json
from datetime import datetime
from tools.base_tool import Tool, ToolParameters, ToolsArray
from tools.base_tools_manager import BaseToolsManager


class TimeDateToolsManager(BaseToolsManager):
    def __init__(self) -> None:
        BaseToolsManager.__init__(self)
        get_current_time_tool = Tool(name="GetCurrentLocalTime", description="Get the current local time.", parameters=ToolParameters())
        get_current_date_tool = Tool(name="GetCurrentLocalDate", description="Get the current local date.", parameters=ToolParameters())
        get_current_date_and_time_tool = Tool(name="GetCurrentLocalDateAndTime", description="Get the current local date and time.", parameters=ToolParameters())
        self.tools = ToolsArray(tools=[get_current_time_tool, get_current_date_tool, get_current_date_and_time_tool])

    def _get_current_time(self):
        """Get the current local time as a string."""
        return {"current_time": datetime.strftime(datetime.now(), "%H:%M:%S")}

    def _get_current_date(self):
        """Get the current local date as a string."""
        return {"current_date": datetime.strftime(datetime.now(), "%Y-%m-%d")}
    
    def _get_current_date_and_time(self):
        """Get the current local date and time as a string."""
        return {"current_date_and_time": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")}

    def handle_tool_as_json(self, tool_name, tool_arguments):
        # TODO. Convert to dictionary search
        tool_response = {}
        if tool_name == "GetCurrentLocalTime":
            tool_result = self._get_current_time()
            tool_response = {"name": tool_name, "result": tool_result}
        elif tool_name == "GetCurrentLocalDate":
            tool_result = self._get_current_date()
            tool_response = {"name": tool_name, "result": tool_result}
        elif tool_name == "GetCurrentLocalDateAndTime":
            tool_result = self._get_current_date_and_time()
            tool_response = {"name": tool_name, "result": tool_result}

        return json.dumps(tool_response)

def main():
    timeDateToolsManager = TimeDateToolsManager()
    print(timeDateToolsManager.get_all_tools())

    print(timeDateToolsManager._get_current_time())
    print(timeDateToolsManager._get_current_date())
    print(timeDateToolsManager._get_current_date_and_time())

if __name__ == "__main__":
    main()