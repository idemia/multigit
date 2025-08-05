:: pyuic5 must be in the path for this to work

:: save directory and switch to current directory
pushd %~dp0

rem Generate ui files only if needed and add type annotations
py gen_and_patch_ui.py %* ^
		ui_about.ui ^
		ui_dialog_quit.ui ^
		ui_about_license.ui ^
		ui_main_window.ui ^
		ui_multigit_widget.ui ^
		ui_git_push_tag.ui ^
		ui_apply_mgit_file.ui ^
		ui_git_revert.ui ^
		ui_select_repos.ui ^
		ui_preferences.ui ^
		ui_repo_properties.ui ^
		ui_git_exec_window.ui ^
		ui_git_tag.ui ^
		ui_git_run_command.ui ^
		ui_export_csv.ui ^
		ui_git_create_branch.ui ^
		ui_git_switch_branch.ui ^
		ui_git_commit.ui ^
		ui_clone_from_mgit.ui ^
		ui_export_mgit.ui ^



:: restore directory
popd

if not "%~1" == "/nopause" pause
