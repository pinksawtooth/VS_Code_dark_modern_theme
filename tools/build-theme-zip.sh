#!/usr/bin/env sh
# Build a Ghidra-importable theme bundle: dist/vscode-dark-modern.theme.zip
#
# Ghidra's "Edit -> Theme -> Import..." accepts a *.theme.zip that contains the
# .theme file plus its [EXTERNAL] icons under images/. On import Ghidra copies
# the icons into the user settings directory and registers the theme (see
# generic.theme.ThemeReader#readZipTheme / docking.theme.gui.ThemeUtils). This
# gives a one-file install with no manual copying.
#
# Constraint enforced by Ghidra: every zip entry must either end in ".theme" or
# contain "images/" in its path (ThemeReader.processIconFile throws otherwise),
# so the bundle contains ONLY the theme file and the images/ tree.
set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
OUT_DIR="$REPO_DIR/dist"
ZIP="$OUT_DIR/vscode-dark-modern.theme.zip"
THEME="themes/vscode-dark-modern.theme"
ICON_DIR="images/vscode/codicons"

cd "$REPO_DIR"
[ -f "$THEME" ] || { echo "Missing $THEME" >&2; exit 1; }
[ -d "$ICON_DIR" ] || { echo "Missing $ICON_DIR" >&2; exit 1; }

mkdir -p "$OUT_DIR"
rm -f "$ZIP"

# Stage the exact layout Ghidra expects: <name>.theme at the root + images/...
STAGE=$(mktemp -d /tmp/themezip.XXXXXX)
trap 'rm -rf "$STAGE"' EXIT
cp "$THEME" "$STAGE/vscode-dark-modern.theme"
mkdir -p "$STAGE/images/vscode/codicons"
cp -R "$ICON_DIR/." "$STAGE/images/vscode/codicons/"

# Two constraints, both learned from how ThemeReader.readZipTheme() works:
#   * -D : NO directory entries. Every non-".theme" entry is fed to
#          processIconFile(), which copies it as a file; a bare "images/"
#          directory entry makes it throw "images: Is a directory" and the whole
#          import fails.
#   * order: the .theme is parsed the moment it is seen, resolving each
#          [EXTERNAL] icon against the user dir right then, so the icon files
#          must be added (hence extracted) BEFORE the .theme entry.
( cd "$STAGE" && zip -DqX "$ZIP" images/vscode/codicons/* && zip -DqX "$ZIP" vscode-dark-modern.theme )

echo "Built $ZIP"
echo "Entries:"
unzip -l "$ZIP" | awk 'NR>3 && $4 != "" {print "  " $4}' | head -8
echo "  ... ($(unzip -l "$ZIP" | tail -1 | awk '{print $2}') entries total)"
echo
echo "Install in Ghidra:  Edit -> Theme -> Import...  ->  select this file"
