#!/usr/bin/env sh
# Render images/vscode/codicons/*.png from the @vscode/codicons SVG sources,
# driven by build/icon-manifest.tsv (produced by tools/build-theme.py).
#
# Usage:
#   python3 tools/build-theme.py            # refresh the manifest + theme
#   CODICONS_SRC=/path/to/codicons/package/src/icons ./tools/generate-icons.sh
#
# Requires ImageMagick 7 (magick) with SVG support. Icons are
# rendered natively at the target pixel size (no upscaling), which keeps the
# half-pixel stroke grid of codicons crisp at 16x16.
set -eu
export LC_ALL=C

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
OUT_DIR="$REPO_DIR/images/vscode/codicons"
MANIFEST="$REPO_DIR/build/icon-manifest.tsv"
SRC_DIR="${CODICONS_SRC:?Set CODICONS_SRC to the codicons package src/icons directory}"
CUSTOM_DIR="$REPO_DIR/tools/custom-icons"
[ -f "$MANIFEST" ] || { echo "Missing $MANIFEST. Run: python3 tools/build-theme.py" >&2; exit 1; }
[ -d "$SRC_DIR" ] || { echo "Missing Codicons source directory: $SRC_DIR" >&2; exit 1; }
command -v magick >/dev/null 2>&1 || { echo "ImageMagick 7 (magick) is required" >&2; exit 1; }

source_svg() {
	case "$1" in
		ghidra-*) printf '%s/%s.svg\n' "$CUSTOM_DIR" "$1" ;;
		*) printf '%s/%s.svg\n' "$SRC_DIR" "$1" ;;
	esac
}

# Check every input before rendering so missing SVGs cannot silently leave
# stale PNGs in a successful build.
[ -f "$SRC_DIR/circuit-board.svg" ] || { echo "Missing SVG: circuit-board" >&2; exit 1; }
[ -f "$CUSTOM_DIR/ghidra-application-small.svg" ] || { echo "Missing SVG: ghidra-application-small" >&2; exit 1; }
while IFS="$(printf '\t')" read -r png stem color; do
	case "$png" in ''|blank|circuit-board-accent*) continue ;; esac
	[ -f "$(source_svg "$stem")" ] || { echo "Missing SVG: $stem (for $png.png)" >&2; exit 1; }
done < "$MANIFEST"

TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/codicons.XXXXXX")
TMP_SVG="$TMP_DIR/icon.svg"
RENDER_DIR="$TMP_DIR/rendered"
mkdir -p "$RENDER_DIR"
trap 'rm -rf "$TMP_DIR"' 0
trap 'exit 1' HUP INT TERM

render() { # render <svg-stem> <#color> <size> <out-file>
	_stem=$1 _color=$2 _size=$3 _out=$4
	sed "s/currentColor/$_color/g; s/fill=\"black\"/fill=\"$_color\"/g" \
		"$(source_svg "$_stem")" > "$TMP_SVG"
	# SVG CSS pixels use 96 DPI. At 72 DPI ImageMagick draws a 16px SVG at
	# 12px, then blurs it when resizing back to 16px.
	_density=$(awk "BEGIN { printf \"%.4f\", 96 * $_size / 16 }")
	magick -background none -density "$_density" "$TMP_SVG" \
		-resize "${_size}x${_size}!" -strip "PNG32:$_out"
}

echo "Rendering 16x16 codicons from manifest..."
count=0
while IFS="$(printf '\t')" read -r png stem color; do
	[ -n "$png" ] || continue
	case "$png" in
		blank) magick -size 16x16 xc:none -strip "PNG32:$RENDER_DIR/blank.png"; count=$((count + 1)); continue ;;
		circuit-board-accent*) continue ;; # app icons rendered below
	esac
	render "$stem" "$color" 16 "$RENDER_DIR/$png.png"
	count=$((count + 1))
done < "$MANIFEST"
echo "  rendered $count glyphs"

echo "Rendering application icons (blue tile + white circuit-board glyph)..."
TILE='#0078D4' # VS Code Dark Modern accent / button.background
for size in 16 24 32 40 48 64 128 256; do
	if [ "$size" -le 24 ]; then
		if [ "$size" -eq 16 ]; then
			out="$RENDER_DIR/circuit-board-accent.png"
		else
			out="$RENDER_DIR/circuit-board-accent-$size.png"
		fi
		render ghidra-application-small '#FFFFFF' "$size" "$out"
		continue
	fi
	radius=$(awk "BEGIN { printf \"%d\", $size * 0.22 }")
	glyph=$(awk "BEGIN { g = int($size * 0.72); print (g % 2) ? g + 1 : g }")
	render circuit-board '#FFFFFF' "$glyph" "$TMP_DIR/circuit_glyph.png"
	if [ "$size" -eq 16 ]; then
		out="$RENDER_DIR/circuit-board-accent.png"
	else
		out="$RENDER_DIR/circuit-board-accent-$size.png"
	fi
	magick -size "${size}x${size}" xc:none -fill "$TILE" \
		-draw "roundrectangle 0,0,$((size - 1)),$((size - 1)),$radius,$radius" \
		"$TMP_DIR/circuit_glyph.png" -gravity center -composite -strip "PNG32:$out"
done
mkdir -p "$OUT_DIR"
cp "$RENDER_DIR/"*.png "$OUT_DIR/"
echo "Done. Output: $OUT_DIR"
