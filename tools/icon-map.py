#!/usr/bin/env python3
"""Semantic icon mapping for the VS Code Dark Modern Ghidra theme.

This is the single source of truth that drives both:
  - tools/generate-icons.sh  (which codicon PNGs to render, and in what color)
  - tools/build-theme.py      (which icon.* keys map to which PNG)

The mapping is keyed by the ORIGINAL Ghidra default icon (its file basename),
so each Ghidra concept is paired with the codicon VS Code itself uses for the
same concept -- e.g. Ghidra's resume.png -> debug-continue, breakpoint-enable
-> a filled red breakpoint dot, version-tracking reject -> a red X.

Color suffixes on a PNG name select the render color (see generate-icons.sh):
  -success green | -error red | -warning yellow | -accent blue
  -disabled grey | -bp breakpoint-red | (none) neutral #CCCCCC
"""

# Normalized original-icon basename  ->  PNG asset name (codicon + color suffix).
# "Normalized" = path stripped, size/modifier brackets stripped, extension dropped.
SEMANTIC_MAP = {
    # ---- Generic actions --------------------------------------------------
    "add": "add", "Plus": "add", "Plus2": "add", "plus": "add",
    "list-remove": "remove", "Minus": "remove",
    "edit-delete": "trash", "delete": "trash", "table_delete": "trash",
    "trash-empty": "trash", "page_delete": "trash", "tag_blue_delete": "trash",
    "edit": "edit", "textfield_rename": "edit", "field.header": "edit",
    "edit-rename": "edit", "accessories-text-editor": "edit", "id": "edit",
    "pencil16": "edit", "door_open": "folder-opened",
    "copy": "copy", "page_white_copy": "copy", "DuplicateData": "copy",
    "MultiDuplicateData": "copy",
    "page_paste": "clippy", "paste": "clippy",
    "edit-cut": "screen-cut",
    "icon.save": "save", "disk": "save", "disk_save_as": "save-as",
    "edit-undo": "discard", "undo_hijack": "discard", "vcUndoCheckOut": "discard",
    "edit-redo": "redo",
    "view-refresh": "refresh", "reload3": "refresh", "computer": "refresh",
    "play_again": "refresh", "arrow_rotate_clockwise": "refresh",
    "edit-find": "search", "magnifier": "search", "default-query": "search",
    "preferences-web-browser-shortcuts": "search",
    "erase16": "close", "x": "close", "pinkX": "close", "dialog-cancel": "close",
    "process-stop": "close",
    "tick": "check", "check": "check", "accept": "check-success",
    "go-next": "check-success", "go-down": "check-success",
    "checkmark_green": "check-success", "flag_green": "check-success",
    "checkmark_yellow": "warning-warning",
    "list-add": "add",

    # ---- Navigation / arrows ---------------------------------------------
    "left": "arrow-left", "left.alternate": "arrow-left",
    "function_graph_flowchart_left": "arrow-left",
    "right": "arrow-right", "right.alternate": "arrow-right",
    "up": "arrow-up", "down": "arrow-down",
    "go-up": "arrow-up", "go-home": "home", "user-home": "home",
    "menu16": "chevron-down", "small_minus": "chevron-down", "small_plus": "chevron-right",
    "view-sort-ascending": "arrow-up", "view-sort-descending": "arrow-down",
    "sortascending": "arrow-up", "sortdescending": "arrow-down",
    "collapse_all": "collapse-all", "expand_all": "expand-all",
    "arrow_in": "collapse-all", "arrow_inout": "expand-all",
    "collapse": "chevron-up", "expand": "chevron-down",
    "2leftarrow": "arrow-left", "2rightarrow": "arrow-right",

    # ---- Debugger flow controls (VS Code debug toolbar) ------------------
    "resume": "debug-continue", "play": "debug-continue", "launch": "debug-start",
    "media-playback-start": "debug-continue",
    "resumeback": "debug-reverse-continue",
    "interrupt": "debug-pause",
    "kill": "debug-stop", "red_can": "debug-stop", "media-playback-stop": "debug-stop",
    "stepinto": "debug-step-into", "stepover": "debug-step-over",
    "stepout": "debug-step-out", "skipover": "debug-step-over",
    "stepback": "debug-step-back", "stepbackinto": "debug-step-back",
    "steplast": "debug-step-back",
    "connect": "plug", "connect-accept": "plug",
    "connect-outbound": "plug", "attach": "plug",
    "disconnect": "debug-disconnect", "disconnected": "debug-disconnect",
    "interrupt.png": "debug-pause",
    "record": "record", "katomic": "debug-continue",
    "debugger": "debug-alt", "debugger32": "debug-alt", "conf": "settings-gear",
    "autoread": "debug-alt", "seek-present": "debug-alt", "overlay-tx": "debug-alt",
    "system-switch-user": "debug-alt", "write-emulator": "debug-alt",
    "edit-bomb": "debug-alt", "cursor_arrow": "debug-alt",
    "skipover.png": "debug-step-over",

    # ---- Breakpoints (VS Code: filled dot = set, hollow = disabled) ------
    "breakpoint-enable": "circle-filled-bp", "breakpoints-enable-all": "circle-filled-bp",
    "breakpoint-enable-ineff": "circle-disabled",
    "breakpoint-disable": "circle-disabled", "breakpoints-disable-all": "circle-disabled",
    "breakpoint-disable-ineff": "circle-disabled",
    "breakpoint-clear": "close", "breakpoints-clear-all": "trash",
    "breakpoint-mixed": "debug-breakpoint-conditional-error",
    "breakpoint-mixed-ineff": "debug-breakpoint-unsupported",
    "breakpoint-overlay-inconsistent": "debug-breakpoint-unsupported",
    "breakpoints-make-effective": "debug-breakpoint-function-error",
    "disabledCode": "circle-disabled",

    # ---- Process / thread / register / memory ----------------------------
    "process": "debug-alt-accent", "process.png": "debug-alt-accent",
    "thread": "debug-alt-accent", "record.png": "record-accent",
    "write-target": "debug-alt-accent", "write-trace": "record-accent",
    "registers": "chip", "registerIcon": "symbol-variable",
    "registerGroup": "chip", "register-marker": "chip",
    "select-registers": "chip", "modules": "chip",
    "memory16": "chip", "table-s": "chip",
    "stack": "debug-stackframe", "StackFrame_Red": "debug-stackframe",
    "StackFrameElement": "debug-stackframe",
    "object-running": "debug-continue-success", "object-populated": "debug-alt",
    "object-terminated": "debug-alt", "object-unpopulated": "circle",

    # ---- Step / breakpoint timeline (12.1) -------------------------------
    "color_swatch": "symbol-color", "zoom_in": "zoom-in", "zoom_out": "zoom-out",
    "zoom": "screen-normal", "viewmagfit": "screen-full",

    # ---- View / layout / graph -------------------------------------------
    "graph_view": "graph", "fullscreen_view": "graph",
    "network-wireless": "broadcast", "network-wireless-16": "broadcast",
    "view-fullscreen": "screen-full",
    "verticalSplit": "split-horizontal", "view_top_bottom": "split-horizontal",
    "view_left_right": "split-vertical", "view_bottom": "split-horizontal",
    "function_graph": "type-hierarchy", "function_graph_code_flow": "type-hierarchy",
    "function_graph_flowchart": "type-hierarchy", "function_graph_curvey": "type-hierarchy",
    "fgin": "type-hierarchy", "fgout": "type-hierarchy", "fginout": "type-hierarchy",
    "fgloop": "type-hierarchy", "fgloopall": "type-hierarchy", "fgpaths": "type-hierarchy",
    "fgrevblock": "type-hierarchy", "fgblock": "arrow-right",
    "graph.layout.default": "layout", "color_swatch.png": "symbol-color",
    "house": "home", "Lasso": "list-selection",

    # ---- Filters / lightbulb / sort --------------------------------------
    "filter_off": "filter", "filter_on": "filter", "filter_matched": "filter",
    "FilterArrays": "filter", "FilterPointers": "filter", "view-filter": "filter",
    "lightbulb": "lightbulb", "lightbulb_off": "lightbulb",

    # ---- Bookmarks / flags / markers -------------------------------------
    "applications-system": "bookmark", "B.gif": "bookmark", "unknown": "bookmark",
    "flag": "flag-accent", "searchm_obj": "search", "searchm_pink": "search",
    "MarkSelection": "flag-accent", "make.selection": "list-selection",
    "notes": "note", "wand": "sparkle",

    # ---- Eyes / hover / pin ----------------------------------------------
    "hoverOff": "eye-closed-disabled", "hoverOn": "eye-accent",
    "pin": "pin", "icon.base.pinned": "pinned",

    # ---- Locks / security / users ----------------------------------------
    "lock": "lock", "unlock": "unlock", "kgpg": "lock", "key": "key",
    "preferences-desktop-user-password": "key",
    "user": "account", "user-busy": "account", "user-online": "account",
    "system-users": "organization",

    # ---- Links / references ----------------------------------------------
    "link": "link", "icon_link": "link", "brick_link": "link",
    "references_to": "references", "ExternalData": "references",
    "tag_yellow": "references",

    # ---- Console / terminal / time / help --------------------------------
    "console": "debug-console", "time": "history", "history": "history",
    "hourglass": "loading", "help-browser": "question", "help-hint": "lightbulb",
    "question_zero": "question", "redQuestionMark": "question-warning",
    "plugin": "plug", "package": "package",

    # ---- Paint / color ----------------------------------------------------
    "paintbrush": "paintcan", "palette": "symbol-color", "font": "text-size",

    # ---- Camera / drive / monitor ----------------------------------------
    "camera-photo": "device-camera", "video-x-generic16": "device-camera-video",
    "drive": "vm", "monitor": "vm", "desktop": "vm",
    "server": "server", "database": "database",

    # ---- Data types -------------------------------------------------------
    "cstruct": "symbol-structure", "defaultDt": "symbol-structure",
    "typedef": "symbol-interface", "enum": "symbol-enum", "cUnion": "symbol-structure",
    "Array": "symbol-array", "BookShelf": "library", "BookShelfOpen": "library",
    "functionDef": "symbol-method", "F": "symbol-method", "FunctionScope": "symbol-method",
    "ExternalFunction": "symbol-method", "ThunkFunction.dark": "symbol-method",
    "LocalVariable": "symbol-variable", "Parameter": "symbol-parameter",
    "Namespace.dark": "symbol-namespace", "class": "symbol-class",
    "L": "symbol-key", "label": "symbol-key",
    "I": "info-accent", "D": "symbol-misc", "U": "symbol-misc", "V": "symbol-misc",
    "text_lowercase": "symbol-string",
    "emblem-favorite": "star-full",

    # ---- Version control / tracking --------------------------------------
    "vcAdd": "add", "vcCheckIn": "arrow-up", "vcCheckOut": "arrow-down",
    "Merge": "git-merge", "vcMerge": "git-merge", "sync_enabled": "git-compare",
    "VCRFastForward": "debug-step-over",
    "Plus.png": "add", "start-here_16": "rocket",
    "undo-apply": "discard", "changed16": "diff",
    "application_view_detail": "list-flat",
    "table_relationship": "git-compare", "table_go": "references",

    # ---- Status (merge / conflict) ---------------------------------------
    "conflictKeep": "error-error", "conflictReplace": "error-error",
    "conflictRename": "edit", "conflictReplaceOrRename": "edit",
    "emblem-important": "error-error", "info_small_hover": "info-accent",
    "info_small": "info-accent", "information": "info-accent", "notes.gif": "note",
    "green_can": "check-success", "carry": "check-success",
    "onesComplement": "check-success", "twosComplement": "check-success",
    "xor": "symbol-operator",

    # ---- Files: source/binary/media/archive ------------------------------
    "binaryData": "file-binary-accent", "hexData": "file-binary-accent",
    "program_obj": "file-binary-accent", "settings16": "settings-gear",
    "wrench": "tools", "document-properties": "settings-gear",

    # ---- Misc / tables ----------------------------------------------------
    "table": "table", "info_small.png": "table",
    "eliminateUnreachable": "list-tree", "decompileFunction": "list-tree",
    "sitemap_color": "list-tree", "plasma": "list-tree", "readOnly": "list-tree",
    "icon.search": "search", "icon.home": "home", "icon.warning": "warning-warning",
    "exec": "play", "function": "symbol-method", "icon.run": "play",
    "gate-set": "symbol-misc",

    # ---- Progress / busy frames ------------------------------------------
    "hourglass24_01": "loading", "hourglass24_02": "loading", "hourglass24_03": "loading",
    "hourglass24_04": "loading", "hourglass24_05": "loading", "hourglass24_06": "loading",
    "hourglass24_07": "loading", "hourglass24_08": "loading", "hourglass24_09": "loading",
    "hourglass24_10": "loading", "hourglass24_11": "loading",
    "eatbits1": "loading", "eatbits2": "loading", "eatbits3": "loading",
    "eatbits4": "loading", "eatbits5": "loading", "eatbits6": "loading",
    "eatbits7": "loading", "eatbits8": "loading",

    # ---- Folder corrections ----------------------------------------------
    "closedSmallFolder": "folder", "openSmallFolder": "folder-opened",
    "closedDescendantsInView": "folder", "disabledClosedFolder": "folder",
    "phone": "device-mobile",
}

