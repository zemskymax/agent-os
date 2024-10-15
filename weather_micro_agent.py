#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from tools.weather_tools import WeatherToolsManager


class WeatherMicroAgent(BaseMicroAgent):
    def __init__(self):
        BaseMicroAgent.__init__(self)
        self.model = OllamaWrapper()
        self.tools_manager = WeatherToolsManager()

def main():
    prompt = "What is the weather in Paris?"

    weather_agent = WeatherMicroAgent()
    print(weather_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
