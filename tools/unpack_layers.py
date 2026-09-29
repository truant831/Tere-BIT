#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
import shutil
import sys

def extract_zip(src: Path, dst: Path, password: str | None = None) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    with ZipFile(src) as zf:
        pwd = password.encode() if password is not None else None
        zf.extractall(dst, pwd=pwd)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} layers.zip")
        raise SystemExit(2)

    root = Path("unpacked_layers")
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()

    outer = Path(sys.argv[1])
    first_dir = root / "outer"
    extract_zip(outer, first_dir)

    candidates = sorted(first_dir.rglob("layer_1.zip"))
    if not candidates:
        raise FileNotFoundError("layer_1.zip not found inside layers.zip")

    current = candidates[0]

    for layer in range(1, 1338):
        stage = root / f"layer_{layer:04d}"
        print(f"[{layer:4d}/1337] {current.name}  password={layer}")
        extract_zip(current, stage, str(layer))

        next_archives = sorted(stage.rglob(f"layer_{layer + 1}.zip"))
        if layer < 1337:
            if not next_archives:
                raise FileNotFoundError(
                    f"layer_{layer + 1}.zip not found after extracting layer {layer}"
                )
            current = next_archives[0]
        else:
            html = list(stage.rglob("prize.html"))
            if not html:
                raise FileNotFoundError("prize.html not found after layer 1337")
            print(f"Done: {html[0]}")

if __name__ == "__main__":
    main()
