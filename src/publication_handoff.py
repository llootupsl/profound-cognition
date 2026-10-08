#!/usr/bin/env python3
"""RC14 native-host *delivery* contract: never confer epistemic authority.

Copies only the actual frozen Product's renderer bytes to a reviewable output
when (1) canonical final result claims legal state, (2) every required file is
present and digest-matches, (3) independently inspectable host transport bytes
exist. This cannot independently establish semantic entailment or provider
independence and therefore never marks the result RELEASED.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import zipfile


def check_real_format(path, form):
    """Independent document-container sanity, not independent epistemic QA."""
    if form == "pdf":
        try:
            import fitz
            doc = fitz.open(str(path))
            try:
                if doc.page_count < 1 or not any(pg.get_text().strip() for pg in doc):
                    raise ValueError("PDF_HAS_NO_READABLE_PAGES")
            finally:
                doc.close()
        except ImportError:
            raise ValueError("PDF_PARSER_UNAVAILABLE_NO_RECEIVER_PASS")
        except (ValueError, RuntimeError) as exc:
            raise ValueError("INVALID_REAL_PDF: " + str(exc))
    elif form == "docx":
        try:
            with zipfile.ZipFile(path) as z:
                names = set(z.namelist())
                if not {"[Content_Types].xml", "word/document.xml", "_rels/.rels"}.issubset(names) or z.testzip():
                    raise ValueError("INVALID_OOXML_PACKAGE")
                from xml.etree import ElementTree as ET
                ET.fromstring(z.read("word/document.xml"))
        except (zipfile.BadZipFile, KeyError) as exc:
            raise ValueError("INVALID_REAL_DOCX: " + str(exc))
    else:
        from html.parser import HTMLParser
        class Probe(HTMLParser):
            def __init__(self):
                super().__init__(); self.seen_body = False; self.text = []
            def handle_starttag(self, tag, attrs):
                if tag == "body": self.seen_body = True
            def handle_data(self, data): self.text.append(data)
        doc = Probe(); doc.feed(path.read_text(encoding="utf-8"))
        if not doc.seen_body or not "".join(doc.text).strip():
            raise ValueError("HTML_STRUCTURE_OR_CONTENT_MISSING")

FORMS = ("pdf", "docx", "html")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def jread(path):
    obj = json.loads(path.read_bytes())
    if not isinstance(obj, dict):
        raise ValueError("EXPECTED_JSON_OBJECT")
    return obj


def child(path, parent):
    # Neither publication paths nor evidence symlinks may escape the exact run.
    if path.is_symlink() or not path.resolve().is_relative_to(parent.resolve()):
        raise ValueError("PATH_OUTSIDE_RUN_OR_SYMLINK")
    return path


def validate_native_delivery(evidence):
    base = Path(evidence).resolve()
    meta = jread(base / "NATIVE_HOST_PROCESS.json")
    scope = meta.get("run_scope")
    if scope not in ("USER_RESEARCH", "PROJECT_R01"):
        raise ValueError("INVALID_RUN_SCOPE")
    dirname = "NATIVE_RUN_EVIDENCE" if scope == "USER_RESEARCH" else "R01_RAW_EVIDENCE"
    if meta.get("raw_evidence_dir") != dirname:
        raise ValueError("INVALID_RUN_EVIDENCE_SCOPE")
    run = base / dirname
    final = jread(run / "FINAL_RESULT.json")
    terminal = jread(run / "TERMINAL_STATE.json")
    if not (final.get("frozen") is True and final.get("snapshot_id") and final.get("snapshot_hash")
            and final.get("publication_state") == "PUBLISHED"
            and final.get("memory_committed") is True
            and final.get("commit_state") == "COMMITTED"):
        raise ValueError("CANONICAL_PRODUCT_NOT_PUBLISHED_AND_COMMITTED")
    pub = final.get("publication_freeze") or {}
    if pub.get("state") != "PUBLICATION_FROZEN":
        raise ValueError("PUBLICATION_FREEZE_MISSING")
    if (terminal.get("snapshot_id") != final["snapshot_id"]
            or terminal.get("snapshot_hash") != final["snapshot_hash"]
            or terminal.get("publication_state") != final["publication_state"]
            or terminal.get("frozen") is not True):
        raise ValueError("TERMINAL_AND_PRODUCT_DISAGREE")
    artifacts = (final.get("publication_artifacts") or {}).get("artifacts") or {}
    validation = (final.get("publication_artifacts") or {}).get("verify") or {}
    if validation.get("status") != "VERIFIED" or validation.get("publication_freeze_pdf") is not True:
        raise ValueError("PDF_PARSER_VERIFICATION_MISSING")
    checked = {}
    expected_parent = (run / "_runtime_artifacts" / "publication").resolve()
    for form in FORMS:
        data = artifacts.get(form) or {}
        if data.get("status") != "RENDERED" or not data.get("path"):
            raise ValueError("REQUIRED_PUBLICATION_ARTIFACT_MISSING:" + form)
        p = child(Path(data["path"]), expected_parent)
        if not p.is_file() or p.stat().st_size <= 0 or p.stat().st_size != data.get("bytes"):
            raise ValueError("PUBLICATION_ARTIFACT_BYTES_MISSING:" + form)
        if sha(p.read_bytes()) != data.get("sha256"):
            raise ValueError("PUBLICATION_ARTIFACT_DIGEST_MISMATCH:" + form)
        check_real_format(p, form)
        checked[form] = {"path": str(p), "sha256": data["sha256"], "bytes": data["bytes"]}
    # A host-written trace alone is not enough. Each submitted result must be
    # causally attached to one immutable model-visible Bridge REQUEST byte file
    # and one actually consumed Bridge RESPONSE byte file.
    bridge_root = run / "MODEL_BRIDGE"
    bridge_index = bridge_root / "BRIDGE_INDEX.jsonl"
    if not bridge_index.is_file():
        raise ValueError("MODEL_VISIBLE_BRIDGE_INDEX_MISSING")
    bridge_events = [json.loads(x) for x in bridge_index.read_text().splitlines() if x.strip()]
    req_events = {}
    resp_events = {}
    for x in bridge_events:
        kind = x.get('kind')
        h = x.get('sha256') if x.get('event') == 'REQUEST' else x.get('request_sha256')
        if kind in ('search','model','verification') and h:
            key = (kind,h)
            if x.get('event') == 'REQUEST':
                if key in req_events: raise ValueError('DUPLICATE_MODEL_VISIBLE_REQUEST')
                req_events[key] = x
            elif x.get('event') == 'RESPONSE':
                if key in resp_events: raise ValueError('DUPLICATE_CONSUMED_RESPONSE')
                resp_events[key] = x
    # The model/search/verifier all need inspectable original bytes and host logs.
    ledger = run / "NATIVE_TOOL_CONTEXTS.jsonl"
    if not ledger.is_file():
        raise ValueError("ACTUAL_HOST_PROVENANCE_LEDGER_MISSING")
    rows = [json.loads(s) for s in ledger.read_text().splitlines() if s.strip()]
    if not {"search", "model", "verification"}.issubset({r.get("kind") for r in rows}):
        raise ValueError("FULL_TOOL_CHAIN_NOT_OBSERVED")
    for row in rows:
        hid = row.get("request_sha256")
        if not isinstance(hid, str) or len(hid) != 64 or any(c not in '0123456789abcdef' for c in hid):
            raise ValueError("INVALID_NATIVE_REQUEST_ID")
        original = child(run / "NATIVE_HOST_RAW" / (hid + ".json"), run)
        trace = child(run / "NATIVE_HOST_TRACE" / (hid + ".json"), run)
        if not original.is_file() or not trace.is_file():
            raise ValueError("HOST_RAW_BYTES_MISSING")
        if sha(original.read_bytes()) != row.get("result_sha256"):
            raise ValueError("HOST_RAW_BYTES_CHANGED")
        req_event = req_events.get((row.get('kind'),hid))
        resp_event = resp_events.get((row.get('kind'),hid))
        if not req_event or not resp_event:
            raise ValueError('UNMATCHED_MODEL_VISIBLE_REQUEST_OR_RESPONSE')
        kind = row.get('kind')
        rp = child(bridge_root / req_event['path'], bridge_root / kind / 'requests')
        sp = child(bridge_root / resp_event['path'], bridge_root / kind / 'responses')
        if not rp.is_file() or sha(rp.read_bytes()) != hid:
            raise ValueError('MODEL_VISIBLE_REQUEST_BYTES_MISSING_OR_CHANGED')
        if not sp.is_file() or sha(sp.read_bytes()) != resp_event.get('sha256'):
            raise ValueError('BRIDGE_CONSUMED_RESPONSE_BYTES_MISSING_OR_CHANGED')
        resp = jread(sp)
        raw_obj = jread(original)
        if resp.get('request_sha256') != hid or {k:v for k,v in resp.items() if k != 'request_sha256'} != raw_obj:
            raise ValueError('BRIDGE_RESPONSE_NOT_DERIVED_FROM_ACTUAL_HOST_BYTES')
        tr = jread(trace)
        if (tr.get("result_sha256") != row.get("result_sha256")
                or tr.get("request_sha256") != hid
                or tr.get("kind") != row.get("kind")
                or tr.get("host_tool_call_id") != row.get("host_tool_call_id")
                or tr.get("host_context_id") != row.get("host_context_id")):
            raise ValueError("HOST_PROVENANCE_LEDGER_DISAGREES")
    consumed_keys = {(r.get('kind'),r.get('request_sha256')) for r in rows}
    if set(req_events) != consumed_keys or set(resp_events) != consumed_keys or len(rows) != len(consumed_keys):
        raise ValueError('UNCONSUMED_OR_UNATTRIBUTED_BRIDGE_ACTIVITY')
    producer_contexts = {r.get('host_context_id') for r in rows if r.get('kind') == 'model'}
    verifier_contexts = {r.get('host_context_id') for r in rows if r.get('kind') == 'verification'}
    if producer_contexts & verifier_contexts:
        raise ValueError("PRODUCER_VERIFIER_CONTEXTS_OVERLAP")
    # Presence of a ledger is not actual independent model/provider attestation.
    return {"scope": scope, "snapshot_id": final["snapshot_id"],
            "snapshot_hash": final["snapshot_hash"], "artifacts": checked,
            "tool_calls": len(rows), "kinds": sorted({r['kind'] for r in rows}),
            "authority_limit": "HOST_RECORDED; SEMANTIC_TRUTH_AND_INDEPENDENCE_NOT_REAUDITED"}


def stage_delivery(evidence, destination):
    record = validate_native_delivery(evidence)
    dest = Path(destination).resolve()
    if dest.exists():
        raise ValueError("DELIVERY_PATH_ALREADY_EXISTS")
    dest.mkdir(parents=True)
    try:
        for fmt, artifact in record['artifacts'].items():
            original = Path(artifact['path'])
            target = dest / ("publication." + fmt)
            with target.open('xb') as f:
                f.write(original.read_bytes())
                f.flush(); os.fsync(f.fileno())
            if sha(target.read_bytes()) != artifact['sha256']:
                raise ValueError("DELIVERED_FILE_BYTES_CHANGED")
        audit = {"status": "PRODUCT_REPORTED_PUBLISHED__BYTES_INTEGRITY_PASS__INDEPENDENT_ACCEPTANCE_PENDING",
                 "NOT_RELEASE": True,
                 "warning": "No independent semantic/source/agent-independence audit is performed by this tool.",
                 **record}
        (dest / 'RECEIVER_CHECK.json').write_text(json.dumps(audit,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        return audit
    except BaseException:
        shutil.rmtree(dest)
        raise
