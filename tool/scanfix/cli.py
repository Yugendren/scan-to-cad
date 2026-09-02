"""scanfix CLI: run one file, or batch a directory (batch is meant for the 3060 box)."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

from .io import SUPPORTED
from .pipeline import Options, run


def _git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       cwd=Path(__file__).resolve().parents[2],
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "nogit"


def _opts(ns) -> Options:
    return Options(nozzle=ns.nozzle, min_wall=ns.min_wall, snap_budget=ns.snap_budget,
                   idealize=not ns.no_idealize, thicken_mm=ns.thicken,
                   mesh_class=ns.mesh_class, target_faces=ns.target_faces)


def _add_common(p):
    p.add_argument("-o", "--outdir", type=Path, default=None)
    p.add_argument("--nozzle", type=float, default=0.4)
    p.add_argument("--min-wall", type=float, default=0.8)
    p.add_argument("--snap-budget", type=float, default=0.15)
    p.add_argument("--no-idealize", action="store_true")
    p.add_argument("--thicken", type=float, default=0.0, help="EXPERIMENTAL explicit outward offset in mm")
    p.add_argument("--mesh-class", choices=["prismatic", "organic", "mixed"], default=None)
    p.add_argument("--target-faces", type=int, default=60000)


def _one_line(rep: dict) -> str:
    v, d, t = rep["verdict"], rep["deviation"], rep["thickness"]
    return (f"{rep['input_name']}: class={rep['mesh_class']} printable={v['printable']} "
            f"watertight={rep['after']['watertight']} dev_p95={d['p95_mm']}mm "
            f"thin={t['below_min_wall_frac']*100:.1f}% ideal={rep['idealize']['accepted']}/"
            f"{rep['idealize']['regions_found']} t={rep['runtime_s']}s")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="scanfix", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run", help="process one file")
    pr.add_argument("input", type=Path)
    _add_common(pr)
    pb = sub.add_parser("batch", help="process every supported file in a directory; appends to the ledger")
    pb.add_argument("indir", type=Path)
    pb.add_argument("--ledger", type=Path, default=None)
    _add_common(pb)
    ns = ap.parse_args(argv)
    opt = _opts(ns)

    if ns.cmd == "run":
        outdir = ns.outdir or ns.input.parent / "scanfix_out"
        rep = run(ns.input, outdir, opt)
        print(_one_line(rep))
        print(f"report: {rep['outputs']['report_html']}")
        return 0

    files = sorted(p for p in ns.indir.iterdir() if p.suffix.lower() in SUPPORTED)
    outdir = ns.outdir or ns.indir.parent / "out"
    ledger = ns.ledger or (Path(__file__).resolve().parents[2] / "evidence" / "dev_ledger.md")
    ledger.parent.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        ledger.write_text("# DEV ledger — one row per file per run\n\n"
                          "| run (UTC) | commit | file | class | watertight | printable | dev p95 mm | "
                          "within budget | thin % | idealize acc/found | runtime s | failure class |\n"
                          "|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    stamp = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    commit = _git_hash()
    rows, summary = [], []
    for f in files:
        try:
            rep = run(f, outdir / f.stem.replace(" ", "_"), opt)
        except Exception as e:  # a crash is a result too
            rows.append(f"| {stamp} | {commit} | {f.name} | ? | ? | ? | ? | ? | ? | ? | ? | CRASH: {str(e)[:80]} |")
            print(f"{f.name}: CRASH {e}")
            continue
        v, d, t, i = rep["verdict"], rep["deviation"], rep["thickness"], rep["idealize"]
        fail = []
        if not rep["after"]["watertight"]:
            fail.append("DEV-watertight")
        if not d["within_budget"]:
            fail.append("DEV-deviation")
        if t["below_min_wall_frac"] > 0.02:
            fail.append("THIN")
        if any("units" in n for n in rep["before"]["notes"]):
            fail.append("UNITS")
        rows.append(f"| {stamp} | {commit} | {f.name} | {rep['mesh_class']} | {rep['after']['watertight']} | "
                    f"{v['printable']} | {d['p95_mm']} | {d['within_budget']} | {t['below_min_wall_frac']*100:.1f} | "
                    f"{i['accepted']}/{i['regions_found']} | {rep['runtime_s']} | {', '.join(fail) or 'ok'} |")
        print(_one_line(rep))
        summary.append(rep)
    with ledger.open("a") as fh:
        fh.write("\n".join(rows) + "\n")
    (outdir / "batch_summary.json").write_text(json.dumps(
        [{k: r[k] for k in ("input_name", "mesh_class", "runtime_s", "verdict", "deviation", "thickness")}
         for r in summary], indent=2))
    print(f"ledger: {ledger}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
