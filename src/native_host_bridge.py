#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API-free host-agent adapter to the already-frozen RC14 file bridge.

This utility never invokes a model or search API. A *host Agent* must perform the
pending native tool call and provide its actual output and invocation trace.
Neither operator completion nor provenance metadata grants epistemic authority.
"""
import argparse
import hashlib
import json
import os
import secrets
from pathlib import Path
import subprocess
import sys
import zipfile

PRODUCT_SHA = '7b538ae5cef0fce538ba1ff557f3fe1e1b61cdcd63c6c6e76a3168c14ebaa3e5'
HANDOFF_SHA = '6b233e25914530f5aa95c485f90e22330a900e2c1cfcb996220893d80b960b54'
BRIDGE_SHA = '4ef997683636a49250f27c398d6f265b6f326e56d3a48331ccc91fb09578d370'
KINDS = {'search', 'model', 'verification'}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


def ensure_no_symlink_or_traversal(zf):
    names = set()
    for info in zf.infolist():
        name = info.filename
        parts = Path(name).parts
        if name in names or name.startswith('/') or '..' in parts or (info.external_attr >> 16) & 0o170000 == 0o120000:
            raise ValueError('UNSAFE_OR_DUPLICATE_HANDOFF_MEMBER')
        names.add(name)
    return names


def verify_handoff(path):
    raw = Path(path).read_bytes()
    if digest(raw) != HANDOFF_SHA:
        raise ValueError('HANDOFF_SHA_MISMATCH')
    with zipfile.ZipFile(path) as z:
        names = ensure_no_symlink_or_traversal(z)
        manifest = z.read('HANDOFF_MANIFEST.sha256').decode().splitlines()
        listed = set()
        for line in manifest:
            sha, name = line.split('  ', 1)
            if name in listed or name not in names or digest(z.read(name)) != sha:
                raise ValueError('HANDOFF_MANIFEST_MISMATCH')
            listed.add(name)
        if names - {'HANDOFF_MANIFEST.sha256'} != listed:
            raise ValueError('HANDOFF_INVENTORY_MISMATCH')
        products = [n for n in names if n.startswith('PRODUCT/') and n.endswith('.zip')]
        if len(products) != 1 or digest(z.read(products[0])) != PRODUCT_SHA:
            raise ValueError('PRODUCT_SHA_MISMATCH')
        if digest(z.read('HARNESS/R01_REAL_MODEL_FILE_BRIDGE.py')) != BRIDGE_SHA:
            raise ValueError('BRIDGE_SHA_MISMATCH')
    return {'handoff_sha256': HANDOFF_SHA, 'product_sha256': PRODUCT_SHA,
            'bridge_sha256': BRIDGE_SHA, 'manifest_items': len(manifest)}


def prepare(handoff, evidence):
    facts = verify_handoff(handoff)
    dest = Path(evidence).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    if list(dest.iterdir()):
        raise ValueError('EVIDENCE_DIRECTORY_MUST_BE_EMPTY')
    with zipfile.ZipFile(handoff) as z:
        ensure_no_symlink_or_traversal(z)
        z.extractall(dest / 'FROZEN_HANDOFF')
    (dest / 'NATIVE_HOST_IDENTITY.json').write_bytes(canonical({
        **facts, 'execution_mode': 'AGENT_PLATFORM_NATIVE_TOOLS_NO_API',
        'epistemic_status': 'NOT_EXECUTED_NOT_VERIFIED',
        'provenance_limit': 'HOST_RECORDED_NOT_PROVIDER_SIGNED'}))
    return facts


def authorize_state(path):
    """Operational control gate. Not an independent assertion of project-file authority."""
    state = Path(path).read_text(encoding='utf-8')
    fields = dict(s.split(':', 1) for s in state.splitlines() if ':' in s and s.split(':', 1)[0].isupper())
    if (fields.get('STATE_STATUS', '').strip() != 'AUTHORITATIVE_DYNAMIC_STATE'
        or fields.get('CONTROL_GATE', '').strip() not in ('PASS', 'RECOVERED_AND_FRESH_PROJECT_VERIFIED')
        or fields.get('R01_AUTHORIZATION', '').strip() != 'GRANTED'
        or PRODUCT_SHA not in state or HANDOFF_SHA not in state):
        raise PermissionError('FRESH_PROJECT_AUTHORIZATION_REQUIRED')
    return digest(state.encode('utf-8'))


def start(evidence, state, model_provider, model_id, verifier_provider, verifier_model,
          search_key, *, run_scope='PROJECT_R01', question=None, output_profile='STANDARD_REPORT'):
    """Launch a real canonical Product run using native Agent tools.

    PROJECT_R01 needs externally established fresh project authorization; ordinary
    USER_RESEARCH needs an actual user question but grants **zero** project/release
    authority. Both retain identical semantic, evidence and publication gates.
    """
    if run_scope not in ('PROJECT_R01', 'USER_RESEARCH'):
        raise ValueError('UNKNOWN_RUN_SCOPE')
    if run_scope == 'PROJECT_R01':
        if not state:
            raise PermissionError('FRESH_PROJECT_AUTHORIZATION_REQUIRED')
        # An ordinary installed Skill has no independently trusted Project
        # attestation channel. A text file claiming GRANTED is not authority.
        # Project R01 must be launched by its separately authorized execution
        # operator and must never be self-authorized by this generic entry.
        raise PermissionError('PROJECT_R01_REQUIRES_TRUSTED_EXTERNAL_AUTHORIZATION_CHANNEL')
    else:
        if state:
            raise ValueError('USER_RESEARCH_MUST_NOT_CONSUME_PROJECT_AUTHORITY')
        if not isinstance(question, str) or not question.strip():
            raise ValueError('NATURAL_QUESTION_REQUIRED')
        question = question.strip()
        st_hash = None
        # Internal per-run HMAC binds source bytes; NOT an API credential and
        # NOT proof that the external source itself signed the receipt.
        if not search_key:
            search_key = secrets.token_hex(32)
        if len(search_key) < 32:
            raise ValueError('SEARCH_RECEIPT_KEY_INVALID')
    if not all([model_provider, model_id, verifier_provider, verifier_model]):
        raise ValueError('HOST_AGENT_MODEL_IDENTITIES_REQUIRED')
    if model_provider == verifier_provider:
        raise ValueError('FROZEN_BRIDGE_REQUIRES_SEPARATE_VERIFIER_PROVIDER')
    if not isinstance(output_profile, str) or not output_profile.strip():
        raise ValueError('OUTPUT_PROFILE_REQUIRED')
    root = Path(evidence).resolve()
    if not (root / 'NATIVE_HOST_IDENTITY.json').is_file() or (root / 'NATIVE_HOST_PROCESS.json').exists():
        raise ValueError('PREPARE_REQUIRED_OR_ALREADY_STARTED')
    handoff = root / 'FROZEN_HANDOFF'
    product = next((handoff / 'PRODUCT').glob('*.zip'))
    bridge = handoff / 'HARNESS/R01_REAL_MODEL_FILE_BRIDGE.py'
    if digest(product.read_bytes()) != PRODUCT_SHA or digest(bridge.read_bytes()) != BRIDGE_SHA:
        raise ValueError('FROZEN_BYTES_CHANGED')
    rawdir = 'NATIVE_RUN_EVIDENCE' if run_scope == 'USER_RESEARCH' else 'R01_RAW_EVIDENCE'
    env = os.environ.copy()
    env.update({'PC_R01_MODEL_PROVIDER': model_provider, 'PC_R01_MODEL_ID': model_id,
                'PC_R01_VERIFIER_PROVIDER': verifier_provider,
                'PC_R01_VERIFIER_MODEL': verifier_model,
                'PC_R01_SEARCH_SIGNING_KEY': search_key})
    output = (root / 'PRODUCT_BRIDGE_STDOUT.log').open('ab')
    errors = (root / 'PRODUCT_BRIDGE_STDERR.log').open('ab')
    try:
        proc = subprocess.Popen([sys.executable, '-B', str(bridge), '--product-zip', str(product),
              '--expected-product-sha256', PRODUCT_SHA,
              '--evidence', str(root / rawdir), '--question', question,
              '--output-profile', output_profile],
              env=env, stdout=output, stderr=errors, start_new_session=True)
    finally:
        output.close(); errors.close()
    meta = {'pid': proc.pid, 'state_sha256': st_hash,
            'run_scope': run_scope, 'raw_evidence_dir': rawdir,
            'question_sha256': digest(question.encode('utf-8')),
            'question': question,
            'output_profile': output_profile,
            'project_r01_authorized': run_scope == 'PROJECT_R01',
            'model_provider': model_provider, 'model_id': model_id,
            'verifier_provider': verifier_provider, 'verifier_model': verifier_model,
            'epistemic_status': 'RUNNING_NOT_VERIFIED'}
    # The active signing secret stays in the child process environment, not in
    # trace, package or metadata. It never needs external API configuration.
    with (root / 'NATIVE_HOST_PROCESS.json').open('xb') as f:
        f.write(canonical(meta))
        f.flush(); os.fsync(f.fileno())
    return meta


def native_raw_directory(evidence):
    root = Path(evidence).resolve()
    info = root / 'NATIVE_HOST_PROCESS.json'
    if info.is_file():
        meta = json.loads(info.read_bytes())
        scope = meta.get('run_scope', 'PROJECT_R01')
        rawdir = meta.get('raw_evidence_dir')
        expected = 'NATIVE_RUN_EVIDENCE' if scope == 'USER_RESEARCH' else 'R01_RAW_EVIDENCE'
        if rawdir != expected:
            raise ValueError('INVALID_EVIDENCE_DIRECTORY_SCOPE')
        return root / rawdir
    return root / 'R01_RAW_EVIDENCE'


def pending(evidence):
    root = native_raw_directory(evidence) / 'MODEL_BRIDGE'
    p = root / 'PENDING_REQUEST.json'
    if not p.is_file():
        ev = root.parent
        if (ev / 'HARNESS_EXCEPTION.txt').is_file():
            return {'pending': False, 'terminal_exists': False,
                    'process_state': 'FAILED_CLOSED',
                    'evidence': str(ev / 'HARNESS_EXCEPTION.txt')}
        if (ev / 'FINAL_RESULT.json').is_file():
            return {'pending': False, 'terminal_exists': True,
                    'process_state': 'CANONICAL_RESULT_PRESENT_NOT_AUTOMATICALLY_VERIFIED'}
        process_file = Path(evidence).resolve() / 'NATIVE_HOST_PROCESS.json'
        if process_file.is_file():
            pid = json.loads(process_file.read_bytes()).get('pid')
            alive = False
            if isinstance(pid, int) and pid > 0:
                try:
                    os.kill(pid, 0)
                    alive = True
                    stat = Path('/proc') / str(pid) / 'stat'
                    if stat.is_file() and stat.read_text().split(') ', 1)[1].startswith('Z'):
                        alive = False
                except (OSError, PermissionError, ValueError):
                    alive = False
            if not alive:
                return {'pending': False, 'terminal_exists': False,
                        'process_state': 'INTERRUPTED_OR_FAILED_NO_TERMINAL',
                        'requires_evidence_recovery': True}
        return {'pending': False, 'terminal_exists': False,
                'process_state': 'WAITING_FOR_NATIVE_HOST_REQUEST'}
    req = json.loads(p.read_bytes())
    if req['kind'] not in KINDS:
        raise ValueError('UNKNOWN_REQUEST_KIND')
    path = Path(req['request_path']).resolve()
    response = Path(req['expected_response_path']).resolve()
    kind = req['kind']
    if (path.parent != (root / kind / 'requests').resolve()
            or response.parent != (root / kind / 'responses').resolve()
            or path.stem != response.stem or path.suffix != '.json'
            or response.suffix != '.json'):
        raise ValueError('PENDING_PATH_ESCAPES_BRIDGE_ROOT')
    if not path.is_file() or digest(path.read_bytes()) != req['request_sha256']:
        raise ValueError('PENDING_REQUEST_BYTES_CHANGED')
    return {'pending': True, 'kind': req['kind'], 'request_sha256': req['request_sha256'],
            'request_path': str(path), 'expected_response_path': req['expected_response_path'],
            'request': json.loads(path.read_bytes())}


def submit(evidence, result_path, trace_path):
    """Bind actual host tool output bytes to current pending request; no tool calls here."""
    cur = pending(evidence)
    if not cur.get('pending'):
        raise ValueError('NO_PENDING_REQUEST')
    result_raw = Path(result_path).read_bytes()
    obj = json.loads(result_raw)
    trace_raw = Path(trace_path).read_bytes()
    trace = json.loads(trace_raw)
    if not isinstance(obj, dict) or not isinstance(trace, dict):
        raise ValueError('OUTPUT_AND_TRACE_MUST_BE_OBJECTS')
    if (trace.get('request_sha256') != cur['request_sha256']
        or trace.get('result_sha256') != digest(result_raw)
        or not str(trace.get('host_tool_call_id') or '').strip()
        or not str(trace.get('host_context_id') or '').strip()
        or trace.get('kind') != cur['kind']):
        raise ValueError('HOST_TOOL_TRACE_MISSING_OR_NOT_BOUND_TO_BYTES')
    if cur['kind'] == 'model':
        if not isinstance(obj.get('semantic_output'), dict):
            raise ValueError('SEMANTIC_OUTPUT_REQUIRED')
    elif cur['kind'] == 'search':
        receipts = obj.get('receipts')
        if not isinstance(receipts, list) or not receipts:
            raise ValueError('ACTUAL_SEARCH_RECEIPTS_REQUIRED')
        for r in receipts:
            if not r.get('engine') or not r.get('result_urls'):
                raise ValueError('ACTUAL_SEARCH_ORIGIN_REQUIRED')
            for url in r['result_urls']:
                if not r.get('result_contents', {}).get(url) or not r.get('result_source_identities', {}).get(url):
                    raise ValueError('ACTUAL_SEARCH_BYTES_AND_SOURCE_IDENTITY_REQUIRED')
    else:
        if type(obj.get('pass')) is not bool:
            raise ValueError('EXPLICIT_VERIFICATION_VERDICT_REQUIRED')
    # Distinct *contexts* are required, not sufficient for independence; checker
    # still has its own source/claim/method obligations, and no self promotion.
    root = Path(evidence).resolve()
    led = root / 'NATIVE_TOOL_CONTEXTS.jsonl'
    old = [json.loads(s) for s in led.read_text().splitlines()] if led.exists() else []
    if any(x['request_sha256'] == cur['request_sha256'] for x in old):
        raise ValueError('REQUEST_ALREADY_SUBMITTED')
    if cur['kind'] == 'verification':
        if any(x['kind'] == 'model' and x['host_context_id'] == trace['host_context_id'] for x in old):
            raise ValueError('VERIFIER_CONTEXT_NOT_ISOLATED_FROM_PRODUCER')
    if cur['kind'] == 'model':
        if any(x['kind'] == 'verification' and x['host_context_id'] == trace['host_context_id'] for x in old):
            raise ValueError('PRODUCER_CONTEXT_NOT_ISOLATED_FROM_VERIFIER')
    # Operator cannot invent provider IDs. Host trace should carry the observed
    # invocation ID, and the bridge will re-check configured identity metadata.
    if cur['kind'] in ('model', 'verification'):
        if (str(obj.get('provider_request_id')) != str(trace['host_tool_call_id'])
            or not obj.get('provider_identity') or not obj.get('model_identity')
            or not obj.get('observed_at')):
            raise ValueError('ACTUAL_MODEL_TOOL_PROVENANCE_REQUIRED')
    response = dict(obj)
    if 'request_sha256' in response or 'bridge_request_identity' in response:
        raise ValueError('RESERVED_RESPONSE_FIELD')
    response['request_sha256'] = cur['request_sha256']
    out = Path(cur['expected_response_path'])
    if out.exists():
        raise ValueError('RESPONSE_ALREADY_EXISTS')
    out.parent.mkdir(parents=True, exist_ok=True)
    # Keep exact untrusted host trace/output *outside* product; admission still
    # belongs to canonical Product & independent checker, not to this operator.
    payload_id = cur['request_sha256']
    raw_dest = root / 'NATIVE_HOST_RAW' / (payload_id + '.json')
    trace_dest = root / 'NATIVE_HOST_TRACE' / (payload_id + '.json')
    raw_dest.parent.mkdir(exist_ok=True)
    trace_dest.parent.mkdir(exist_ok=True)
    # Exclusive append-once evidence. The exact trace bytes already checked
    # above are the bytes preserved; never reopen a mutable caller file.
    for dest, raw in ((raw_dest, result_raw), (trace_dest, trace_raw)):
        with dest.open('xb') as f:
            f.write(raw)
            f.flush(); os.fsync(f.fileno())
    with out.open('xb') as f:
        f.write(canonical(response))
        f.flush(); os.fsync(f.fileno())
    with led.open('ab') as f:
        f.write(canonical({'kind': cur['kind'], 'request_sha256': payload_id,
                           'host_context_id': trace['host_context_id'],
                           'host_tool_call_id': trace['host_tool_call_id'],
                           'result_sha256': digest(result_raw),
                           'host_reported_only': True}))
        f.flush(); os.fsync(f.fileno())
    return {'submitted': True, 'kind': cur['kind'], 'response_path': str(out),
            'provenance_level': 'HOST_RECORDED_NOT_PROVIDER_SIGNED'}


def main():
    parser = argparse.ArgumentParser(description='API-free agent-host transport, not a verifier')
    sub = parser.add_subparsers(dest='cmd', required=True)
    i = sub.add_parser('inspect'); i.add_argument('--handoff', required=True)
    p = sub.add_parser('prepare'); p.add_argument('--handoff', required=True); p.add_argument('--evidence', required=True)
    s = sub.add_parser('start'); s.add_argument('--evidence', required=True); s.add_argument('--state')
    s.add_argument('--scope', choices=['user', 'r01'], default='user')
    s.add_argument('--question'); s.add_argument('--output-profile', default='STANDARD_REPORT')
    for key in ('model-provider', 'model-id', 'verifier-provider', 'verifier-model'):
        s.add_argument('--'+key, required=True)
    n = sub.add_parser('next'); n.add_argument('--evidence', required=True)
    d = sub.add_parser('deliver'); d.add_argument('--evidence', required=True); d.add_argument('--destination', required=True)
    x = sub.add_parser('submit'); x.add_argument('--evidence', required=True); x.add_argument('--result', required=True); x.add_argument('--trace', required=True)
    a = parser.parse_args()
    try:
        if a.cmd == 'inspect': out = verify_handoff(a.handoff)
        elif a.cmd == 'prepare': out = prepare(a.handoff, a.evidence)
        elif a.cmd == 'start': out = start(a.evidence, a.state, a.model_provider, a.model_id, a.verifier_provider, a.verifier_model, os.environ.get('PC_R01_SEARCH_SIGNING_KEY'), run_scope=('PROJECT_R01' if a.scope == 'r01' else 'USER_RESEARCH'), question=a.question, output_profile=a.output_profile)
        elif a.cmd == 'next': out = pending(a.evidence)
        elif a.cmd == 'deliver':
            from publication_handoff import stage_delivery
            out = stage_delivery(a.evidence, a.destination)
        else: out = submit(a.evidence, a.result, a.trace)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except (Exception,) as e:
        print(json.dumps({'ok': False, 'failure': type(e).__name__, 'reason': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__': main()
