#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from tools.github_tools import *
from tools.weather_tools import *
from auxiliary.custom_logger import *

### Constants ###
MODEL = "llama3.1"
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

class WeatherMicroAgent(BaseMicroAgent):
    def __init__(self):
        BaseMicroAgent.__init__(self, model=MODEL, options=OPTIONS)
        self.tools_manager = WeatherToolsManager()

def main():
    prompt = "What is the weather in Paris?"

    weather_agent = WeatherMicroAgent()
    print(weather_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
