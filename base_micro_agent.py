#!/usr/bin/env python3
from auxiliary.custom_logger import *


class BaseMicroAgent:
    def __init__(self):
        self.history = ""
        self.messages = []
        self.tool_managers = []
        self.model = None
        self.logger = CustomLogger()

    def _handle_user(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        self.logger.print_log("\nUser input:\n" + str(self.messages), USER_INPUT_INFO)

    def _handle_tool(self, tool_name: str, tool_arguments):
        for tool_manager in self.tool_managers:
            if tool_manager.has_tool_by_name(tool_name):
                tool_response = tool_manager.handle_tool_as_json(tool_name=tool_name, tool_arguments=tool_arguments)
                if tool_response:
                    self.logger.print_log("\nTool response:\n" + str(tool_response), INFO)
                    self.messages.append({'role': 'tool', 'content': tool_response})
                else:
                    self.logger.print_log("\nTool response is empty!\n", ERROR)

    def _call_model(self):
        self.logger.print_log("\nFull conversation history.\n" + str(self.messages), DEBUG)
        tools = []
        for tool_manager in self.tool_managers:
            tools += tool_manager.get_all_tools()
        self.logger.print_log("\nAvailable tools:\n" + str(tools), TOOLS_INFO)

        response = self.model.generate_response(messages=self.messages, tools=tools)
        # print("response: " + str(response))
        # TODO. do i need to add the context (add reason why the LLM is calling a specific function) for the 'reasoning' purposes?

        # INFO. the 'response' dictionary should contain on of the following
        #   'tool_calls': [{'function': {'name': 'WeatherFromLatLongTool', 'arguments': {'latitude': 31.5, 'longitude': 35.2}}}]
        #   'content': 'The current date in Jerusalem is October 18, 2024, and the local time is 16:44. The current temperature in Jerusalem is 22.0°C.'

        if response:
            self.messages.append(response)
            return response
        return ""

    def handle_input(self, user_input):
        self._handle_user(user_input)

        while True:
            answer = self._call_model()
            if answer:
                try:
                    self.logger.print_log("\nAgent answer:\n" + str(answer), INFO)

                    if "tool_calls" in answer and len(answer["tool_calls"]) > 0:
                        for tool in answer["tool_calls"]:
                            # print(str(tool))
                            self._handle_tool(tool_name=tool["function"]["name"], tool_arguments=tool["function"]["arguments"])
                    elif "content" in answer:
                        final_response = "\nFinal response:\n" + answer["content"]
                        self.logger.print_log(final_response, DEBUG)
                        return final_response
                    else:
                        self.logger.print_log("Something bad has happened.", ERROR)
                        return ""
                except Exception as exp:
                    error = "Something went terribly wrong! Error: " + str(exp)
                    self.logger.print_log(">>> " + error + " <<<", ERROR)
                    return error
            else:
                self.logger.print_log("Unexpected end of the conversation!", ERROR)
                break
