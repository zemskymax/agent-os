from tools.github_tools import GithubToolsManager


def main():

    tool_managers = [GithubToolsManager()]
    tools = []
    for tool_manager in tool_managers:
        tools += tool_manager.get_all_tools()

    for tool in tools:
        print(str(tool.to_json()))


if __name__ == "__main__":
    main()
