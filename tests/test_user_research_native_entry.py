#!/usr/bin/env python3
"""Real Product entry in ordinary host-native user mode. NO mocked producer/tool results.

The test must stop at the FIRST true pending native tool request; its success
never implies cognition, verification, publication, or project R01 approval.
"""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import native_host_bridge as native

def check_fail(code,call):
    try:call()
    except Exception as e:
        if code not in str(e): raise AssertionError((code,str(e)))
        return
    raise AssertionError('expected failure: '+code)

with tempfile.TemporaryDirectory(prefix='pc_user_native_') as td:
    d=Path(td)
    ev=d/'user_evidence'
    native.prepare(ROOT/'FROZEN_HANDOFF.zip',ev)
    check_fail('NATURAL_QUESTION_REQUIRED',lambda:native.start(
      ev,None,'primary-host-agent','native-model-1','isolated-review-agent','native-model-2',None,
      run_scope='USER_RESEARCH',question='   '))
    check_fail('USER_RESEARCH_MUST_NOT_CONSUME_PROJECT_AUTHORITY',lambda:native.start(
      ev,d/'fake-control.md','primary-host-agent','native-model-1',
      'isolated-review-agent','native-model-2',None,run_scope='USER_RESEARCH',question='何为科学？'))
    check_fail('FROZEN_BRIDGE_REQUIRES_SEPARATE_VERIFIER_PROVIDER',lambda:native.start(
      ev,None,'same-host','native-model-1','same-host','native-model-2',None,
      run_scope='USER_RESEARCH',question='科学是什么？'))
    check_fail('FRESH_PROJECT_AUTHORIZATION_REQUIRED',lambda:native.start(
      ev,None,'primary-host-agent','native-model-1','isolated-review-agent',
      'native-model-2',None,run_scope='PROJECT_R01'))
    state=d/'synthetic.md'
    state.write_text('STATE_STATUS: AUTHORITATIVE_DYNAMIC_STATE\nCONTROL_GATE: PASS\nR01_AUTHORIZATION: GRANTED\n'+native.PRODUCT_SHA+native.HANDOFF_SHA)
    check_fail('PROJECT_R01_REQUIRES_TRUSTED_EXTERNAL_AUTHORIZATION_CHANNEL',lambda:native.start(
      ev,state,'primary-host-agent','native-model-1','isolated-review-agent',
      'native-model-2','K'*64,run_scope='PROJECT_R01',question='这是另一个问题'))
    question='为什么科学论文的同行评议不能自动证明一个因果结论？'
    result=native.start(ev,None,'primary-host-agent','native-model-1',
       'isolated-review-agent','native-model-2',None,run_scope='USER_RESEARCH',question=question)
    pid=result['pid']; got=None
    try:
        for _ in range(180):
            p=native.pending(ev)
            if p['pending']:
                got=p;break
            try:os.kill(pid,0)
            except OSError:break
            time.sleep(0.25)
    finally:
        try:os.killpg(pid,signal.SIGTERM)
        except (ProcessLookupError,PermissionError):pass
    assert got and got['kind']=='search', (got,(ev/'PRODUCT_BRIDGE_STDERR.log').read_text(errors='replace')[-3000:])
    assert got['request']['request_type']=='OPEN_WORLD_SEARCH'
    assert result['project_r01_authorized'] is False
    assert result['run_scope']=='USER_RESEARCH'
    assert result['question']==question
    assert result['question_sha256']==hashlib.sha256(question.encode()).hexdigest()
    assert native.native_raw_directory(ev).name=='NATIVE_RUN_EVIDENCE'
    assert not (ev/'R01_RAW_EVIDENCE').exists()
    assert not (ev/'NATIVE_RUN_EVIDENCE'/'FINAL_RESULT.json').exists()
    assert 'PC_R01_SEARCH_SIGNING_KEY' not in (ev/'NATIVE_HOST_PROCESS.json').read_text()
    assert native.digest((ev/'FROZEN_HANDOFF'/'HARNESS'/'R01_REAL_MODEL_FILE_BRIDGE.py').read_bytes()) == native.BRIDGE_SHA
    assert native.digest(next((ev/'FROZEN_HANDOFF'/'PRODUCT').glob('*.zip')).read_bytes()) == native.PRODUCT_SHA
    print(json.dumps({'test':'ORDINARY_NATIVE_RESEARCH_ENTRY', 'result':'PASS',
         'question_sha256':result['question_sha256'],
         'pending_request_kind':got['kind'],
         'model_or_search_completed':False,'independent_verification':False,
         'research_publication_completed':False,'r01_authorized':False,
         'negative_cases':5},ensure_ascii=False))
