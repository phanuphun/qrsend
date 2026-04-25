[Setup]
AppName=QR Send
AppVersion=1.0.0
AppPublisher=Phanuphun Namwong
DefaultDirName={autopf}\qrsend
DefaultGroupName=QR Send
OutputBaseFilename=qrsend-setup
OutputDir=Output
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "..\dist\qrsend.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "com0com-setup\setup.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "com0com-setup\ReadMe.txt"; DestDir: "{tmp}"; Flags: deleteafterinstall
Source: "com0com-setup\ReadMe1st.txt"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "{tmp}\setup.exe"; Parameters: "/S"; StatusMsg: "Installing com0com driver..."; Flags: waituntilterminated

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: not ContainsPath('{app}')

[Code]
function ContainsPath(Param: string): boolean;
var
  OrigPath: string;
begin
  if not RegQueryStringValue(HKLM,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path', OrigPath)
  then begin
    Result := False;
    exit;
  end;
  Result := Pos(';' + Param + ';', ';' + OrigPath + ';') > 0;
end;

