#!/usr/bin/env sh
set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ "${GHIDRA_USER_DIR:-}" = "" ]; then
	case "$(uname -s)" in
		Darwin*)
			GHIDRA_USER_DIR="$HOME/Library/ghidra/ghidra_12.1.2_PUBLIC"
			;;
		Linux*)
			GHIDRA_USER_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/ghidra/ghidra_12.1.2_PUBLIC"
			;;
		*)
			printf 'Set GHIDRA_USER_DIR to your Ghidra user settings directory.\n' >&2
			exit 1
			;;
	esac
fi

mkdir -p "$GHIDRA_USER_DIR/themes"
mkdir -p "$GHIDRA_USER_DIR/images/vscode/codicons"

cp "$REPO_DIR/themes/vscode-dark-modern.theme" "$GHIDRA_USER_DIR/themes/"
cp -R "$REPO_DIR/images/vscode/codicons/." "$GHIDRA_USER_DIR/images/vscode/codicons/"

printf 'Installed VS Code Dark Modern theme to %s\n' "$GHIDRA_USER_DIR"
