#!/usr/bin/env sh
# Render images/vscode/codicons/*.png from the @vscode/codicons SVG sources,
# driven by build/icon-manifest.tsv (produced by tools/build-theme.py).
#
# Usage:
#   python3 tools/build-theme.py            # refresh the manifest + theme
#   CODICONS_SRC=/path/to/codicons/package/src/icons ./tools/generate-icons.sh
#
# Requires ImageMagick 7 (magick) built with librsvg SVG support. Icons are
# rendered natively at the target pixel size (no upscaling), which keeps the
# half-pixel stroke grid of codicons crisp at 16x16.
set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
OUT_DIR="$REPO_DIR/images/vscode/codicons"
MANIFEST="$REPO_DIR/build/icon-manifest.tsv"
SRC_DIR="${CODICONS_SRC:?Set CODICONS_SRC to the codicons package src/icons directory}"
[ -f "$MANIFEST" ] || { echo "Missing $MANIFEST. Run: python3 tools/build-theme.py" >&2; exit 1; }
TMP_SVG=$(mktemp /tmp/codicon.XXXXXX.svg)
trap 'rm -f "$TMP_SVG"' EXIT

render() { # render <svg-stem> <#color> <size> <out-file>
	_stem=$1 _color=$2 _size=$3 _out=$4
	sed "s/currentColor/$_color/g; s/fill=\"black\"/fill=\"$_color\"/g" \
		"$SRC_DIR/$_stem.svg" > "$TMP_SVG"
	_density=$(awk "BEGIN { printf \"%.4f\", 72 * $_size / 16 }")
	magick -background none -density "$_density" "$TMP_SVG" \
		-resize "${_size}x${_size}!" "PNG32:$_out"
}

echo "Rendering 16x16 codicons from manifest..."
count=0
while IFS="$(printf '\t')" read -r png stem color; do
	[ -n "$png" ] || continue
	case "$png" in
		blank) magick -size 16x16 xc:none "PNG32:$OUT_DIR/blank.png"; count=$((count + 1)); continue ;;
		circuit-board-accent*) continue ;; # app icons rendered below
	esac
	[ -f "$SRC_DIR/$stem.svg" ] || { echo "  WARN missing svg: $stem (for $png.png)" >&2; continue; }
	render "$stem" "$color" 16 "$OUT_DIR/$png.png"
	count=$((count + 1))
done < "$MANIFEST"
echo "  rendered $count glyphs"

echo "Rendering application icons (blue tile + white circuit-board glyph)..."
TILE='#0078D4' # VS Code Dark Modern accent / button.background
for size in 16 24 32 40 48 64 128 256; do
	radius=$(awk "BEGIN { printf \"%d\", $size * 0.22 }")
	glyph=$(awk "BEGIN { g = int($size * 0.72); print (g % 2) ? g + 1 : g }")
	render circuit-board '#FFFFFF' "$glyph" /tmp/circuit_glyph.png
	if [ "$size" -eq 16 ]; then
		out="$OUT_DIR/circuit-board-accent.png"
	else
		out="$OUT_DIR/circuit-board-accent-$size.png"
	fi
	magick -size "${size}x${size}" xc:none -fill "$TILE" \
		-draw "roundrectangle 0,0,$((size - 1)),$((size - 1)),$radius,$radius" \
		/tmp/circuit_glyph.png -gravity center -composite "PNG32:$out"
done
rm -f /tmp/circuit_glyph.png
echo "Done. Output: $OUT_DIR"
