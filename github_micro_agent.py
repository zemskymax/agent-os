#!/usr/bin/env python3
from base_micro_agent import BaseMicroAgent
from model_wrappers.ollama_model_wrapper import OllamaWrapper
from model_wrappers.vllm_model_wrapper import VllmWrapper
from tools.github_tools import GithubToolsManager


SYSTEM = """You are a helpful assistant. You are tasked with enhancing the README file of an open-source project to improve its discoverability and appeal to potential contributors.
# Your task:
## Project Documentation & README Enhancement:
Write a comprehensive and well-organized README file that includes a project overview, its purpose, and key features.
eNSURE TO highlight the relevant technologies used, the problem the project solves, and the target audience.
Provide detailed sections on installation, usage, and contributing guidelines, making it easy for new users and developers to understand the project.
Incorporate visual elements such as screenshots, GIFs, or diagrams to make the README engaging and informative.
## SEO Optimization:
Optimize the README for search engines by using relevant keywords throughout, particularly related to the project’s technologies and goals.
Use structured headings (H1, H2, etc.) and include descriptive alt text for images to ensure search engines can index the content effectively.
Incorporate external links to related tools, technologies, or resources, and internal links to further project documentation.
## Content Management & Updates:
Ensure the README remains up to date, reflecting any changes in the project, new features, or milestones.
Organize the content so it remains easy to follow and relevant as the project evolves.
Focus on writing the README to be both user-friendly and SEO-optimized, aiming to improve the project’s visibility in search engines and attract contributors from the open-source community.
"""

class GithubMicroAgent(BaseMicroAgent):
    def __init__(self, system):
        tool_managers = [GithubToolsManager()]
        BaseMicroAgent.__init__(self, system, tool_managers=tool_managers)
        self.model = VllmWrapper()
        # self.model = OllamaWrapper()

def main():
    # prompt = """Check all the python files in the the 'zemskymax/private_chat' git repository. Provide the best documentation (docstring) in english for each class and function found in this repository.
    # Upload the new content to a new branch in the repository.  Use available tools. Important - JSON data must be correct! Do not provide explanations."""
    # prompt = "Receive all the content from the 'zemskymax/private_chat' git repository."
    # prompt = "Update the 'README.md' file in the 'stam_1' branch ('zemskymax/private_chat' git repository) with 'Hello World1' text."
    # prompt = "Create new 'stam_1' branch in the 'zemskymax/private_chat' git repository."
    # prompt = "Create a new branch in the 'zemskymax/private_chat' git repository."
    prompt = "Scan the 'zemskymax/private_chat' git repository. Update or create the best readme file. Upload the new content to a new branch in the repository."

    github_agent = GithubMicroAgent(SYSTEM)
    print(github_agent.handle_input(prompt))

if __name__ == "__main__":
    main()
