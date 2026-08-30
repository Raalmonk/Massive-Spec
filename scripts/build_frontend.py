#!/usr/bin/env python
"""One-command frontend build for the M-Spec timeline.

Compiles the React app (front_end/src/app.jsx) and the Tailwind CSS into
static, minified assets under front_end/dist/, then stamps the asset
references in timelinev2.html with a content-hash version query so long
`Cache-Control: immutable` headers are safe.

Usage:
    python scripts/build_frontend.py            # build once
    python scripts/build_frontend.py --watch    # rebuild app.js on change (dev)

Node.js is provided by the `nodejs-wheel-binaries` pip package (installed in
the project venv), so no system Node installation is required. The build
outputs (dist/app.js, dist/app.css) are committed to git, so the server never
needs to run this — it just serves the prebuilt files.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRONT_END = ROOT / "front_end"
DIST = FRONT_END / "dist"
HTML_FILES = [FRONT_END / "timelinev2.html", FRONT_END / "main_menu.html"]


def find_node_dir() -> Path:
    """Locate the directory containing the node executable."""
    try:
        import nodejs_wheel  # type: ignore

        return Path(nodejs_wheel.__file__).parent
    except ImportError:
        pass
    # fall back to a node already on PATH
    import shutil

    node = shutil.which("node")
    if node:
        return Path(node).parent
    sys.exit(
        "error: Node.js not found. Run: pip install nodejs-wheel-binaries "
        "(or install Node.js and put it on PATH)"
    )


def run(cmd: list[str], env: dict[str, str]) -> None:
    printable = " ".join(str(c) for c in cmd)
    print(f"+ {printable}")
    subprocess.run(cmd, cwd=FRONT_END, env=env, check=True)


def bin_path(name: str) -> Path:
    """Path to an npm-installed executable, cross-platform."""
    suffix = ".cmd" if os.name == "nt" else ""
    return FRONT_END / "node_modules" / ".bin" / f"{name}{suffix}"


def short_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()[:10]


def stamp_html() -> None:
    """Rewrite dist asset references with content-hash ?v= queries."""
    versions = {
        "dist/app.js": short_hash(DIST / "app.js"),
        "dist/app.css": short_hash(DIST / "app.css"),
    }
    for html_file in HTML_FILES:
        if not html_file.exists():
            continue
        text = html_file.read_text(encoding="utf-8")
        original = text
        for asset, digest in versions.items():
            text = re.sub(
                re.escape(asset) + r"(\?v=[0-9a-f]+)?",
                f"{asset}?v={digest}",
                text,
            )
        if text != original:
            html_file.write_text(text, encoding="utf-8", newline="\n")
            print(f"stamped asset versions in {html_file.name}")


def main() -> None:
    watch = "--watch" in sys.argv

    node_dir = find_node_dir()
    env = os.environ.copy()
    env["PATH"] = str(node_dir) + os.pathsep + env.get("PATH", "")

    if not (FRONT_END / "node_modules").exists():
        npm_cli = node_dir / "lib" / "node_modules" / "npm" / "bin" / "npm-cli.js"
        node_exe = node_dir / ("node.exe" if os.name == "nt" else "bin/node")
        run([str(node_exe), str(npm_cli), "install", "--no-audit", "--no-fund"], env)

    esbuild_cmd = [
        str(bin_path("esbuild")),
        "src/app.jsx",
        "--bundle",
        "--minify",
        "--sourcemap",
        "--outfile=dist/app.js",
        '--define:process.env.NODE_ENV="production"',
        "--target=es2019",
        "--legal-comments=none",
    ]

    tailwind_cmd = [
        str(bin_path("tailwindcss")),
        "-c", "tailwind.config.js",
        "-i", "src/tailwind.css",
        "-o", "dist/app.css",
        "--minify",
    ]

    if watch:
        # watch 模式: esbuild --watch 会阻塞, 所以先把 CSS 编译一次再进入 watch。
        # (改了 Tailwind 类之后需要重跑一次完整 build)
        run(tailwind_cmd, env)
        esbuild_cmd.append("--watch")
        run(esbuild_cmd, env)
        return

    run(esbuild_cmd, env)
    run(tailwind_cmd, env)

    stamp_html()

    for name in ("app.js", "app.css"):
        size = (DIST / name).stat().st_size
        print(f"dist/{name}: {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
