#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from model_wrappers.vllm_model_wrapper import VllmWrapper
from tools.file_management_tools import FileToolsManager


SYSTEM = "You are senior software engineer with more than 10 years of experience in python development. You are specializing in python package development. Use available tools."

class ProjectMicroAgent(BaseMicroAgent):
    def __init__(self, system):
        tool_managers = [FileToolsManager()]
        BaseMicroAgent.__init__(self, system=system, tool_managers=tool_managers)
        # self.model = OllamaWrapper()
        self.model = VllmWrapper()

def main():
    prompt = """I have created a python project - 'Agent-OS'. The project has several sibling modules. It could be found at the '/home/maxpc/developer/LLMs/agent-os'. Running the
    'python src/validators/tool_validator.py', I receive the following error: from tools.github_tools import GithubToolsManager. ModuleNotFoundError: No module named 'tools'. Help me rearrange the project so i could use sibling packages."""

    weather_agent = ProjectMicroAgent(SYSTEM)
    print(weather_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
