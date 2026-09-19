# VS Code Dark Modern Theme for Ghidra

English | [日本語](README.ja.md)

A VS Code Dark Modern-inspired theme for Ghidra 12.1.3 PUBLIC.

![VS Code Dark Modern theme screenshot](https://github.com/user-attachments/assets/5767b4f8-0b72-4dad-afc1-47850b6349c4)

This package is made from a Ghidra theme file and external icon assets. It installs into the Ghidra user settings directory and does not modify Ghidra's application directory, jar files, or signed binaries.

## Contents

- `themes/vscode-dark-modern.theme`
- `images/vscode/codicons/`
- `install.ps1`
- `install.sh`
- `tools/` (icon mapping and generation scripts; not needed to install)

`images/vscode/codicons/` contains the PNG icons referenced by the theme through `[EXTERNAL]images/vscode/codicons/...`, plus the Codicons license files.

## Install (Recommended): Import One Theme File

The quickest, cross-platform way — no manual copying, no shell scripts:

1. Download [vscode-dark-modern.theme.zip from the latest release](https://github.com/pinksawtooth/VS_Code_dark_modern_theme/releases/latest/download/vscode-dark-modern.theme.zip) (also available under `dist/` in this repository).
2. In Ghidra, open `Edit` -> `Theme` -> `Import...`.
3. Select the downloaded `vscode-dark-modern.theme.zip`.

Ghidra extracts the bundled icons into your user settings directory and registers the theme in one step. Restart Ghidra if some UI parts do not update immediately.

This zip is a native Ghidra theme bundle (a `.theme` file plus its icons). Rebuild it after editing the theme with:

```sh
./tools/build-theme-zip.sh
```

The script installers below remain available if you prefer copying the files yourself.

## Install On Windows

For Windows and Ghidra 12.1.3 PUBLIC, run PowerShell from this repository directory:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

The installer copies the theme into:

```text
%APPDATA%\ghidra\ghidra_12.1.3_PUBLIC
```

Manual Windows installation:

```powershell
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.1.3_PUBLIC'

New-Item -ItemType Directory -Force -Path "$GhidraUserDir\themes" | Out-Null
New-Item -ItemType Directory -Force -Path "$GhidraUserDir\images\vscode\codicons" | Out-Null

Copy-Item .\themes\vscode-dark-modern.theme -Destination "$GhidraUserDir\themes\" -Force
Copy-Item .\images\vscode\codicons\* -Destination "$GhidraUserDir\images\vscode\codicons\" -Recurse -Force
```

If you use a different Ghidra version, replace `ghidra_12.1.3_PUBLIC` with your Ghidra user directory name.

To install into a custom Ghidra user settings directory:

```powershell
.\install.ps1 -GhidraUserDir '<Ghidra user settings directory>'
```

## Install On macOS Or Linux

On macOS, the installer defaults to:

```text
$HOME/Library/ghidra/ghidra_12.1.3_PUBLIC
```

On Linux, the installer defaults to:

```text
${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.3_PUBLIC
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
$GhidraUserDir = Join-Path $env:APPDATA 'ghidra\ghidra_12.1.3_PUBLIC'

Remove-Item "$GhidraUserDir\themes\vscode-dark-modern.theme" -Force
Remove-Item "$GhidraUserDir\images\vscode\codicons" -Recurse -Force
```

Restart Ghidra and choose another theme afterward.

## Uninstall On macOS Or Linux

Use the same Ghidra user settings directory that was used during installation.

macOS:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.1.3_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

Linux:

```sh
GHIDRA_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.3_PUBLIC"

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
- The theme definitions and bundled icons are checked against Ghidra 12.1.3 PUBLIC. GUI behavior has not been re-tested on every OS. It also covers the theme keys new in 12.1.x (debugger breakpoint timeline, split active/inactive docking tabs, byte viewer edit cursors) while keeping the older 12.0.x keys, preserving compatibility with Ghidra 12.0.4 and 12.1.2. Use the custom settings-directory option when installing on those versions.
- Colors follow the official VS Code Dark Modern palette: `#1F1F1F` editor, `#181818` chrome, `#2B2B2B` borders, `#313131` inputs, and `#0078D4` accent.
- Listing / Decompiler preserve syntax colors while selecting text, so code selections use a darker blue `#193549` and searches use dark amber fills. Ordinary text inputs retain `#264F78` selections. Changed bytes and debugger values use amber `#D7BA7D`; error text uses a lighter red `#F48771`, separately from red error icons. Addresses are brighter than line numbers.
- Function Graph uses green for fall-through, yellow for conditional jumps, and blue for unconditional jumps, sharing the Program Graph semantics. Highlighted paths are white. Bit-field cells use dark fills for readable labels.
- Panel headers use a flat background with white focused titles and muted inactive titles. Selected document tabs use white text, the close icon brightens on hover, and the tab-list button uses a downward chevron. Popup and supported window borders use subtle grays. Fonts, click targets and docking behavior retain their existing settings.
- Standard Swing tabs use FlatLaf's underline style. Ghidra's custom document tabs retain their own beveled borders; a theme cannot replace that renderer. Native title-bar integration also depends on the OS and application window code (see [FlatLaf window decorations](https://www.formdev.com/flatlaf/window-decorations/) and [macOS integration](https://www.formdev.com/flatlaf/macos/)).
- Generic actions use Codicons; Ghidra-specific concepts use companion icons with the same palette and 16px grid. `tools/icon-map.py` manages the mapping, and editable SVG sources for the companions live in `tools/custom-icons/`.
- External functions and thunks have distinct arrows; unions show overlapping storage and pointers an arrow into storage. Breakpoints use solid, outlined, half-filled and broken outlines to distinguish states, with a small exclamation overlay for inconsistencies. Graph directions and cycles, decompiler read-only/unreachable-code actions, and locked folders have dedicated shapes. The 16/24px application icons use simplified circuit traces.
- To regenerate the assets: `python3 tools/build-theme.py` rewrites the theme's `icon.*` lines and the render manifest, then `CODICONS_SRC=<codicons>/src/icons ./tools/generate-icons.sh` renders the PNGs from Codicons and companion SVG sources (requires ImageMagick 7 with SVG support). SVG sizing uses a 96 DPI baseline to render directly at the output dimensions.

## Building And Checking

The builder looks for Ghidra 12.0.4, 12.1.2 and 12.1.3 under `~/ghidra/`, with newer definitions taking precedence. For other locations, set `GHIDRA_DIRS` to the Ghidra installation directory (not its user settings directory). Separate multiple installations with `:` on macOS/Linux or `;` on Windows.

```sh
GHIDRA_DIRS="/path/to/ghidra_12.1.3_PUBLIC" python3 tools/build-theme.py
CODICONS_SRC="/path/to/codicons/package/src/icons" ./tools/generate-icons.sh
./tools/build-theme-zip.sh
python3 -m unittest discover -s tests -v
```

Use `@vscode/codicons` **0.0.45**, matching the bundled assets. The builder stops if it cannot read Ghidra icon definitions; the renderer checks all required Codicons and `tools/custom-icons/` SVG inputs and stages the rendered files before copying them into the asset directory.

The editor uses Java's logical `Monospaced` font on every OS. Active filters use an accent-colored icon. Version Tracking status icons preserve their individual cells, and progress frames use Ghidra's rotation modifiers; these modifiers survive theme regeneration.

With a JDK and a local Ghidra installation, run the integration check as well:

```sh
python3 tests/check_ghidra.py "/path/to/ghidra_12.1.3_PUBLIC"
```

It imports the ZIP using Ghidra's reader in a temporary settings directory, checks rendered status cells, animation frames, distinct companion shapes, breakpoint overlay placement and close-icon hover feedback, and writes `build/theme-check.png`, `build/icons-check.png`, `build/colors-check.png` and `build/windows-check.png` for visual inspection. These are offscreen samples, not live GUI screenshots. The window preview shows header color samples, Ghidra's actual tab-border renderer and standard Swing tabs; it does not test native title bars or drag/resize behavior.

Color tests require at least 4.5:1 for critical text/background pairs and a 3:1 regression floor for syntax-preserving selection/search backgrounds. The latter is a visibility safeguard, not a claim of accessibility compliance for the whole theme.
