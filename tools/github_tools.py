#!/usr/bin/env python3
import json
import time
from typing import List
from github import Github, Auth, GithubException, UnknownObjectException
from auxiliary.env_variable_handler import EnvironmentVariableHandler
from tools.base_tool import *
from tools.base_tools_manager import BaseToolsManager


FILES_TO_EXCLUDE = [".gitignore", "LICENSE"]

class GithubToolsManager(BaseToolsManager):
    def __init__(self) -> None:
        BaseToolsManager.__init__(self)
        github_repo_full_name_parameter = ToolParameter(name="github", description="The github repository name to get the content for.", type="string", required=True)
        github_repo_name_to_content_tool_parameters = ToolParameters(parameters=[github_repo_full_name_parameter])
        github_repo_name_to_content_tool = Tool(name="GithubRepoNameToContentTool", description="Get the content for a given github repository.", parameters=github_repo_name_to_content_tool_parameters)
        # TODO. add tool example
        # TODO. add callback function

        github_repo_full_name_parameter = ToolParameter(name="github", description="The github repository name to create a new branch.", type="string", required=True)
        github_branch_name_parameter = ToolParameter(name="branch_name", description="The branch name to create.", type="string", required=False)
        github_create_new_branch_tool_parameters = ToolParameters(parameters=[github_repo_full_name_parameter, github_branch_name_parameter])
        github_create_new_branch_tool = Tool(name="GithubCreateNewBranchTool", description="Create new branch in a given github repository.", parameters=github_create_new_branch_tool_parameters)

        github_repo_full_name_parameter = ToolParameter(name="github", description="The github repository name.", type="string", required=True)
        github_branch_name_parameter = ToolParameter(name="branch_name", description="The branch name where the file should get updated. Will create a new branch or skip if exists.", type="string", required=True)
        github_file_name_parameter = ToolParameter(name="file_name", description="The name of the existing file that need to be update.", type="string", required=True)
        github_content_parameter = ToolParameter(name="file_content", description="New content to replace the existing one of the file. Must provide the content in the correct JSON format (Escape single and double quotes)!", type="string", required=True)
        github_update_file_tool_parameters = ToolParameters(parameters=[github_repo_full_name_parameter, github_branch_name_parameter, github_file_name_parameter, github_content_parameter])
        github_update_file_tool = Tool(name="GithubUpdateFileContentTool", description="Update a file in a branch for a given github repository.", parameters=github_update_file_tool_parameters)

        self.tools = ToolsArray(tools=[github_repo_name_to_content_tool, github_update_file_tool])
        # print(self.tools.to_json())

        # TODO. move to the Github engine manager class
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
        # or self.gh = github.Github(login, password)

    def _get_github_repo(self, repo_full_name):
        return self.gh.get_repo(repo_full_name)

    def _get_github_repo_content(self, repo_full_name):
        github_repo = self._get_github_repo(repo_full_name)

        github_repo_hierarchy = {"repo name": github_repo.name, "type": "directory", "children": self._get_all_files_in_github_repo(github_repo)}

        return github_repo_hierarchy

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
        # TODO. set active branch
        contents = github_repo.get_contents(file_path)
        text = contents.decoded_content.decode()
        return text

    def _get_default_branch(self, github_repo, default_branch="master"):
        return github_repo.get_branch(default_branch)

    def _check_branch_exists(self, github_repo, branch) -> bool:
        # curr_branch = github_repo.get_branch(branch="branch")
        # print(curr_branch)
        for br in github_repo.get_branches():
            if branch == br.name:
                return True
        return False

    def _create_new_branch(self, repo_full_name, branch="temp1"):
        print(f"Create new {branch} branch.")

        github_repo = self._get_github_repo(repo_full_name)

        default_branch = self._get_default_branch(github_repo)
        print(f"Default branch: \n{default_branch.name} \nNew branch: \n{branch}")

        status = "success"
        try:
            github_repo.create_git_ref(ref='refs/heads/' + branch, sha=default_branch.commit.sha)
            time.sleep(2.5)
        except GithubException as ex:
            print(f"Error: {ex}")
            # print(ex.data['errors'][0]['code']) # error
            status = f"Error code: {ex.status}, error message: {ex.data['message']}"

        return {"repo_name": github_repo.name, "branch_name": branch, "status": status}

    def _update_file(self, repo_full_name, branch, file_name, file_content="temp1"):
        print(f"Repo: \n{repo_full_name}")
        github_repo = self._get_github_repo(repo_full_name)

        print(f"Branch: \n{branch} \nFile name: \n{file_name} \nFile content: \n{file_content}")

        if not self._check_branch_exists(github_repo, branch):
            self._create_new_branch(repo_full_name, branch)

        try:
            file = github_repo.get_contents(file_name, ref=branch)
        except UnknownObjectException as exp:
            print(f"Create new {file_name} file.")
            file = github_repo.create_file(file_name, f"Auto create {file_name} file.", "", branch=branch)

        print(f"File: \n {file.path}")
        github_repo.update_file(file.path, "Test1", file_content, file.sha, branch=branch)
        # API: update_file(path, message, content, sha, branch=NotSet, committer=NotSet, author=NotSet)

        return {"repo_name": github_repo.name, "branch_name": branch, "file": file_name, "status": "success"}

    def handle_tool_as_json(self, tool_name, tool_arguments):
        # TODO. Convert to dictionary search
        tool_response = {}
        if tool_name == "GithubRepoNameToContentTool":
            tool_result = self._get_github_repo_content(repo_full_name=tool_arguments["github"])
            tool_response = {"name": tool_name, "result": tool_result}
        elif tool_name == "GithubCreateNewBranchTool":
            # TODO. Test with empty branch name
            if "branch_name" in tool_arguments:
                new_branch_name = tool_arguments["branch_name"]
            tool_result = self._create_new_branch(repo_full_name=tool_arguments["github"], branch=new_branch_name)
            tool_response = {"name": tool_name, "result": tool_result}
        elif tool_name == "GithubUpdateFileContentTool":
            tool_result = self._update_file(repo_full_name=tool_arguments["github"], branch=tool_arguments["branch_name"],
                                            file_name=tool_arguments["file_name"], file_content=tool_arguments["file_content"])
            tool_response = {"name": tool_name, "result": tool_result}

        return json.dumps(tool_response)

def main():
    # github_repo_full_name = "zemskymax/data-ai-extractor"
    github_repo_full_name = "zemskymax/private_chat"

    githubToolsManager = GithubToolsManager()
    print(githubToolsManager.get_all_tools())

    github_repo_hierarchy_as_json = githubToolsManager._get_github_repo_content(github_repo_full_name)

    print(github_repo_hierarchy_as_json)


if __name__ == "__main__":
    main()
