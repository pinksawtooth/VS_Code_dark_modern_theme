# Ghidra-specific companion icons

These project-authored SVGs use the Codicons 16-unit grid, one-unit strokes,
transparent backgrounds and the theme's existing semantic colors. They add
Ghidra concepts for which a shared generic glyph loses useful information.

- Function variants: a cube with an outward arrow for external functions or
  a bent forwarding arrow for thunks.
- Types: overlapping storage for unions; an arrow into storage for pointers.
- Breakpoints: a broken outline means ineffective (one or more trace locations
  are absent), a half-filled circle means mixed, and a minus means disabled.
  The inconsistency exclamation sits outside the base dot as an overlay.
- Graph actions: incoming, outgoing, through, all paths, single/all cycles,
  and forward/reverse scoped flow each have a separate glyph.
- Decompiler actions: code plus a lock or an excluded line.
- Folders: separate open and closed silhouettes with a lock.
- Application: the 16/24px variant uses two contacts and fewer traces; larger
  sizes use the existing Codicons circuit-board artwork.

`tools/icon-map.py` chooses the asset and color. `tools/generate-icons.sh`
resolves `ghidra-*` stems here, and other stems in `CODICONS_SRC`. PNG outputs
stay in `images/vscode/codicons/` so the installers and Ghidra ZIP layout remain
compatible. Edit these SVG sources before regenerating the assets; do not edit
the PNGs directly. Upstream Codicons retain their bundled attribution and licenses.

Keep `stroke-opacity="1"` explicit: ImageMagick's internal SVG renderer otherwise
inherits a zero stroke opacity from its default `stroke="none"` context.
