"""Optional integration check: python3 tests/check_ghidra.py /path/to/ghidra."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    install = Path(sys.argv[1]).resolve()
    root = Path(__file__).resolve().parents[1]
    jars = sorted((install / "Ghidra").rglob("*.jar"))
    if not jars:
        sys.exit(f"No Ghidra jars found in {install}")
    classpath = os.pathsep.join(str(p) for p in jars)
    with tempfile.TemporaryDirectory(prefix="ghidra-theme-check-") as temp:
        sources = [root / "tests/GhidraThemeCheck.java", root / "tests/ThemeColorPreview.java",
                   root / "tests/WindowChromePreview.java"]
        subprocess.run(["javac", "-proc:none", "-cp", classpath, "-d", temp,
                        *(str(source) for source in sources)], check=True)
        output = root / "build/theme-check.png"
        output.parent.mkdir(exist_ok=True)
        subprocess.run([
            "java", "-Djava.awt.headless=true", "-cp", temp + os.pathsep + classpath,
            "GhidraThemeCheck", str(install), str(root / "dist/vscode-dark-modern.theme.zip"),
            str(Path(temp) / "settings"), str(output),
        ], check=True)
        print(f"Rendered check: {output}")


if __name__ == "__main__":
    main()
