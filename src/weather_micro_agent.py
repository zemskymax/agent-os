#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from model_wrappers.vllm_model_wrapper import VllmWrapper
from tools.time_date_tools import TimeDateToolsManager
from tools.weather_tools import WeatherToolsManager


SYSTEM = "You are a helpful assistant that gives weather updates. Use available tools."

class WeatherMicroAgent(BaseMicroAgent):
    def __init__(self, system):
        tool_managers = [TimeDateToolsManager(), WeatherToolsManager()]
        BaseMicroAgent.__init__(self, system=system, tool_managers=tool_managers)
        # self.model = OllamaWrapper()
        self.model = VllmWrapper()

def main():
    prompt = "What is the current date and weather in Athens?"

    weather_agent = WeatherMicroAgent(SYSTEM)
    print(weather_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