# Per-key overrides win over SEMANTIC_MAP, for the few keys whose shared default
# icon should differ by context.
KEY_OVERRIDES = {
    # Main toolbar undo/redo. Ghidra's default is EMPTY_ICON{oxygen-edit-redo
    # [mirror]} for undo and the same glyph un-mirrored for redo; since both
    # share one source bitmap, only an explicit override can give undo its own
    # (left-curving) glyph.
    "icon.undo": "discard",
    "icon.redo": "redo",
    "icon.toggle.collapse": "chevron-up",
    "icon.toggle.expand": "chevron-down",
    "icon.left": "arrow-left",
    "icon.right": "arrow-right",
    "icon.up": "arrow-up",
    "icon.down": "arrow-down",
    "icon.home": "home",
    "icon.search": "search",
    "icon.zoom.in": "zoom-in",
    "icon.zoom.out": "zoom-out",
    "icon.help": "question",
    "icon.font": "text-size",
    "icon.navigate.in": "arrow-right",
    "icon.navigate.out": "arrow-left",
    "icon.make.selection": "list-selection",
    "icon.plugin.calltree.function": "type-hierarchy",
    "icon.plugin.calltree.recursive": "sync",
    "icon.debugger.provider.regions": "chip",
    "icon.debugger.provider.modules": "chip",
    "icon.debugger.map.modules": "chip",
    "icon.debugger.map.sections": "chip",
    "icon.debugger.map.regions": "chip",
    "icon.debugger.provider.time": "history",
    "icon.debugger.diff.next": "arrow-down",
    "icon.debugger.diff.previous": "arrow-up",
    "icon.plugin.composite.editor.move.down": "arrow-down",
    "icon.plugin.composite.editor.move.up": "arrow-up",
    "icon.plugin.datatypes.enum": "symbol-enum",
    "icon.plugin.datatypes.structure": "symbol-structure",
    "icon.plugin.datatypes.union": "symbol-structure",
    "icon.plugin.datatypes.typedef": "symbol-interface",
    "icon.plugin.datatypes.pointer": "symbol-numeric",
    "icon.plugin.datatypes.function": "symbol-method",
    "icon.run": "play",
}

if __name__ == "__main__":
    # quick self-check
    vals = set(SEMANTIC_MAP.values()) | set(KEY_OVERRIDES.values())
    print(f"{len(SEMANTIC_MAP)} semantic entries, {len(KEY_OVERRIDES)} key overrides")
    print(f"{len(vals)} distinct PNG assets referenced")
