; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#include "environment.iss"

#define MyAppDirectory "Alert Logic\alcli"
#define MyAppName "Alert Logic CLI"
#define MyAppPublisher "Alert Logic, Inc."
#define MyAppURL "https://github.com/alertlogic/alcli"
#define MyAppExeName "alcli.exe"
#define WorkingDir "C:\Users\travis\build\alertlogic\alcli\"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{07CF5DE4-A7A5-4EA6-8A71-200EB58574ED}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright (C) 2020 Alert Logic, Inc.
SetupIconFile="{#WorkingDir}icons/alertlogic-win.ico"
WizardImageFile="{#WorkingDir}icons/alertlogic-modern-image.bmp"
WizardSmallImageFile="{#WorkingDir}icons/alertlogic-modern-small-image.bmp"
DefaultDirName={autopf}\{#MyAppDirectory}
DisableWelcomePage=no
DisableReadyPage=yes
DisableProgramGroupPage=yes
LicenseFile={#WorkingDir}LICENSE
; Uncomment the following line to run in non administrative install mode (install for current user only.)
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=commandline
OutputBaseFilename=alcli_setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesEnvironment=true
SignTool=signtool $f
SignedUninstaller=true
UninstallDisplayIcon={app}\alcli.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "envPath"; Description: "Add to PATH variable" 

[Files]
Source: "{#WorkingDir}build\exe.win-amd64-3.8\alcli.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#WorkingDir}build\exe.win-amd64-3.8\lib\*"; DestDir: "{app}\Lib"; Excludes: "{#WorkingDir}build\exe.win-amd64-3.8\lib\VCRUNTIME140.dll,{#WorkingDir}build\exe.win-amd64-3.8\lib\test\*,{#WorkingDir}build\exe.win-amd64-3.8\lib\*\test\*"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#WorkingDir}build\exe.win-amd64-3.8\python38.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#WorkingDir}build\exe.win-amd64-3.8\lib\VCRUNTIME140.dll"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Name: "{commonprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Run]
; Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait skipifsilent

[Code]

procedure CurStepChanged(CurStep: TSetupStep);
begin
    if (CurStep = ssPostInstall) and WizardIsTaskSelected('envPath')
    then EnvAddPath(ExpandConstant('{app}'));
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
    if CurUninstallStep = usPostUninstall
    then EnvRemovePath(ExpandConstant('{app}'));
end;
