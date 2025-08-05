#    Copyright (c) 2019-2023 IDEMIA
#    Author: IDEMIA (Philippe Fremy, Florent Oulieres)
# 
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
# 
#         http://www.apache.org/licenses/LICENSE-2.0
# 
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#


import json, re
import pathlib, logging
from typing import Dict, Any, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from src.mg_repo_info import MultiRepo, MgRepoInfo

from src.mg_utils import anonymise_git_url

logger = logging.getLogger('mg_json_mgit_parser')
dbg = logger.debug

# The mgit file format version that we generate
MGIT_FILE_FORMAT_VERSION = "1.0"

# Full format of the mgit file is documented at this page:
# doc/Multigit file format.md


def exportToMgit(mgitFname: str, desc: str, repos: List['MgRepoInfo'], snapshotMode: bool = False) -> None:
    '''Export the list of repositories to a multigit file.

    If snapshotMode is False (the default), the branch/tag information is exported.
    If snapshotMode is True, the tag or SHA1 of the commit of the branch  is exported.
    '''

    repos.sort(key=lambda repo: repo.name.lower())

    reposAsDict = []    # type: List[ Dict[str, str] ]

    for repoInfo in repos:
        # Ensure each repo has the information we need, but normally, this has already been done
        repoInfo.ensure_head_and_url(blocking=True)
        if snapshotMode:
            repoInfo.ensure_sha1(blocking=True)

        # clear username from url
        repoInfo.url = anonymise_git_url(repoInfo.url or '')

        repoDesc = ''
        head: str

            if snapshotMode:
                if 'tag' in repoInfo.head:
                    repoDesc = 'commit of %s' % repoInfo.head
                elif 'branch' in repoInfo.head:
                    repoDesc = 'commit on %s' % repoInfo.head

                # force pointing to last commit
                head_type = 'commit'
                assert repoInfo.commit_sha1 is not None # to make mypy happy, we already know that sha1 is set
                head = repoInfo.commit_sha1
            else:
                # branch or tag or commit
            head_type, head = repoInfo.head_info()

        repoDict = {
            "url": repoInfo.url or '',
            "head": head,
            "head_type": head_type,
            "destination": repoInfo.relpath,
        }
        if len(repoDesc):
            repoDict['description'] = repoDesc

        reposAsDict.append(repoDict)

    reposAsDict.sort(key=lambda rd: rd['destination'].lower())


    mgit_content = {
        'fileFormatVersion': MGIT_FILE_FORMAT_VERSION,
        'description':       desc,
        'repositories':      reposAsDict,

        # for compatibility with previous versions of MultiGit
        'variables' : {},
        'postCloneCommands': [],
     }

    with open(mgitFname, 'w', newline='', encoding='utf8', errors='replace') as jsonf:
        json.dump(mgit_content, jsonf, indent=4, sort_keys=True)



class PostCloneCommand:
    type: str
    description: str
    cmd_file: str

    def __repr__(self) -> str:
        post_cmd_str =  "    POST CLONE COMMAND: {0}\n".format(self.description)
        post_cmd_str += "        type:    {0}\n".format(self.type)
        post_cmd_str += "        file:    {0}\n".format(self.cmd_file)
        post_cmd_str += "\n"
        return post_cmd_str

    def __init__(self, dic_cmd: Dict[str, Any]) -> None:
        self.type = dic_cmd["type"]
        self.description = dic_cmd["description"]
        self.cmd_file = dic_cmd["file"]


class Repository:
    url: str
    head: str
    head_type: str
    destination: str    # relative path to which the clone should be performed
    dest_fullpath: str  # full path of the destination directory
    description: str     # optional description of the head

    def __init__(self, url: str = "", head: str = "", head_type: str = "",
                 dest: str = "", base_path: str = "") -> None:
        self.url = url
        self.head = head
        self.head_type = head_type
        # remove / or \ from the beginning of dest
        self.destination = dest.lstrip("/\\")
        self.update_basepath(base_path)
        self.description = ''

    def update_basepath(self, base_path: str) -> None:
        '''Propagate the base_path information to all repositories, to fill the full path'''
        self.dest_fullpath = str(pathlib.Path(base_path) / self.destination)

    def fill_from_json(self, dic_rep: Dict[str, str], base_path: str) -> None:
        # JSON input dictionnary format
        #     {
        #         "url": "https://repo_url/proj.git",
        #         "head": "dev",
        #         "head_type": "branch",
        #         "destination": "some/repo/path"
        #     }
        self.url = dic_rep.get("url", "")
        self.head = dic_rep.get("head", "")
        self.head_type = dic_rep.get("head_type", "")
        # remove / or \ from the beginning of destination
        self.destination = dic_rep.get("destination", "").strip("/\\")
        self.description = dic_rep.get("description", "").strip()
        self.update_basepath(base_path)


    def pretty_head(self) -> str:
        '''Pretty name of the head indicating which type of head'''
        s = ' '.join([self.head_type, self.head])
        if len(self.description):
            s += ' (%s)' % self.description
        return s


    def __repr__(self) -> str:
        repo_str =  "    REPOSITORY:\n"
        repo_str += "        URL:    {0}\n".format(self.url)
        if self.description:
            repo_str += "        Description:    {0}\n".format(self.description)
        repo_str += "        Head:    {0}\n".format(self.head)
        if self.head_type:
            repo_str += "        Head type:    {0}\n".format(self.head_type)
        repo_str += "        Destination:    {0}\n".format(self.destination)
        repo_str += "        Full path:    {0}\n".format(self.dest_fullpath)
        repo_str += "\n"
        return repo_str


