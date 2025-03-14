; Script de Inno Setup para criar um instalador .msi
[Setup]
AppName=OrgAI
AppVersion=1.0
DefaultDirName={pf}\OrgAI
DefaultGroupName=OrgAI
OutputDir=.
OutputBaseFilename=OrgAI_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\OrgAI.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\OrgAI"; Filename: "{app}\OrgAI.exe"; IconFilename: "{app}\logo.ico"
Name: "{group}\{cm:UninstallProgram,OrgAI}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\OrgAI.exe"; Description: "{cm:LaunchProgram,OrgAI}"; Flags: nowait postinstall skipifsilent