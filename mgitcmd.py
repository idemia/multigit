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


import argparse, sys, os
from pathlib import Path
from typing import Union, List, Optional

from src import mg_const as mgc
from src.mg_json_mgit_parser import ProjectStructure
from src.mg_tools import get_git_exec, RunProcess

HELP='''
mgitcmd clone path_to_mgit_file.mgit [--dest path_to_dir] [--shallow] 
    Clone a group of repositories according to path_to_mgit_file.mgit
    
    --dest path_to_dir: Clones into the target directory. If not provided,
                        clones into the current directory.
    
    --shalllow: Perform a shallow clone with --depth 1 . Applied only on tags
                and branches, will not work for HEAD specified as a commit. This
                speeds up the clone process by downloading less data.
                
                
mgitcmd --version
    Displays version information and exits.
  
    
mgitcmd --help
    Display this help
    
'''

VERSION_LINE = 'Multigit Command-line version v%s' % mgc.VERSION


def cmd_clone(fname: str, dest_dir: Optional[str], shallow: bool) -> None:
    if not Path(fname).exists():
        print('Mgit file does not exist: %s' % fname)
        sys.exit(0)
    project = ProjectStructure()
    base_dir = Path(dest_dir or '.').resolve()
    project.fill_from_json_file(fname, base_dir)
    print('Cloning information:')
    print(project)

    reposToClone =  project.repos[:]
    reposToClone.sort(key=lambda r: r.destination)

    errors = []
    tasks: List[Union[str, List[str]]] = []
    for repo in reposToClone:
        if Path(repo.dest_fullpath).exists():
            errors.append('Directory already exists, can not clone: %s' % repo.dest_fullpath)
        if repo.url == '':
            errors.append('Can not clone repository with empty URL: %s' % repo.destination)
        tasks.append('Cloning ' + repo.destination)
        clone_cmd = ['clone', repo.url, repo.dest_fullpath]
        tasks.append(clone_cmd)
        if shallow and repo.head_type in ('branch', 'tag'):
            clone_cmd.extend( ['--branch', repo.head ] )
            clone_cmd.extend(['--depth', '1'])
        else:
            # head_type: commit or empty
            if len(repo.head):
                # if head is empty, this is an empty repository, nothing to checkout
                tasks.append('Checkout %s@%s' % (repo.destination, repo.head))
                # use the '--' to make sure this is a branch/commit checkout
                tasks.append(['-C', repo.dest_fullpath, 'checkout', '-q', repo.head, '--'])

    if errors:
        print('Errors:')
        print('- ' + '\n- '.join(errors))
        print('Aborting')
        sys.exit(-1)

    prog_git = get_git_exec()
    if prog_git is None or len(prog_git) == 0:
        print('Can not find git with executable!')
        print('Please put it on the path or define git location in the Multigit settings.')
        sys.exit(-1)

    for task in tasks:
        if type(task) is str:
            print('[[ %s ]]' % task)
            continue

        git_cmd = [prog_git, *task]

        # our pool process does not handle force blocking, launch directly
        print('> ' + ' '.join(git_cmd))
        exit_code, cmd_out = RunProcess().exec_blocking(git_cmd, allow_errors=True)
        print(cmd_out)

        if exit_code != 0:
            print('Git failure (exit code %d)' % exit_code)
            sys.exit(-1)

    print('Clone successful.')


def main() -> None:
    if '--help' in sys.argv or len(sys.argv) == 1:
        print('USAGE: ' + HELP)
        sys.exit(0)

    if '--version' in sys.argv:
        print(VERSION_LINE)
        sys.exit(0)

    parser = argparse.ArgumentParser(add_help=False, usage=HELP)
    parser.add_argument('clone', nargs=2)
    parser.add_argument('--dest', nargs=1)
    parser.add_argument('--shallow', action='store_true', default=False)
    parse_result = parser.parse_args()

    print(VERSION_LINE)
    cmd_clone(parse_result.clone[1], (parse_result.dest or [None])[0], parse_result.shallow)

if __name__ == '__main__':
    main()