class ProjectStructure:

    file_format_version: str
    base_path: pathlib.Path
    variables: Dict[str, str]
    description: str
    repos: List['Repository']
    post_commands: List['PostCloneCommand']

    def __init__(self, base_path: str = '') -> None:
        self.base_path = pathlib.Path(base_path)
        self.file_format_version = ''
        self.variables = {}
        self.description = ''
        self.repos = []
        self.post_commands = []

    def __repr__(self) -> str:
        proj_str = "PROJECT:    {0}\n\n".format('\n            '.join(self.description.split('\n')))
        proj_str += "    PATH: {0}\n".format(self.base_path)
        proj_str += '\n'
        if len(self.variables):
            proj_str += "    VARIABLES: \n"
            for k, v in self.variables.items():
                proj_str += "        {0} :    {1}\n".format(k,v)
            proj_str += "\n"
        for repo in self.repos:
            proj_str += "{0}\n".format(repo)
        if len(self.post_commands):
            for post_cmd in self.post_commands:
                proj_str += "{0}\n".format(post_cmd)
        return proj_str


    def replace_variable_in_string(self, input_str: str) -> str:
        '''In the given string, replace the value $VAR$ with the content of the variable VAR.
        Do this for every variable defined'''
        for k, v in self.variables.items():
            if input_str.find("$"+k+"$") != -1:
                input_str = input_str.replace("$"+k+"$", v)
        return input_str


    def apply_variables(self) -> None:
        '''Apply the variable substitution to all fields of the Structure and its Repositories
        and PostClone actions'''
        for k, v in self.variables.items():
            self.variables[k] = self.replace_variable_in_string(v)

        self.description = self.replace_variable_in_string(self.description)

        for repo in self.repos:
            repo.url = self.replace_variable_in_string(repo.url)
            repo.head = self.replace_variable_in_string(repo.head)
            repo.head_type = self.replace_variable_in_string(repo.head_type)
            repo.destination = self.replace_variable_in_string(repo.destination)
            repo.update_basepath(str(self.base_path))

        for post_cmd in self.post_commands:
            post_cmd.description = self.replace_variable_in_string(post_cmd.description)
            post_cmd.type = self.replace_variable_in_string(post_cmd.type)
            post_cmd.cmd_file = self.replace_variable_in_string(post_cmd.cmd_file)


    def fill_repositories_from_json_data(self, repo_list: List[Dict[str, str]]) -> None:
        self.repos = []
        for dic_rep in repo_list:
            rep = Repository()
            rep.fill_from_json(dic_rep, str(self.base_path))
            self.repos.append(rep)
        self.repos.sort(key=lambda repo: repo.destination.lower())


    def fill_postcommand_from_json_data(self, post_cmd_list: List[Dict[str, Any]]) -> List['PostCloneCommand']:
        self.post_commands = []
        for dic_cmd in post_cmd_list:
            self.post_commands.append(PostCloneCommand(dic_cmd))
        return self.post_commands


    def fill_from_json_data(self, d: Dict[str, Any]) -> None:
        self.variables = d.get("variables", {})
        self.description = d["description"]
        self.file_format_version = d["fileFormatVersion"]
        self.fill_repositories_from_json_data(d["repositories"])
        self.fill_postcommand_from_json_data(d.get("postCloneCommands", []))
        self.apply_variables()


    def set_base_path(self, base_path: pathlib.Path) -> None:
        self.base_path = base_path
        for repo in self.repos:
            repo.update_basepath(str(self.base_path))


    def fill_from_json_file(self, project_json_file: Union[pathlib.Path, str],
                            base_path: pathlib.Path) -> None:
        '''Parse the json file. May generate json.JSONDecodeError if invalid json file is provided'''
        project_json_file = pathlib.Path(project_json_file)
        with open(project_json_file, encoding='utf8') as file:
            data = json.load(file)
        self.set_base_path(base_path)
        self.fill_from_json_data(data)


