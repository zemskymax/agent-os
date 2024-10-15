#!/usr/bin/env python3
import json
from typing import List
from github import Github, Auth
from auxiliary.env_variable_handler import EnvironmentVariableHandler
from tools.base_tool import *


FILES_TO_EXCLUDE = [".gitignore", "LICENSE"]

class GithubToolsManager:
    def __init__(self) -> None:
        github_repo_full_name_parameter = ToolParameter(name="github", description="The github repo name to get the content for.", type="string", required=True)
        github_repo_name_to_content_tool_parameters = ToolParameters(parameters=[github_repo_full_name_parameter])
        github_repo_name_to_content_tool = Tool(name="GithubRepoNameToContentTool", description="Get the content for a given github repository.", parameters=github_repo_name_to_content_tool_parameters)
        # TODO. add tool example
        # TODO. add callback function

        self.tools = ToolsArray(tools=[github_repo_name_to_content_tool])
        # print(self.tools.to_json())

        self.gh = None

        self._validate_environment_variables()
        self._init_github()

    def __del__(self):
        if self.gh:
            self.gh.close()

    def _validate_environment_variables(self):
        env_manager = EnvironmentVariableHandler()
        github_access_token = env_manager.get_from_env("GITHUB_ACCESS_TOKEN")

        if github_access_token:
            self.auth = Auth.Token(github_access_token)
        else:
            raise Exception("Please provide Github access token!")

    def _init_github(self):
        self.gh = Github(auth=self.auth)

    def _get_github_repo_content(self, repo_full_name):
        github_repo = self.gh.get_repo(repo_full_name)

        github_repo_hierarchy = {"name": github_repo.name, "type": "directory", "children": self._get_all_files_in_github_repo(github_repo)}

        return json.dumps(github_repo_hierarchy)

    def _get_all_files_in_github_repo(self, github_repo, folder_path = ""):
        contents = github_repo.get_contents(folder_path)

        files: List[str] = []
        for content in contents:
            if content.type == "dir":
                children = self._get_all_files_in_github_repo(github_repo, content.path)
                files.append({"name": content.path, "type": "directory", "children": children})
            else:
                if content.path not in FILES_TO_EXCLUDE:
                    try:
                        file_content = self._get_file_content(github_repo, content.path)
                    except Exception as ex:
                        print(ex)
                        file_content = ""
                    files.append({"name": content.name, "type": "file", "content": file_content})

        return files

    def _get_file_content(self, github_repo, file_path):
        contents = github_repo.get_contents(file_path)
        return contents.decoded_content.decode()

    def handle_tool_as_json(self, tool_name, tool_arguments):
        # TODO. Convert to dictionary search
        if tool_name == "GithubRepoNameToContentTool":
            tool_result = self._get_github_repo_content(repo_full_name=tool_arguments["github"])
            return json.dumps(tool_result)
        else:
            return json.dumps({})

    def get_all_tools(self):
        tools_to_json = []

        tools = self.tools.to_dict()
        for tool in tools:
            tools_to_json.append({
                'type': 'function',
                'function': tool
            })

        return tools_to_json

def main():
    # github_repo_full_name = "zemskymax/data-ai-extractor"
    github_repo_full_name = "zemskymax/private_chat"

    githubToolsManager = GithubToolsManager()
    print(githubToolsManager.get_all_tools())

    github_repo_hierarchy_as_json = githubToolsManager._get_github_repo_content(github_repo_full_name)

    print(github_repo_hierarchy_as_json)


if __name__ == "__main__":
    main()
