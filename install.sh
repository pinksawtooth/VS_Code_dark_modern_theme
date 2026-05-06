#!/usr/bin/env sh
set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
GHIDRA_USER_DIR=${GHIDRA_USER_DIR:-"$HOME/Library/ghidra/ghidra_12.0.4_PUBLIC"}

mkdir -p "$GHIDRA_USER_DIR/themes"
mkdir -p "$GHIDRA_USER_DIR/images/vscode/codicons"

cp "$REPO_DIR/themes/vscode-dark-modern.theme" "$GHIDRA_USER_DIR/themes/"
cp -R "$REPO_DIR/images/vscode/codicons/." "$GHIDRA_USER_DIR/images/vscode/codicons/"

printf 'Installed VS Code Dark Modern theme to %s\n' "$GHIDRA_USER_DIR"
