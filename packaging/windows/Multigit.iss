#define SETUPNAME "Multigit OpenSource"

#define COMPANY "IDEMIA"
#define NAME "Multigit"

; only digits allowed here
#define VERSION "1.7.1"

; text also allowed here
#define VERSIONSTR "1.7.1"

 [_ISTool]
EnableISX=false

[Setup]
SourceDir=..\..
SetupIconFile=images\multigit-logo.ico
UninstallDisplayIcon=images\multigit-logo.ico
AppCopyright=Copyright © 2020-2023 {#COMPANY}
AppID=Multigit
AppName={#SETUPNAME}
AppVerName={#SETUPNAME} {#VERSIONSTR}    
AppPublisher={#COMPANY}
AppPublisherURL=http://github.com/idemia/multigit
AppVersion={#VERSIONSTR}
DefaultDirName={autopf}\{#SETUPNAME}
DefaultGroupName=Multigit
OutputDir=Setup
OutputBaseFilename={#SETUPNAME} {#VERSIONSTR}

VersionInfoVersion={#VERSION}
UninstallRestartComputer=false

UninstallFilesDir={app}\Uninstall

PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UsePreviousPrivileges=yes


[Files]
Source: Dist\MultiGit\*.*; DestDir: {app}; Flags: recursesubdirs;
Source: Doc\multigit-json-schema.json; DestDir: {app}

[Icons]
Name: {group}\{#NAME} {#VERSIONSTR}; Filename: {app}\{#NAME}.exe;
Name: {group}\{cm:UninstallProgram,{#NAME} {#VERSIONSTR}}; Filename: "{uninstallexe}";WorkingDir: {app};


[Code]
{ Code below is for triggering automatic uninstall of previous version before install of new version }

{ ///////////////////////////////////////////////////////////////////// }
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;


{ ///////////////////////////////////////////////////////////////////// }
function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;


{ ///////////////////////////////////////////////////////////////////// }
function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
{ Return Values: }
{ 1 - uninstall string is empty }
{ 2 - error executing the UnInstallString }
{ 3 - successfully executed the UnInstallString }

  { default return value }
  Result := 0;

  { get the uninstall string of the old app }
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/VERYSILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

{ ///////////////////////////////////////////////////////////////////// }
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;
