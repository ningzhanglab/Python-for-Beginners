"""Validate sources, execute all lesson code with Quarto, then check the website."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from check_course import check_practice_formats

ROOT = Path(__file__).resolve().parents[1]


def main():
    os.chdir(ROOT)
    env = os.environ.copy()
    env["QUARTO_PYTHON"] = sys.executable
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    # Keep local caches and runtime files inside the ignored project scratch folder.
    for variable, name in [("MPLCONFIGDIR", "matplotlib"), ("JUPYTER_RUNTIME_DIR", "jupyter")]:
        directory = ROOT / "scratch" / name
        directory.mkdir(parents=True, exist_ok=True)
        env[variable] = str(directory)
    quarto = shutil.which("quarto", path=env["PATH"])
    if not quarto:
        raise SystemExit("Install Quarto 1.11.9 and put quarto on PATH; see CONTRIBUTING.md.")
    subprocess.run([sys.executable, "scripts/check_course.py"], env=env, check=True)
    # Quarto executes .ipynb inputs in place. Render disposable copies so the
    # authoritative notebooks remain output-free, even after a failed render.
    with tempfile.TemporaryDirectory(prefix="python-course-build-") as temporary:
        workspace = Path(temporary)
        for name in ["_quarto.yml", "styles.css", "index.qmd", "about.qmd",
                     "lessons", "projects", "reference", "data", "scripts"]:
            source = ROOT / name
            destination = workspace / name
            if source.is_dir():
                shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copyfile(source, destination)
        subprocess.run([quarto, "render", "--execute"], cwd=workspace, env=env, check=True)
        check_practice_formats(workspace)
        output = ROOT / "_site"
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(workspace / "_site", output)
    subprocess.run([sys.executable, "scripts/check_site.py"], env=env, check=True)


if __name__ == "__main__":
    main()
