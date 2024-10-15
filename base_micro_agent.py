import ollama
from auxiliary.custom_logger import *


class BaseMicroAgent:
    def __init__(self, model, options):
        self.history = ""
        self.model = model
        self.model_options = options
        self.messages = []
        self.tools_manager = None
        self.logger = CustomLogger()

    def _handle_user(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        # print("messages: " + str(self.messages))

    def _handle_tool(self, tool_name: str, tool_arguments):
        tool_response = self.tools_manager.handle_tool_as_json(tool_name=tool_name, tool_arguments=tool_arguments)
        if tool_response:
            self.logger.print_log("\nTool response:\n" + str(tool_response), INFO)
            self.messages.append({'role': 'tool', 'content': tool_response})
        else:
            self.logger.print_log("\nTool response is empty!\n", ERROR)

    def _call_agent(self):
        self.logger.print_log("\nFull conversation history.\n" + str(self.messages), DEBUG)
        tools = self.tools_manager.get_all_tools()
        # print("tools: " + str(tools))
        response = ollama.chat(self.model, messages=self.messages, stream=False, tools=tools, keep_alive="1h")
        # print("response: " + str(response))

        if response["message"]:
            self.messages.append(response["message"])
            return response["message"]
        return ""

    def handle_input(self, user_input):
        self._handle_user(user_input)

        while True:
            answer = self._call_agent()
            if answer:
                try:
                    self.logger.print_log("\nAgent answer received:\n" + str(answer), INFO)

                    if "tool_calls" in answer and len(answer["tool_calls"]) > 0:
                        for tool in answer["tool_calls"]:
                            print(str(tool))
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
