# VS Code Dark Modern Theme for Ghidra

English | [日本語](README.ja.md)

A VS Code Dark Modern-inspired theme for Ghidra 12.0.4 PUBLIC.

![VS Code Dark Modern theme screenshot](assets/screenshot.png)

This package is made only from a Ghidra theme file and external icon assets. It does not modify Ghidra's application bundle, jar files, or signed binaries, so it is safe to install without affecting macOS code signing.

## Contents

- `themes/vscode-dark-modern.theme`
- `images/vscode/codicons/`
- `install.sh`

`images/vscode/codicons/` contains the PNG icons referenced by the theme through `[EXTERNAL]images/vscode/codicons/...`, plus the Codicons license files.

## Install

For macOS and Ghidra 12.0.4 PUBLIC:

```sh
git clone https://github.com/pinksawtooth/VS_Code_dark_modern_theme.git
cd VS_Code_dark_modern_theme
./install.sh
```

Manual installation:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC"

mkdir -p "$GHIDRA_USER_DIR/themes"
mkdir -p "$GHIDRA_USER_DIR/images/vscode/codicons"

cp themes/vscode-dark-modern.theme "$GHIDRA_USER_DIR/themes/"
cp -R images/vscode/codicons/. "$GHIDRA_USER_DIR/images/vscode/codicons/"
```

If you use a different Ghidra version, replace `ghidra_12.0.4_PUBLIC` with your own Ghidra user directory name.

You can also override the target directory when running the installer:

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC" ./install.sh
```

## Enable The Theme

1. Start or restart Ghidra.
2. Open `Edit` -> `Theme`.
3. Select `VS Code Dark Modern`.
4. Restart Ghidra if some UI parts do not update immediately.

## Update

Pull the latest version and run the installer again:

```sh
git pull
./install.sh
```

## Uninstall

```sh
GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC"

rm -f "$GHIDRA_USER_DIR/themes/vscode-dark-modern.theme"
rm -rf "$GHIDRA_USER_DIR/images/vscode/codicons"
```

Restart Ghidra and choose another theme afterward.

## Notes

- This theme intentionally stays within Ghidra's theme system.
- It does not modify Ghidra jars, app bundles, or signed files.
- It was tested with Ghidra 12.0.4 PUBLIC.
