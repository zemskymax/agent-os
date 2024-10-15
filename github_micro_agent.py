#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from tools.github_tools import GithubToolsManager


class GithubMicroAgent(BaseMicroAgent):
    def __init__(self):
        BaseMicroAgent.__init__(self)
        self.model = OllamaWrapper()
        self.tools_manager = GithubToolsManager()

def main():
    prompt = "Provide a good docstring for each class, function and method created in the 'zemskymax/private_chat' git repository. Reply with the relevant code."
    # prompt = "Receive all the content from the 'zemskymax/private_chat' git repository."

    github_agent = GithubMicroAgent()
    print(github_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
