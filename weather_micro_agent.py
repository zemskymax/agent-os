#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from model_wrappers.vllm_model_wrapper import VllmWrapper
from tools.time_date_tools import TimeDateToolsManager
from tools.weather_tools import WeatherToolsManager


class WeatherMicroAgent(BaseMicroAgent):
    def __init__(self, system):
        BaseMicroAgent.__init__(self)
        # self.model = OllamaWrapper()
        self.model = VllmWrapper()
        self.system = system
        self.tool_managers = [TimeDateToolsManager(), WeatherToolsManager()]

def main():
    prompt = "What is the current date and weather in Athens?"
    system = "You are a helpful assistant that gives weather updates."

    weather_agent = WeatherMicroAgent(system)
    print(weather_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
