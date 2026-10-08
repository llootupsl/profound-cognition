import sys, os, json, pathlib, tempfile, importlib.util, hashlib

BASE=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE/'src'))
import native_host_bridge as native
FROZEN=BASE/'BRIDGE_REFERENCE/R01_REAL_MODEL_FILE_BRIDGE.py'
HANDOFF=BASE/'FROZEN_HANDOFF.zip'
spec=importlib.util.spec_from_file_location('frozen_bridge',FROZEN)
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
OK=0

def check(condition, desc):
    global OK
    if not condition:raise AssertionError(desc)
    OK+=1
    print('PASS',OK,desc)

def expect_block(fn, code):
    try: fn()
    except Exception as exc:
        check(code in str(exc), 'block '+code)
        return
    raise AssertionError('expected reject '+code)

def submit_result(root,kind,body, context, req=None, call_id='CALL-1'):
    cur=req or native.pending(root)
    raw=native.canonical(body)
    trace={'kind':kind,'request_sha256':cur['request_sha256'],
           'result_sha256':native.digest(raw), 'host_tool_call_id':call_id,
           'host_context_id':context}
    result=pathlib.Path(root)/'result.json';t=pathlib.Path(root)/'trace.json'
    result.write_bytes(raw);t.write_bytes(native.canonical(trace))
    return result,t

