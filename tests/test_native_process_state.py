#!/usr/bin/env python3
"""Native host must not confuse a missing request with a completed run."""
import sys, tempfile, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
import native_host_bridge as n
with tempfile.TemporaryDirectory() as td:
    ev=Path(td)
    meta={'run_scope':'USER_RESEARCH','raw_evidence_dir':'NATIVE_RUN_EVIDENCE','pid':2147483600}
    (ev/'NATIVE_HOST_PROCESS.json').write_bytes(n.canonical(meta))
    r=n.pending(ev)
    assert r['process_state']=='INTERRUPTED_OR_FAILED_NO_TERMINAL' and not r['terminal_exists'],r
    raw=ev/'NATIVE_RUN_EVIDENCE';raw.mkdir()
    (raw/'HARNESS_EXCEPTION.txt').write_text('synthetic crash')
    r=n.pending(ev)
    assert r['process_state']=='FAILED_CLOSED' and not r['terminal_exists'],r
    (raw/'HARNESS_EXCEPTION.txt').unlink()
    (raw/'FINAL_RESULT.json').write_text('{"frozen": false}')
    r=n.pending(ev)
    assert r['process_state']=='CANONICAL_RESULT_PRESENT_NOT_AUTOMATICALLY_VERIFIED' and r['terminal_exists'],r
    print('PASS 3 native process status cases; no false completion')
