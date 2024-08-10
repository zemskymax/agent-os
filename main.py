#!/usr/bin/env python3
import ollama
from tools.weather_tools import *
from auxiliary.custom_logger import *

### Constants ###
MODEL = "llama3.1"
PROMPT = "What is the weather in Paris?"
OPTIONS = {
    # defined in https://github.com/ollama/ollama/blob/main/docs/modelfile.md
    'num_ctx': 2048,        # default is 2048
    'num_predict': 1024,    # default is 128
    'temperature': 0.0,     # default is 0.8
    'top_k': 5,             # default is 40
    'top_p': 0.5,           # default is 0.9
    'repeat_penalty': 1.0,  # default is 1.1
    'seed': 17,             # default is 0
    'stop': ['<|eot_id|>']
}

class WeatherMicroAgent:
    def __init__(self):
        self.history = PROMPT
        self.model = MODEL
        self.model_options = OPTIONS
        self.weatherToolsManager = WeatherToolsManager()
        self.messages = []
        self.logger = CustomLogger()

    def _call_agent(self):
        self.logger.print_log("\nFull conversation history.\n" + str(self.messages), DEBUG)
        tools = self.weatherToolsManager.get_all_tools()
        # print("tools: " + str(tools))
        response = ollama.chat(self.model, messages=self.messages, stream=False, tools=tools, keep_alive="1h")
        # print("response: " + str(response))

        if response["message"]:
            self.messages.append(response["message"])
            return response["message"]
        return ""

    def _handle_user(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        # print("messages: " + str(self.messages))
    
    def _handle_tool(self, tool_name: str, tool_arguments):
        tool_response = self.weatherToolsManager.handle_tool_as_json(tool_name=tool_name, tool_arguments=tool_arguments)
        if tool_response:
            self.logger.print_log("\nTool response:\n" + str(tool_response), INFO)
            self.messages.append({'role': 'tool', 'content': tool_response})
        else:
            self.logger.print_log("\nTool response is empty!\n", ERROR)

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

if __name__ == "__main__":
    weather_agent = WeatherMicroAgent()

    print(weather_agent.handle_input(PROMPT))
