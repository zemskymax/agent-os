from base_micro_agent import BaseMicroAgent
from tools.github_tools import GithubToolsManager

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

class GihtubMicroAgent(BaseMicroAgent):
    def __init__(self):
        BaseMicroAgent.__init__(self, model=MODEL, options=OPTIONS)
        self.tools_manager = GithubToolsManager()

def main():
    prompt = "Provide a good docstring for each class, function and method created in the 'zemskymax/private_chat' git repository. Reply with the relevant code."
    # prompt = "Receive all the content from the 'zemskymax/private_chat' git repository."

    github_agent = GihtubMicroAgent()
    print(github_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
