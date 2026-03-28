from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

PACKAGE_ID = 'multigit'
STAGED_INSTALLER_NAME = 'multigit-install.exe'
ROOT_DIR = pathlib.Path(__file__).resolve().parents[2]
PACKAGE_DIR = pathlib.Path(__file__).resolve().parent
TOOLS_DIR = PACKAGE_DIR / 'tools'
NUSPEC_PATH = PACKAGE_DIR / f'{PACKAGE_ID}.nuspec'
VERSION_RE = re.compile(r"VERSION = '([^']+)'")
NUSPEC_VERSION_RE = re.compile(r'<version>([^<]+)</version>')
TOOL_FILES = ('chocolateyinstall.ps1', 'chocolateyuninstall.ps1')


def read_project_version() -> str:
    content = (ROOT_DIR / 'src' / 'mg_const.py').read_text(encoding='utf-8')
    match = VERSION_RE.search(content)
    if match is None:
        raise RuntimeError('Unable to read VERSION from src/mg_const.py')
    return match.group(1)


def read_nuspec_version() -> str:
    content = NUSPEC_PATH.read_text(encoding='utf-8')
    match = NUSPEC_VERSION_RE.search(content)
    if match is None:
        raise RuntimeError(f'Unable to read version from {NUSPEC_PATH}')
    return match.group(1)

def default_installer_path(version: str) -> pathlib.Path:
    return ROOT_DIR / 'Setup' / f'Multigit OpenSource {version}.exe'


def stage_package(installer_path: pathlib.Path, stage_dir: pathlib.Path) -> pathlib.Path:
    project_version = read_project_version()
    nuspec_version = read_nuspec_version()
    if project_version != nuspec_version:
        raise RuntimeError(
            f'Chocolatey package version mismatch: src/mg_const.py has {project_version} '
            f'but {NUSPEC_PATH.name} has {nuspec_version}'
        )

    if not installer_path.is_file():
        raise FileNotFoundError(f'Installer not found: {installer_path}')

    if stage_dir.exists():
        shutil.rmtree(stage_dir)

    tools_output_dir = stage_dir / 'tools'
    tools_output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(NUSPEC_PATH, stage_dir / NUSPEC_PATH.name)
    for tool_file in TOOL_FILES:
        shutil.copy2(TOOLS_DIR / tool_file, tools_output_dir / tool_file)

    shutil.copy2(installer_path, tools_output_dir / STAGED_INSTALLER_NAME)
    return stage_dir / NUSPEC_PATH.name



def pack_package(nuspec_path: pathlib.Path, output_dir: pathlib.Path) -> pathlib.Path:
    choco_executable = shutil.which('choco')
    if choco_executable is None:
        raise FileNotFoundError("Chocolatey executable 'choco' was not found in PATH")

    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [choco_executable, 'pack', nuspec_path.name, '--outputdirectory', str(output_dir.resolve())],
        cwd=nuspec_path.parent,
        check=True,
    )
    return output_dir / f'{PACKAGE_ID}.{read_project_version()}.nupkg'



def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Stage and optionally build the Chocolatey package for Multigit.')
    parser.add_argument(
        '--installer',
        type=pathlib.Path,
        help='Path to the Windows installer to embed. Defaults to Setup/IDEMIA Multigit OpenSource <version>.exe',
    )
    parser.add_argument(
        '--stage-dir',
        type=pathlib.Path,
        default=ROOT_DIR / 'build' / 'chocolatey' / 'package',
        help='Directory used to stage the Chocolatey package before packing.',
    )
    parser.add_argument(
        '--output-dir',
        type=pathlib.Path,
        default=ROOT_DIR / 'dist',
        help='Directory receiving the final .nupkg output.',
    )
    parser.add_argument(
        '--skip-pack',
        action='store_true',
        help='Only prepare the staging directory and skip the Chocolatey pack command.',
    )
    return parser.parse_args(argv)



def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    version = read_project_version()
    installer_path = (args.installer or default_installer_path(version)).resolve()
    stage_dir = args.stage_dir.resolve()
    output_dir = args.output_dir.resolve()

    try:
        nuspec_path = stage_package(installer_path, stage_dir)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

    print(f'Staging prepared in: {stage_dir}')
    print(f'Embedded installer: {installer_path}')

    if args.skip_pack:
        print('Skipping Chocolatey pack step as requested.')
        return 0

    try:
        package_path = pack_package(nuspec_path, output_dir)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1

    print(f'Chocolatey package created: {package_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

