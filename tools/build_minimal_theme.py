#!/usr/bin/env python3
"""Ultra-minimal: only enable PageList visibility. Nothing else."""
from pathlib import Path

ROOT = Path(r"H:/project/English_Learning_Platform")
src = (ROOT / "backup" / "theme-indie-original-backup.xml").read_text(encoding="utf-8")
old = "<b:widget cond='!data:view.isPost' id='PageList1' locked='true' title='' type='PageList' visible='false'>"
new = "<b:widget cond='!data:view.isPost' id='PageList1' locked='true' title='' type='PageList' visible='true'>"
if old not in src:
    raise SystemExit("pattern missing")
out = src.replace(old, new, 1)
path = ROOT / "themeCode-MINIMAL.txt"
path.write_text(out, encoding="utf-8", newline="\n")
print("Wrote", path, "size", len(out))
