#!/usr/bin/env python3
import ollama


### Constants ###
MODEL = "llama3.1"
OPTIONS = {
    # defined in https://github.com/ollama/ollama/blob/main/docs/modelfile.md
    'num_ctx': 2048,        # default is 2048
    'num_predict': 1024,    # default is 128
    'temperature': 0.2,     # default is 0.8
    'top_k': 5,             # default is 40
    'top_p': 0.5,           # default is 0.9
    'repeat_penalty': 1.0,  # default is 1.1
    'seed': 17,             # default is 0
    'stop': ['<|eot_id|>']
}

class OllamaWrapper:
    def __init__(self):
        self.model = MODEL
        self.model_options = OPTIONS

    def generate_response(self, messages, tools):
        if messages and tools:
            return ollama.chat(model=self.model, options=self.model_options, stream=False, keep_alive="1h", messages=messages, tools=tools)
        return ""