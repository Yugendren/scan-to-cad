#!/usr/bin/env python3
"""Build the three known-CAD parts, save ground truth, and produce virtual-scan
corruptions as DEV inputs. Each part runs in a subprocess because pymeshlab's
Poisson reconstruction can hard-exit the interpreter on degenerate loops; a failed
attempt is retried with a different seed/depth and every attempt is recorded.

Light enough for the Mac (seconds per part); parameter sweeps belong on the 3060."""

import json
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
tool = Path(__file__).resolve().parent
inputs = root / "devset" / "inputs"
truth_dir = root / "devset" / "truth"
inputs.mkdir(parents=True, exist_ok=True)
truth_dir.mkdir(parents=True, exist_ok=True)

RAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
PARTS = ["l_bracket", "flange", "pocket_block"]

WORKER = r'''
import json, sys
from pathlib import Path
from scanfix import known_cad
from scanfix.virtual_scanner import ScannerConfig, virtual_scan
name, rays, seed, depth, truth_dir, inputs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]), Path(sys.argv[6])
part, truth = getattr(known_cad, name)()
part.export(truth_dir / f"{name}_truth.stl")
scan, stats = virtual_scan(part, ScannerConfig(views=12, rays_per_view=rays, seed=seed, poisson_depth=depth))
out = inputs / f"synth_{name}.stl"
scan.export(out)
truth["scanner_stats"] = stats
truth["truth_stl"] = str(truth_dir / f"{name}_truth.stl")
truth["truth_bbox_measured"] = [round(float(x), 3) for x in part.extents]
truth["scan_faces"] = int(len(scan.faces)); truth["scan_watertight"] = bool(scan.is_watertight)
(truth_dir / f"{name}.json").write_text(json.dumps(truth, indent=2))
print("OK", out.name, len(scan.faces), "faces", flush=True)
'''

manifest, attempts = {}, []
for name in PARTS:
    done = False
    for seed, depth in [(0, 8), (1, 8), (2, 7), (3, 9)]:
        t0 = time.time()
        r = subprocess.run([sys.executable, "-c", WORKER, name, str(RAYS), str(seed), str(depth),
                            str(truth_dir), str(inputs)], cwd=tool, capture_output=True, text=True)
        ok = r.returncode == 0 and "OK" in r.stdout
        attempts.append({"part": name, "seed": seed, "depth": depth, "ok": ok,
                         "seconds": round(time.time() - t0, 1),
                         "stderr_tail": r.stderr.strip().splitlines()[-1:] if r.stderr.strip() else []})
        print(f"{name} seed={seed} depth={depth}: {'OK' if ok else 'FAILED'} ({time.time()-t0:.1f}s)", flush=True)
        if ok:
            manifest[f"synth_{name}.stl"] = json.loads((truth_dir / f"{name}.json").read_text())
            done = True
            break
    if not done:
        print(f"{name}: all attempts failed — recorded, no DEV item", flush=True)
manifest["_attempts"] = attempts
(truth_dir / "synthetic_truth.json").write_text(json.dumps(manifest, indent=2))
print("truth:", truth_dir / "synthetic_truth.json")
