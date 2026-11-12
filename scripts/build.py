"""Validate sources, execute all lesson code with Quarto, then check the website."""

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import yaml

from check_course import check_practice_formats, check_exports

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['review'], help='Include the browser accessibility audit in a separate review site.')
    args = parser.parse_args()
    output_name = '_site-review' if args.profile else '_site'
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
        for name in ["_quarto.yml", "_quarto-review.yml", "styles.css", "index.qmd", "about.qmd", "requirements.txt",
                     "lessons", "projects", "reference", "data", "scripts", "examples"]:
            source = ROOT / name
            destination = workspace / name
            if source.is_dir():
                shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copyfile(source, destination)
        # A changed custom stylesheet must get a fresh URL after publication.
        # Derive it from the authoritative file; keep source configuration simple.
        css_name = 'styles-' + hashlib.sha256((workspace / 'styles.css').read_bytes()).hexdigest()[:12] + '.css'
        shutil.copyfile(workspace / 'styles.css', workspace / css_name)
        config_path = workspace / '_quarto.yml'
        config = yaml.safe_load(config_path.read_text(encoding='utf-8'))
        config['format']['html']['css'] = css_name
        config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding='utf-8')
        command = [quarto, "render", "--execute"]
        if args.profile:
            command += ['--profile', args.profile]
        subprocess.run(command, cwd=workspace, env=env, check=True)
        # Outputs are created during execution, after Quarto discovers resources.
        # Stage them explicitly; absolute learner links also work inside Colab.
        shutil.copytree(workspace / 'downloads', workspace / output_name / 'downloads', dirs_exist_ok=True)
        check_practice_formats(workspace)
        check_exports(workspace)
        output = ROOT / output_name
        if output.exists():
            shutil.rmtree(output)
        shutil.copytree(workspace / output_name, output)
    subprocess.run([sys.executable, "scripts/check_site.py", '--site', output_name], env=env, check=True)


if __name__ == "__main__":
    main()
