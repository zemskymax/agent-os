#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from model_wrappers.vllm_model_wrapper import VllmWrapper
from tools.github_tools import GithubToolsManager


class GithubMicroAgent(BaseMicroAgent):
    def __init__(self, system):
        BaseMicroAgent.__init__(self)
        self.system = system
        self.model = VllmWrapper()
        # self.model = OllamaWrapper()
        self.tool_managers = [GithubToolsManager()]

def main():
    # prompt = "Provide a good docstring for each class, function and method created in the 'zemskymax/private_chat' git repository. Reply with the relevant code."
    # prompt = "Receive all the content from the 'zemskymax/private_chat' git repository."
    # prompt = "Update the 'README.md' file in the 'stam_1' branch ('zemskymax/private_chat' git repository) with 'Hello World1' text."
    # prompt = "Create new 'stam_1' branch in the 'zemskymax/private_chat' git repository."
    prompt = "Create a new branch in the 'zemskymax/private_chat' git repository."
    system = ""

    github_agent = GithubMicroAgent(system)
    print(github_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
