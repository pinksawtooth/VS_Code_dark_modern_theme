"""Offline regression checks: python3 -m unittest discover -s tests -v."""
import importlib.util
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "themes/vscode-dark-modern.theme"
spec = importlib.util.spec_from_file_location("build_theme", ROOT / "tools/build-theme.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def values(text):
    return dict(re.findall(r"^([^#\s][^=]*?)\s*=\s*(.*?)\s*$", text, re.M))


def asset(value):
    return re.match(r"\[EXTERNAL\](.*?\.png)", value).group(1)


def resolved_color(theme, key):
    while not key.startswith("#"):
        key = theme[key]
    return tuple(int(key[i:i + 2], 16) / 255 for i in (1, 3, 5))


def contrast(theme, fg, bg):
    def luminance(rgb):
        linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return sum(c * w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))
    a, b = sorted(luminance(resolved_color(theme, key)) for key in (fg, bg))
    return (b + 0.05) / (a + 0.05)


class ThemeTests(unittest.TestCase):
    def setUp(self):
        self.text = THEME.read_text()
        self.theme = values(self.text)

    def test_references_and_assets(self):
        keys = re.findall(r"^([^#\s][^=]*?)\s*=", self.text, re.M)
        self.assertEqual(len(keys), len(set(keys)), "Duplicate theme keys")
        for key, value in self.theme.items():
            if value.startswith("[EXTERNAL]"):
                png = (ROOT / asset(value)).read_bytes()
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n", key)
                self.assertTrue(all(struct.unpack(">II", png[16:24])), key)
            if value.startswith(("color.", "font.")):
                seen = {key}
                while value.startswith(("color.", "font.")):
                    ref = value.split("[", 1)[0]
                    self.assertIn(ref, self.theme, key)
                    self.assertNotIn(ref, seen, key)
                    seen.add(ref)
                    value = self.theme[ref]

    def test_portable_monospaced_editor(self):
        self.assertEqual(self.theme["font.vscode.editor"], "Monospaced-plain-13")
        for key in ("font.listing.base", "font.decompiler", "font.byteviewer"):
            self.assertEqual(self.theme[key], "font.monospaced")

    def test_critical_text_contrast(self):
        pairs = [
            ("color.fg.listing.address", "color.bg.listing"),
            ("color.fg.byteviewer.changed", "color.bg.byteviewer"),
            ("color.fg.byteviewer.changed", "color.bg.selection"),
            ("color.fg.plugin.functiongraph.label.non.picked", "color.bg.plugin.functiongraph"),
            ("color.fg.dialog.status.error", "color.bg"),
            ("color.fg.plugin.function.editor.dialog.textfield.error", "[laf.color]TextField.background"),
        ]
        for fg in ("color.fg.debugger.value.changed.selected", "color.fg.debugger.plugin.objects.error",
                   "color.debugger.plugin.resources.value.changed.selected", "color.fg.table.uneditable.selected"):
            for bg in ("[laf.color]Table.selectionBackground", "[laf.color]Table.selectionInactiveBackground"):
                pairs.append((fg, bg))
        for suffix in ("bit.active", "bit.component", "bit.conflict", "bit.undefined", "non.bit", "byte.header"):
            pairs.append(("color.bg.plugin.editors.compositeeditor.text",
                          "color.bg.plugin.editors.compositeeditor." + suffix))
        for fg, bg in pairs:
            with self.subTest(fg=fg, bg=bg):
                self.assertGreaterEqual(contrast(self.theme, fg, bg), 4.5)

    def test_syntax_remains_legible_on_highlights(self):
        # This 3:1 floor is a theme regression guard for syntax-preserving
        # highlights, not a claim of 4.5:1 text accessibility compliance.
        foregrounds = [key for key in self.theme if key.startswith("color.fg.listing.")
                       and ".flow.arrow." not in key and ".tabs." not in key]
        foregrounds += [key for key in self.theme if key.startswith("color.fg.decompiler.")]
        backgrounds = ("color.bg.selection.listing", "color.bg.fieldpanel.selection",
            "color.bg.find.highlight", "color.bg.find.highlight.active",
            "color.bg.decompiler.highlights.find", "color.bg.decompiler.highlights.find.active",
            "color.bg.decompiler.current.variable", "color.bg.decompiler.highlights.middle.mouse")
        for fg in foregrounds:
            for bg in backgrounds:
                with self.subTest(fg=fg, bg=bg):
                    self.assertGreaterEqual(contrast(self.theme, fg, bg), 3.0)

    def test_flow_colors_share_semantics_and_highlights_are_distinct(self):
        colors = []
        for flow in ("fall.through", "jump.conditional", "jump.unconditional"):
            fg = "color.bg.plugin.functiongraph.edge." + flow
            rgb = resolved_color(self.theme, fg)
            self.assertEqual(rgb, resolved_color(self.theme, "color.flowtype." + flow))
            self.assertEqual(rgb, resolved_color(self.theme, "color.bg.plugin.programgraph.edge." + flow))
            self.assertNotEqual(rgb, resolved_color(self.theme, fg + ".highlight"))
            colors.append(rgb)
        self.assertEqual(len(set(colors)), 3)
        self.assertNotEqual(resolved_color(self.theme, "color.fg.byteviewer.changed"),
                            resolved_color(self.theme, "color.fg.error"))

    def test_status_cells_do_not_overlap(self):
        names = ("not.applied", "applied", "rejected", "ignored", "error")
        prefix = "icon.version.tracking.match.table.markup.status."
        rectangles = []
        images = []
        for state in names:
            value = self.theme[prefix + state]
            w, h = map(int, re.search(r"\[size\((\d+),(\d+)\)\]", value).groups())
            x, y = map(int, re.search(r"\[move\((\d+),(\d+)\)\]", value).groups())
            self.assertLessEqual(x + w, 45)
            self.assertLessEqual(y + h, 16)
            rectangles.append((x, x + w))
            images.append((ROOT / asset(value)).read_bytes())
        for a, b in zip(sorted(rectangles), sorted(rectangles)[1:]):
            self.assertLessEqual(a[1], b[0])
        self.assertEqual(len(set(images)), len(names))
        self.assertNotEqual(asset(self.theme[prefix + "ignored"]),
                            asset(self.theme[prefix + "disabled"]))
        self.assertIn("[size(8,8)]", self.theme[prefix + "disabled"])
        self.assertNotIn("[move", self.theme[prefix + "disabled"])

    def test_filter_states_have_different_images(self):
        for off, on in (
            ("icon.widget.filterpanel.filter.off", "icon.widget.filterpanel.filter.on"),
            ("icon.plugin.datatypes.filter.arrays.off", "icon.plugin.datatypes.filter.arrays.on"),
            ("icon.plugin.datatypes.filter.pointers.off", "icon.plugin.datatypes.filter.pointers.on"),
            ("icon.version.tracking.unfiltered", "icon.version.tracking.filtered"),
        ):
            self.assertNotEqual((ROOT / asset(self.theme[off])).read_bytes(),
                                (ROOT / asset(self.theme[on])).read_bytes())

    def test_semantic_variants_keep_separate_assets(self):
        groups = (
            ("icon.plugin.symboltree.node.", ("function", "function.external", "function.thunk")),
            ("icon.plugin.datatypes.", ("structure", "union", "pointer")),
            ("icon.debugger.breakpoint.marker.", (
                "enabled", "disabled", "mixed", "ineffective.enabled",
                "ineffective.disabled", "ineffective.mixed")),
            ("icon.plugin.functiongraph.action.viewer.vertex.hover.", (
                "paths.to.vertex", "paths.from.vertex", "paths.from.to.vertex", "paths.all",
                "cycles", "cycles.all", "scoped.flow.forward", "scoped.flow.reverse")),
            ("icon.decompiler.action.", ("provider", "provider.readonly", "provider.unreachable")),
            ("icon.plugin.datatypes.util.", ("closed.folder", "closed.folder.locked",
                "closed.folder.disabled", "open.folder", "open.folder.locked", "open.folder.disabled")),
        )
        for prefix, suffixes in groups:
            with self.subTest(prefix=prefix):
                data = [(ROOT / asset(self.theme[prefix + s])).read_bytes() for s in suffixes]
                self.assertEqual(len(set(data)), len(data))

    def test_custom_sources_are_local_self_contained_svgs(self):
        for path in (ROOT / "tools/custom-icons").glob("*.svg"):
            root = ET.parse(path).getroot()
            self.assertEqual(root.attrib["viewBox"], "0 0 16 16", path.name)
            self.assertFalse(any(e.tag.endswith(("image", "script", "text")) for e in root.iter()))
            for element in root.iter():
                self.assertFalse(any(k.endswith("href") for k in element.attrib), path.name)
        for value in self.theme.values():
            if value.startswith("[EXTERNAL]") and "/ghidra-" in value:
                stem, _ = builder.split_color(Path(asset(value)).stem)
                self.assertTrue((ROOT / "tools/custom-icons" / (stem + ".svg")).is_file(), stem)

    def test_animation_frames_have_distinct_rotations(self):
        for prefix, count in (("icon.task.progress", 7), ("icon.task.progress.hourglass", 11)):
            angles = [int(re.search(r"\[rotate\((\d+)\)\]",
                                   self.theme[f"{prefix}.{n}"]).group(1))
                      for n in range(1, count + 1)]
            self.assertEqual(len(set(angles)), count)
            self.assertTrue(all(0 <= angle < 360 for angle in angles))

    def test_bundle_matches_theme_and_assets(self):
        with zipfile.ZipFile(ROOT / "dist/vscode-dark-modern.theme.zip") as z:
            self.assertIsNone(z.testzip())
            self.assertFalse(any(entry.is_dir() for entry in z.infolist()))
            self.assertEqual(z.namelist()[-1], THEME.name)
            self.assertEqual(z.read(THEME.name), THEME.read_bytes())
            for value in self.theme.values():
                if value.startswith("[EXTERNAL]"):
                    name = asset(value)
                    self.assertEqual(z.read(name), (ROOT / name).read_bytes(), name)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="theme-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        shutil.copytree(ROOT / "tools", self.repo / "tools")
        shutil.copytree(ROOT / "themes", self.repo / "themes")
        self.theme = self.repo / "themes" / THEME.name
        self.install = self.root / "ghidra_12.1.3_PUBLIC"
        self.install.mkdir()
        (self.install / "test.theme.properties").write_text("icon.add = add.png\n")

    def build(self, directory):
        return subprocess.run([sys.executable, "-B", str(self.repo / "tools/build-theme.py")],
                              env={**os.environ, "GHIDRA_DIRS": str(directory)},
                              capture_output=True, text=True)

    def test_invalid_input_leaves_existing_outputs_untouched(self):
        manifest = self.repo / "build/icon-manifest.tsv"
        manifest.parent.mkdir()
        manifest.write_text("existing manifest\n")
        before = self.theme.read_bytes()
        empty = self.root / "empty"
        empty.mkdir()
        for directory in ("", self.root / "missing", empty):
            with self.subTest(directory=directory):
                result = self.build(directory)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Cannot build theme", result.stderr)
                self.assertEqual(self.theme.read_bytes(), before)
                self.assertEqual(manifest.read_text(), "existing manifest\n")

    def test_discovers_supported_install_in_user_home(self):
        base = self.root / "ghidra"
        base.mkdir()
        target = base / self.install.name
        target.mkdir()
        with patch.dict(os.environ, {}, clear=True), patch.object(
                builder.os.path, "expanduser", return_value=str(self.root)):
            self.assertIn(str(target), builder.ghidra_dirs())

    def test_rebuild_keeps_modifiers_and_legacy_keys(self):
        with self.theme.open("a") as out:
            out.write("\nicon.test.legacy = [EXTERNAL]images/vscode/codicons/add.png[size(12,12)][move(2,3)]\n")
        expected = values(self.theme.read_text())
        first = self.build(self.install)
        self.assertEqual(first.returncode, 0, first.stderr)
        result = values(self.theme.read_text())
        self.assertEqual(result, expected)
        before = self.theme.read_bytes()
        manifest = (self.repo / "build/icon-manifest.tsv").read_bytes()
        second = self.build(self.install)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.theme.read_bytes(), before)
        self.assertEqual((self.repo / "build/icon-manifest.tsv").read_bytes(), manifest)

    @unittest.skipUnless(os.name == "posix", "Requires a POSIX shell")
    def test_render_failure_preserves_previous_assets(self):
        output = self.repo / "images/vscode/codicons/filter.png"
        output.parent.mkdir(parents=True)
        output.write_bytes(b"previous asset")
        manifest = self.repo / "build/icon-manifest.tsv"
        manifest.parent.mkdir()
        manifest.write_text("filter\tfilter\t#CCCCCC\n")
        svg = self.root / "svg"
        svg.mkdir()
        (svg / "circuit-board.svg").write_text("<svg/>")
        binary = self.root / "bin"
        binary.mkdir()
        magick = binary / "magick"
        magick.write_text('#!/bin/sh\nprintf x >> "$MAGICK_LOG"\nexit 1\n')
        magick.chmod(0o755)
        log = self.root / "magick.log"
        env = {**os.environ, "CODICONS_SRC": str(svg), "MAGICK_LOG": str(log),
               "PATH": str(binary) + os.pathsep + os.environ.get("PATH", "")}
        script = self.repo / "tools/generate-icons.sh"
        missing = subprocess.run(["sh", str(script)], env=env, capture_output=True, text=True)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("Missing SVG: filter", missing.stderr)
        self.assertFalse(log.exists(), "Rendering started before input validation")
        (svg / "filter.svg").write_text("<svg/>")
        failed = subprocess.run(["sh", str(script)], env=env, capture_output=True, text=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertTrue(log.exists())
        self.assertEqual(output.read_bytes(), b"previous asset")

    @unittest.skipUnless(os.name == "posix", "Requires a POSIX shell")
    def test_missing_custom_source_fails_before_rendering(self):
        manifest = self.repo / "build/icon-manifest.tsv"
        manifest.parent.mkdir()
        manifest.write_text("ghidra-missing\tghidra-missing\t#CCCCCC\n")
        svg = self.root / "svg"
        svg.mkdir()
        (svg / "circuit-board.svg").write_text("<svg/>")
        # A similarly named upstream file must not hide a missing local source.
        (svg / "ghidra-missing.svg").write_text("<svg/>")
        binary = self.root / "bin"
        binary.mkdir()
        magick = binary / "magick"
        log = self.root / "magick.log"
        magick.write_text('#!/bin/sh\nprintf x >> "$MAGICK_LOG"\nexit 1\n')
        magick.chmod(0o755)
        result = subprocess.run(["sh", str(self.repo / "tools/generate-icons.sh")],
            env={**os.environ, "CODICONS_SRC": str(svg), "MAGICK_LOG": str(log),
                 "PATH": str(binary) + os.pathsep + os.environ.get("PATH", "")},
            capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing SVG: ghidra-missing", result.stderr)
        self.assertFalse(log.exists())

    @unittest.skipUnless(os.name == "posix", "Requires a POSIX shell")
    def test_install_targets_12_1_3_and_accepts_custom_directory(self):
        binary = self.root / "bin"
        binary.mkdir()
        uname = binary / "uname"
        uname.write_text("#!/bin/sh\nprintf 'Linux\\n'\n")
        uname.chmod(0o755)
        config = self.root / "config with spaces"
        env = {**os.environ, "PATH": str(binary) + os.pathsep + os.environ.get("PATH", ""),
               "XDG_CONFIG_HOME": str(config)}
        env.pop("GHIDRA_USER_DIR", None)
        for target in (None, self.root / "custom settings"):
            with self.subTest(target=target):
                current_env = dict(env)
                if target is not None:
                    current_env["GHIDRA_USER_DIR"] = str(target)
                expected = target or config / "ghidra/ghidra_12.1.3_PUBLIC"
                result = subprocess.run(["sh", str(ROOT / "install.sh")], env=current_env,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual((expected / "themes" / THEME.name).read_bytes(), THEME.read_bytes())
                for icon in (ROOT / "images/vscode/codicons").glob("*.png"):
                    self.assertEqual((expected / "images/vscode/codicons" / icon.name).read_bytes(),
                                     icon.read_bytes())


if __name__ == "__main__":
    unittest.main()
