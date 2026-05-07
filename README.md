# VS Code Dark Modern Theme for Ghidra

English | [日本語](README.ja.md)

A VS Code Dark Modern-inspired theme for Ghidra 12.0.4 PUBLIC.

![VS Code Dark Modern theme screenshot](https://raw.githubusercontent.com/pinksawtooth/VS_Code_dark_modern_theme/main/assets/screenshot.png)

This package is made from a Ghidra theme file and external icon assets. It installs into the Ghidra user settings directory and does not modify Ghidra's application directory, jar files, or signed binaries.

## Contents

- `themes/vscode-dark-modern.theme`
- `images/vscode/codicons/`
- `install.ps1`
- `install.sh`

`images/vscode/codicons/` contains the PNG icons referenced by the theme through `[EXTERNAL]images/vscode/codicons/...`, plus the Codicons license files.

## Install On Windows

For Windows and Ghidra 12.0.4 PUBLIC, run PowerShell from this repository directory:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

The installer copies the theme into:

```text
%APPDATA%\ghidra\ghidra_12.0.4_PUBLIC
```

Manual Windows installation:

```powershell
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.0.4_PUBLIC'

New-Item -ItemType Directory -Force -Path "$GhidraUserDir\themes" | Out-Null
New-Item -ItemType Directory -Force -Path "$GhidraUserDir\images\vscode\codicons" | Out-Null

Copy-Item .\themes\vscode-dark-modern.theme -Destination "$GhidraUserDir\themes\" -Force
Copy-Item .\images\vscode\codicons\* -Destination "$GhidraUserDir\images\vscode\codicons\" -Recurse -Force
```

If you use a different Ghidra version, replace `ghidra_12.0.4_PUBLIC` with your Ghidra user directory name.

To install into a custom Ghidra user settings directory:

```powershell
.\install.ps1 -GhidraUserDir '<Ghidra user settings directory>'
```

## Install On macOS Or Linux

On macOS, the installer defaults to:

```text
$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC
```

On Linux, the installer defaults to:

```text
${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.0.4_PUBLIC
```

```sh
git clone https://github.com/pinksawtooth/VS_Code_dark_modern_theme.git
cd VS_Code_dark_modern_theme
./install.sh
```

You can also override the target directory when running the installer:

```sh
GHIDRA_USER_DIR="<Ghidra user settings directory>" ./install.sh
```

## Enable The Theme

1. Start or restart Ghidra.
2. Open `Edit` -> `Theme`.
3. Select `VS Code Dark Modern`.
4. Restart Ghidra if some UI parts do not update immediately.

## Update

Pull the latest version and run the installer again:

Windows:

```powershell
git pull
.\install.ps1
```

macOS or Linux:

```sh
git pull
./install.sh
```

## Uninstall On Windows

```powershell
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.0.4_PUBLIC'

Remove-Item "$GhidraUserDir\themes\vscode-dark-modern.theme" -Force
Remove-Item "$GhidraUserDir\images\vscode\codicons" -Recurse -Force
```

Restart Ghidra and choose another theme afterward.

## Uninstall On macOS Or Linux

Use the same Ghidra user settings directory that was used during installation.

macOS:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

Linux:

```sh
GHIDRA_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.0.4_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

Restart Ghidra and choose another theme afterward.

## Notes

- Ghidra stores user-installed themes under the user settings directory. On Windows, Ghidra's default settings directory is `%APPDATA%\ghidra\ghidra_<version>`.
- On macOS, Ghidra's default settings directory is `$HOME/Library/ghidra/ghidra_<version>`.
- On Linux, Ghidra's default settings directory is `${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_<version>`.
- Even if Ghidra itself is installed in a separate application directory, copy this theme to the user settings directory so Ghidra can discover it.
- This theme intentionally stays within Ghidra's theme system.
- It does not modify Ghidra jars, application files, or signed files.
- It was tested with Ghidra 12.0.4 PUBLIC.
