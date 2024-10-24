import json
import os
import pathlib
from tools.base_tool import Tool, ToolParameter, ToolParameters, ToolsArray
from tools.base_tools_manager import BaseToolsManager


FILES_TO_EXCLUDE = ["LICENSE"]
FOLDERS_TO_EXCLUDE = ["env", "__pycache__", "tests"]

class FileToolsManager(BaseToolsManager):
    # TODO. supports only Ubuntu - add Windows support
    def __init__(self) -> None:
        BaseToolsManager.__init__(self)

        folder_full_path_parameter = ToolParameter(name="folder_path", description="The full folder path to get the content for.", type="string", required=True)
        folder_to_content_tool_parameters = ToolParameters(parameters=[folder_full_path_parameter])
        folder_to_content_tool = Tool(name="FolderToContentTool", description="Get the content for a given folder.", parameters=folder_to_content_tool_parameters)

        self.tools = ToolsArray(tools=[folder_to_content_tool])

    def _is_hidden(self, path):
        name = os.path.basename(os.path.abspath(path))
        return name.startswith('.')

    def _get_file_content(self, file_full_path, extension=".py"):
        file = pathlib.Path(file_full_path)
        suffix = file.suffixes[0]
        # print(suffix)
        if suffix == extension:
            contents = file.read_text()
            return contents
        return ""

    def _get_folder_content(self, path):
        if os.path.isfile(path):
            file_name = os.path.basename(path)
            if self._is_hidden(path):
                print(f"File {file_name} is hidden - skip.")
            elif file_name not in FILES_TO_EXCLUDE:
                file_content = self._get_file_content(file_full_path=path)
                # print(f"Add {file_name} file to the hierarchy.")
                return {"name": file_name, "type": "file"}
                # return {"name": file_name, "type": "file", "content": file_content}
            return    
        elif os.path.isdir(path):
            folder_name = os.path.basename(path)
            if self._is_hidden(path):
                print(f"Folder {folder_name} is hidden - skip.")
            else:
                if folder_name not in FOLDERS_TO_EXCLUDE:
                    # print(f"Add {folder_name} folder to the hierarchy.")
                    # children = [self._get_folder_content(os.path.join(path, child)) for child in os.listdir(path)]
                    children = [f for child in os.listdir(path) if (f := self._get_folder_content(os.path.join(path, child))) is not None]

                    return {"name": folder_name, "type": "folder", "children": children}
        else:
            print("WTF?")

    def _get_folder_hierarchy(self, folder_path):
        print("-")
        normalize_path = os.path.expanduser(folder_path)
        structure = self._get_folder_content(normalize_path)
        print(json.dumps(structure, indent=2))
        return structure

    def handle_tool_as_json(self, tool_name, tool_arguments):
        # TODO. Convert to dictionary search
        tool_response = {}
        if tool_name == "FolderToContentTool":
            tool_result = self._get_folder_hierarchy(folder_path=tool_arguments["folder_path"])
            tool_response = {"name": tool_name, "result": tool_result}

        return json.dumps(tool_response)

def main():
    project_full_path = "~/developer/LLMs/crew_generation"
    # project_full_path = "~/developer/LLMs/agent-os"

    file_tools_manager = FileToolsManager()
    print(file_tools_manager.get_all_tools())

    project_hierarchy_as_json = file_tools_manager._get_folder_hierarchy(project_full_path)
    print(json.dumps(project_hierarchy_as_json, indent=2))

if __name__ == "__main__":
    main()
