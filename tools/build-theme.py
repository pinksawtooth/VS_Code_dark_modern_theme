#!/usr/bin/env python3
"""Rebuild the icon.* block of the theme + the codicon render manifest.

Pipeline:
  1. Parse every Ghidra *.theme.properties (12.0.4 + 12.1.2) to learn the
     default icon each icon.* key resolves to.
  2. Map each key to a codicon PNG via tools/icon-map.py (by original icon
     basename), falling back to the current theme's choice so coverage never
     regresses.
  3. Emit:
       - build/icon-manifest.tsv : <png>\t<svg-stem>\t<color>  (for the renderer)
       - rewrites themes/vscode-dark-modern.theme icon.* lines in place.

Run from the repo root:  python3 tools/build-theme.py
Environment:
  GHIDRA_DIRS   : colon-separated Ghidra install dirs (default: the two known)
"""
import os
import re
import sys
import glob
import importlib.util

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(REPO, "themes", "vscode-dark-modern.theme")
CODICON_DIR = "images/vscode/codicons"

# --- load icon-map.py -------------------------------------------------------
spec = importlib.util.spec_from_file_location("icon_map", os.path.join(REPO, "tools", "icon-map.py"))
icon_map = importlib.util.module_from_spec(spec)
spec.loader.exec_module(icon_map)
SEMANTIC_MAP = icon_map.SEMANTIC_MAP
KEY_OVERRIDES = icon_map.KEY_OVERRIDES

# Color suffix -> render color. Stem is the PNG name minus a trailing suffix.
COLOR_SUFFIX = {
    "success": "#89D185", "error": "#F14C4C", "warning": "#CCA700",
    "accent": "#3794FF", "disabled": "#6A6A6A", "bp": "#E51400",
}
NEUTRAL = "#CCCCCC"


def split_color(png_stem):
    """'circle-disabled' -> ('circle', '#6A6A6A'); 'add' -> ('add', NEUTRAL)."""
    parts = png_stem.rsplit("-", 1)
    if len(parts) == 2 and parts[1] in COLOR_SUFFIX:
        return parts[0], COLOR_SUFFIX[parts[1]]
    return png_stem, NEUTRAL


def ghidra_dirs():
    env = os.environ.get("GHIDRA_DIRS")
    if env:
        return env.split(":")
    home = os.path.expanduser("~")
    cands = [
        "/Users/samsepi0l/ghidra/ghidra_12.0.4_PUBLIC",
        "/Users/samsepi0l/ghidra/ghidra_12.1.2_PUBLIC",
    ]
    return [d for d in cands if os.path.isdir(d)]


def load_defaults():
    """key -> raw default icon value (last version wins)."""
    defaults = {}
    for d in ghidra_dirs():
        for f in glob.glob(os.path.join(d, "**", "*.theme.properties"), recursive=True):
            with open(f, errors="replace") as fh:
                for line in fh:
                    line = line.strip()
                    m = re.match(r"^(icon\.[^=\s]+)\s*=\s*(.+?)\s*(?://.*)?$", line)
                    if m:
                        defaults[m.group(1)] = m.group(2).strip()
    return defaults


def norm_basename(value):
    """Reduce a raw icon value to a normalized basename for SEMANTIC_MAP lookup."""
    head = value.split("{")[0].strip()
    head = re.sub(r"(\[[^\]]*\]\s*)+$", "", head).strip()
    # For an EMPTY_ICON canvas with an overlay (e.g. the undo/redo buttons are
    # EMPTY_ICON{oxygen-edit-redo.png...}), the meaningful glyph is the first
    # overlay inside the braces, not the empty canvas.
    if head in ("", "EMPTY_ICON") and "{" in value:
        inner = value.split("{", 1)[1]
        inner = inner.split("}", 1)[0].strip()
        value = inner if inner else head
    else:
        value = head
    # strip trailing [..] modifiers (possibly several)
    value = re.sub(r"(\[[^\]]*\]\s*)+$", "", value).strip()
    base = value.rsplit("/", 1)[-1]
    base = re.sub(r"\.(png|gif|jpg|jpeg)$", "", base, flags=re.I)
    return base


def resolve_default(key, defaults, seen=None):
    """Follow icon-reference chains (value that is itself an icon.* key)."""
    if seen is None:
        seen = set()
    if key in seen or key not in defaults:
        return None
    seen.add(key)
    val = defaults[key]
    head = val.split("{")[0].strip()
    head = re.sub(r"(\[[^\]]*\]\s*)+$", "", head).strip()
    if head.startswith("icon."):
        return resolve_default(head, defaults, seen)
    return val