with tempfile.TemporaryDirectory() as tmp:
    root=pathlib.Path(tmp)
    facts=native.verify_handoff(HANDOFF)
    check(facts['manifest_items']==19 and facts['product_sha256']==native.PRODUCT_SHA,'frozen package identity')
    ev=root/'evidence';native.prepare(HANDOFF,ev)
    check((ev/'FROZEN_HANDOFF/PRODUCT').exists(),'prepare real product without mutation')
    expect_block(lambda:native.prepare(HANDOFF,ev),'EVIDENCE_DIRECTORY_MUST_BE_EMPTY')
    bad=root/'bad.zip';bad.write_bytes(HANDOFF.read_bytes()[:-1]+b'X')
    expect_block(lambda:native.verify_handoff(bad),'HANDOFF_SHA_MISMATCH')
    expect_block(lambda:native.start(ev,root/'no_state','hostA','m','hostB','v','S'*64),'PROJECT_R01_REQUIRES_TRUSTED_EXTERNAL_AUTHORIZATION_CHANNEL')
    state=root/'historical.md';state.write_text('STATE_STATUS: PROPOSED_PROJECT_FILE_REPLACEMENT\nCONTROL_GATE: BLOCKED\nR01_AUTHORIZATION: NOT_GRANTED\n'+native.PRODUCT_SHA+native.HANDOFF_SHA)
    expect_block(lambda:native.start(ev,state,'hostA','m','hostB','v','S'*64),'PROJECT_R01_REQUIRES_TRUSTED_EXTERNAL_AUTHORIZATION_CHANNEL')
    source=bridge.EvidenceStore(ev/'R01_RAW_EVIDENCE/MODEL_BRIDGE')
    check(not native.pending(ev)['pending'],'no request yet')
    # Actual frozen bridge emits real bytes. Operator must consume exactly them.
    seq,stem,path,h=source.request('search',{'request_type':'OPEN_WORLD_SEARCH','queries':['stress']})
    cur=native.pending(ev)
    check(cur['request_sha256']==h and cur['kind']=='search','native host sees exact frozen search request')
    output={'receipts':[{'result_urls':['https://example.org/report'], 'result_contents':{'https://example.org/report':'Real text bytes from a test-only host fixture.'},'result_source_identities':{'https://example.org/report':'Example Publisher'},'engine':'NATIVE_HOST_TOOL'}]}
    bad_output={'receipts':[{'result_urls':['https://example.org/report'], 'result_contents':{},'result_source_identities':{},'engine':'NATIVE_HOST_TOOL'}]}
    f,t=submit_result(ev,'search',bad_output,'webCTX',call_id='SEARCH-1')
    expect_block(lambda:native.submit(ev,f,t),'ACTUAL_SEARCH_BYTES_AND_SOURCE_IDENTITY_REQUIRED')
    f,t=submit_result(ev,'search',output,'webCTX',call_id='SEARCH-1')
    tr=json.loads(t.read_text());tr['request_sha256']='0'*64;t.write_bytes(native.canonical(tr))
    expect_block(lambda:native.submit(ev,f,t),'HOST_TOOL_TRACE_MISSING_OR_NOT_BOUND_TO_BYTES')
    f,t=submit_result(ev,'search',output,'webCTX',call_id='SEARCH-1')
    r=native.submit(ev,f,t)
    check(r['submitted'] and r['provenance_level']=='HOST_RECORDED_NOT_PROVIDER_SIGNED','search response and honest provenance status')
    obj,raw,sh=source.wait_response('search',seq,stem,poll=0.01)
    check(obj['request_sha256']==h and obj['receipts'][0]['engine']=='NATIVE_HOST_TOOL','frozen bridge consumes submitted search response')
    expect_block(lambda:native.submit(ev,f,t),'NO_PENDING_REQUEST')
    # Valid generated structured payload is not a Research pass; only transport tested.
    seq,stem,path,h=source.request('model',{'request_type':'SEMANTIC_MODEL','actual_runtime_request':{'claim':'x'}})
    mod={'semantic_output':{'narrative':'test controlled sample','claims':[]},'provider_identity':'native-main',
         'model_identity':'model-a','provider_request_id':'MODEL-42','observed_at':'2026-10-08T00:00:00Z'}
    f,t=submit_result(ev,'model',mod,'primary-context',call_id='MODEL-42')
    native.submit(ev,f,t)
    obj,raw,sh=source.wait_response('model',seq,stem,poll=0.01)
    check(obj['semantic_output']['narrative']=='test controlled sample','model tool byte transport; no semantic claim')
    seq,stem,path,h=source.request('verification',{'request_type':'INDEPENDENT_VERIFICATION','claim_payload':{'x':1}})
    ver={'pass':False,'claim_entailment_result':'UNKNOWN','counterevidence_result':'UNKNOWN',
         'method_validation_result':'UNKNOWN','provider_identity':'native-checker',
         'model_identity':'model-b','provider_request_id':'VERIFY-12','observed_at':'2026-10-08T00:00:00Z'}
    f,t=submit_result(ev,'verification',ver,'primary-context',call_id='VERIFY-12')
    expect_block(lambda:native.submit(ev,f,t),'VERIFIER_CONTEXT_NOT_ISOLATED_FROM_PRODUCER')
    f,t=submit_result(ev,'verification',ver,'verifier-context',call_id='VERIFY-12')
    native.submit(ev,f,t)
    obj,raw,sh=source.wait_response('verification',seq,stem,poll=0.01)
    check(obj['pass'] is False,'independent-context negative verdict retained')
    check(not native.pending(ev)['pending'],'all requests consumed')
    led=(ev/'NATIVE_TOOL_CONTEXTS.jsonl').read_text()
    check(len(led.splitlines())==3, 'three trace records, no fabricated credential')
    check(not (ev/'FROZEN_HANDOFF/PRODUCT').joinpath('NATIVE_HOST_RAW').exists(),'all native evidence outside product')
print('ALL PASS',OK)
# Additional negative: pending file path cannot escape bridge evidence root.
with tempfile.TemporaryDirectory() as tmp:
    ev=pathlib.Path(tmp); store=bridge.EvidenceStore(ev/'R01_RAW_EVIDENCE/MODEL_BRIDGE')
    seq,stem,path,h=store.request('search',{'request_type':'OPEN_WORLD_SEARCH'})
    meta=ev/'R01_RAW_EVIDENCE/MODEL_BRIDGE/PENDING_REQUEST.json'
    pending_obj=json.loads(meta.read_text());pending_obj['expected_response_path']=str(ev/'evil.json')
    meta.write_bytes(native.canonical(pending_obj))
    expect_block(lambda:native.pending(ev),'PENDING_PATH_ESCAPES_BRIDGE_ROOT')
print('ALL PASS INCLUDING PATH-BOUNDARY',OK)