def load_current_theme_map():
    """key -> current png name, from the theme on disk (fallback source)."""
    cur = {}
    for line in open(THEME):
        m = re.match(r"^(icon\.[^=\s]+)\s*=\s*\[EXTERNAL\]images/vscode/codicons/(.+)\.png\s*$", line.strip())
        if m:
            cur[m.group(1)] = m.group(2)
    return cur


def main():
    defaults = load_defaults()
    current = load_current_theme_map()

    # All icon.* keys we should emit = union of keys present in current theme
    # and keys defined by Ghidra (so new keys get covered too).
    keys = set(current) | set(k for k in defaults if k.startswith("icon."))

    png_for = {}
    stats = {"override": 0, "semantic": 0, "fallback": 0, "empty": 0}
    unmapped = []
    for key in keys:
        raw = defaults.get(key, "")
        # Preserve special non-codicon values (EMPTY_ICON etc.) only if we have
        # no current override; our theme historically replaces them, so prefer
        # an explicit mapping.
        if key in KEY_OVERRIDES:
            png_for[key] = KEY_OVERRIDES[key]; stats["override"] += 1; continue
        resolved = resolve_default(key, defaults) or raw
        base = norm_basename(resolved)
        if base in SEMANTIC_MAP:
            png_for[key] = SEMANTIC_MAP[base]; stats["semantic"] += 1; continue
        # also try the full key as a semantic alias (e.g. "icon.search")
        if key in SEMANTIC_MAP:
            png_for[key] = SEMANTIC_MAP[key]; stats["semantic"] += 1; continue
        if key in current:
            png_for[key] = current[key]; stats["fallback"] += 1
            if base not in ("blank",) and resolved:
                unmapped.append((key, base, current[key]))
        else:
            stats["empty"] += 1
    # Keep EMPTY icons truly empty
    for key in list(png_for):
        if defaults.get(key, "").startswith("EMPTY_ICON") and key not in KEY_OVERRIDES \
           and norm_basename(resolve_default(key, defaults) or "") not in SEMANTIC_MAP:
            png_for[key] = "blank"

    # --- write manifest -----------------------------------------------------
    assets = sorted(set(png_for.values()))
    os.makedirs(os.path.join(REPO, "build"), exist_ok=True)
    manifest = os.path.join(REPO, "build", "icon-manifest.tsv")
    with open(manifest, "w") as out:
        for png in assets:
            stem, color = split_color(png)
            out.write(f"{png}\t{stem}\t{color}\n")

    # --- rewrite theme icon lines ------------------------------------------
    lines = open(THEME).read().splitlines(keepends=True)
    out_lines, written, seen_keys = [], set(), set()
    icon_line = re.compile(r"^(icon\.[^=\s]+)\s*=")
    # Build the canonical icon block text once, sorted, to drop in place of the
    # first contiguous icon.* run. We replace each existing icon line with its
    # new value and drop the rest, then append any brand-new keys after the run.
    new_value = {k: f"[EXTERNAL]{CODICON_DIR}/{png_for[k]}.png" for k in png_for}

    in_block = False
    for line in lines:
        m = icon_line.match(line.strip())
        if m:
            key = m.group(1)
            in_block = True
            if key in new_value and key not in seen_keys:
                out_lines.append(f"{key} = {new_value[key]}\n")
                seen_keys.add(key)
            # drop duplicate/again-listed icon lines
            continue
        else:
            if in_block:
                # we just exited the first icon run; flush any unseen keys here
                missing = sorted(k for k in new_value if k not in seen_keys)
                for k in missing:
                    out_lines.append(f"{k} = {new_value[k]}\n")
                    seen_keys.add(k)
                in_block = False
            out_lines.append(line)
    if in_block:  # file ended within the block
        for k in sorted(k for k in new_value if k not in seen_keys):
            out_lines.append(f"{k} = {new_value[k]}\n")
            seen_keys.add(k)

    with open(THEME, "w") as fh:
        fh.writelines(out_lines)

    print(f"keys emitted: {len(png_for)}  assets: {len(assets)}")
    print(f"  stats: {stats}")
    if unmapped:
        print(f"  {len(unmapped)} keys used fallback (no semantic entry). Sample:")
        for key, base, png in unmapped[:25]:
            print(f"    {key:55s} default={base:30s} -> {png}")
    print(f"manifest: {manifest}")


if __name__ == "__main__":
    main()
