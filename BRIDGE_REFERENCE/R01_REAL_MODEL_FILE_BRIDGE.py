#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Profound Cognition V9 GPT6 RC14 provenance-corrective candidate — execution-only real-world R01 file bridge.

This harness is deliberately OUTSIDE the Product. It binds three real host capabilities to the
canonical Product runtime while recording the actual structured bytes visible to the execution
operator/model:
  SEARCH request -> host/web response -> SearchReceipt
  SEMANTIC request -> real model response -> ProviderCallResult
  VERIFICATION payload -> independent real-model verdict -> sealed production checker receipt

The harness never edits Product bytes. All bridge traffic and final result evidence are append-only
files under --evidence. Resource time is telemetry; no timeout is used as epistemic completion.
"""
from __future__ import print_function
import argparse, hashlib, json, os, pathlib, secrets, shutil, subprocess, sys, time, traceback, zipfile
sys.dont_write_bytecode = True


def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()


def canonical_bytes(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),default=str)+'\n').encode('utf-8')


def jsonable(obj):
    if obj is None or isinstance(obj,(str,int,float,bool)): return obj
    if isinstance(obj,dict): return {str(k):jsonable(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple,set)): return [jsonable(v) for v in obj]
    f=getattr(obj,'as_dict',None)
    if callable(f):
        try: return jsonable(f())
        except Exception: pass
    d=getattr(obj,'__dict__',None)
    if isinstance(d,dict): return {str(k):jsonable(v) for k,v in d.items() if not str(k).startswith('_')}
    return str(obj)


class EvidenceStore(object):
    """One process-run's immutable request/response transaction ledger.

    A crashed process's unresolved request remains historical evidence, not
    evidence that a later invocation contacted any model or verifier.
    """
    def __init__(self, root):
        self.root = pathlib.Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        # A fresh process MUST NOT recreate an old request filename even when
        # its sequence and payload digest match the previous process.
        self.run_id = secrets.token_hex(16)
        self.seq = {"model": 0, "search": 0, "verification": 0}
        self.issued = {}
        self.consumed = set()
        self.index = self.root / 'BRIDGE_INDEX.jsonl'
        for k in self.seq:
            (self.root / k / 'requests').mkdir(parents=True, exist_ok=True)
            (self.root / k / 'responses').mkdir(parents=True, exist_ok=True)
        self._record({'event': 'RUN_START', 'run_id': self.run_id,
                      'provenance': 'NEW_PROCESS_NO_AUTOMATIC_RESPONSE_REUSE'})

    def _record(self, event):
        with self.index.open('ab') as f:
            f.write(canonical_bytes(event))
            f.flush()
            os.fsync(f.fileno())

    def _next(self, kind):
        if kind not in self.seq:
            raise ValueError('BRIDGE_UNKNOWN_REQUEST_KIND')
        self.seq[kind] += 1
        return self.seq[kind]

    def request(self, kind, payload):
        seq = self._next(kind)
        # Make the actual model-visible request bytes invocation-specific, not
        # merely the filename. Otherwise copying an old response to the new
        # filename could satisfy an unchanged request digest.
        if not isinstance(payload, dict):
            raise TypeError('BRIDGE_REQUEST_PAYLOAD_MUST_BE_OBJECT')
        on_wire = dict(payload)
        if 'bridge_request_identity' in on_wire:
            raise ValueError('BRIDGE_RESERVED_REQUEST_IDENTITY')
        on_wire['bridge_request_identity'] = {
            'run_id': self.run_id, 'sequence': seq,
            'nonce': secrets.token_hex(16)}
        raw = canonical_bytes(on_wire)
        h = hashlib.sha256(raw).hexdigest()
        stem = '%s_%06d_%s' % (self.run_id, seq, h[:16])
        p = self.root / kind / 'requests' / (stem + '.json')
        # x+b prevents accidental rewrite even if paths collide. No silently
        # recycled model-visible bytes, request ids or previous responses.
        with p.open('xb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        self.issued[(kind, seq, stem)] = h
        expected_response = self.root / kind / 'responses' / (stem + '.json')
        pending = self.root / 'PENDING_REQUEST.json'
        pending.write_bytes(canonical_bytes({
            'kind': kind, 'run_id': self.run_id, 'seq': seq,
            'request_path': str(p), 'request_sha256': h,
            'expected_response_path': str(expected_response)}))
        self._record({'event': 'REQUEST', 'run_id': self.run_id, 'kind': kind,
                      'seq': seq, 'path': str(p.relative_to(self.root)), 'sha256': h})
        return seq, stem, p, h

    def wait_response(self, kind, seq, stem, poll=0.5):
        original_sha = self.issued.get((kind, seq, stem))
        if original_sha is None:
            raise RuntimeError('BRIDGE_REQUEST_NOT_ISSUED_BY_THIS_RUN')
        if (kind, seq, stem) in self.consumed:
            raise RuntimeError('BRIDGE_RESPONSE_ALREADY_CONSUMED_IN_THIS_RUN')
        p = self.root / kind / 'responses' / (stem + '.json')
        while not p.exists():
            time.sleep(poll)
        req = self.root / kind / 'requests' / (stem + '.json')
        if not req.is_file() or sha256_file(req) != original_sha:
            raise RuntimeError('BRIDGE_ORIGINAL_REQUEST_BYTES_CHANGED')
        raw = p.read_bytes()
        h = hashlib.sha256(raw).hexdigest()
        obj = json.loads(raw.decode('utf-8'))
        if not isinstance(obj, dict) or obj.get('request_sha256') != original_sha:
            raise RuntimeError('BRIDGE_RESPONSE_REQUEST_HASH_MISMATCH')
        self._record({'event': 'RESPONSE', 'run_id': self.run_id, 'kind': kind,
                      'seq': seq, 'path': str(p.relative_to(self.root)),
                      'request_sha256': original_sha, 'sha256': h})
        self.consumed.add((kind, seq, stem))
        pending = self.root / 'PENDING_REQUEST.json'
        try:
            cur = json.loads(pending.read_text())
            if (cur.get('kind') == kind and cur.get('seq') == seq and
                    cur.get('run_id') == self.run_id and
                    cur.get('request_sha256') == original_sha):
                pending.unlink()
        except FileNotFoundError:
            pass
        return obj, raw, h


def prepare_fresh_product(product_zip, expected_sha, evidence_root):
    product_zip=pathlib.Path(product_zip).resolve(); ev=pathlib.Path(evidence_root).resolve()
    actual=sha256_file(product_zip)
    if expected_sha and actual.lower()!=str(expected_sha).strip().lower():
        raise RuntimeError('PRODUCT_SHA256_MISMATCH expected=%s actual=%s'%(expected_sha,actual))
    root=ev/'FRESH_PRODUCT'
    if root.exists(): shutil.rmtree(str(root))
    root.mkdir(parents=True)
    with zipfile.ZipFile(str(product_zip)) as zf: zf.extractall(str(root))
    def runcheck(parts):
        r=subprocess.run([sys.executable,'-B']+parts,cwd=str(root),capture_output=True,text=True,encoding='utf-8')
        return {'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    manifest=runcheck(['verify_manifest.py','--root','.','--manifest','./PACKAGE_MANIFEST.sha256'])
    version=runcheck(['scripts/version-consistency-check.py'])
    identity={'product_zip':str(product_zip),'product_zip_sha256':actual,'expected_sha256':expected_sha,'manifest_precheck':manifest,'version_precheck':version}
    (ev/'PRODUCT_IDENTITY_PRE.json').write_bytes(canonical_bytes(identity))
    if manifest['rc']!=0 or version['rc']!=0:
        raise RuntimeError('fresh Product identity/precheck failed')
    return root,actual


def verify_product_post(product_root,evidence_root):
    r=subprocess.run([sys.executable,'-B','verify_manifest.py','--root','.','--manifest','./PACKAGE_MANIFEST.sha256'],cwd=str(product_root),capture_output=True,text=True,encoding='utf-8')
    out={'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    pathlib.Path(evidence_root,'PRODUCT_IDENTITY_POST.json').write_bytes(canonical_bytes(out))
    if r.returncode!=0: raise RuntimeError('Product bytes changed during execution (manifest POSTCHECK failed)')
    return out

def load_runtime(product_root):
    root=str(pathlib.Path(product_root).resolve()); runtime=os.path.join(root,'runtime')
    sys.path[:0]=[root,runtime]
    import mainline
    from adapters.model_adapter import HostModelAdapter
    from semantic_producer import ProviderCallResult
    from search_provider import SearchProvider, PROVIDER_AVAILABLE
    from search_ledger import SearchReceipt
    from verification_engine import VerificationEngine
    return mainline,HostModelAdapter,ProviderCallResult,SearchProvider,PROVIDER_AVAILABLE,SearchReceipt,VerificationEngine


def model_request_payload(req):
    d=jsonable(req)
    return {
      "request_type":"SEMANTIC_MODEL",
      "actual_runtime_request":d,
      "execution_instruction":"Use a real model to answer ONLY this request. Return a structured semantic_output object. Ground every derived claim in material/source bindings supplied by the request. Never invent evidence IDs, material IDs, source identities or capability completion. If producer_policy contains capability_execution_contract, execute every declared procedure step and populate capability_execution with non-echo derived results linked to grounded claim_ids.",
      "response_contract":{"semantic_output":"object accepted by ModelBackedSemanticProducer","provider_identity":"real provider id","model_identity":"real model id","usage":"optional telemetry","latency":"optional telemetry","retries":"optional telemetry"}
    }


def build(product_root,evidence_root):
    ML,HostModelAdapter,ProviderCallResult,SearchProvider,PROVIDER_AVAILABLE,SearchReceipt,VerificationEngine=load_runtime(product_root)
    from search_provider import sign_receipt as _sign_search_receipt
    store=EvidenceStore(evidence_root)
    declared={
        'model_provider':os.environ.get('PC_R01_MODEL_PROVIDER','').strip(),
        'model_id':os.environ.get('PC_R01_MODEL_ID','').strip(),
        'verifier_provider':os.environ.get('PC_R01_VERIFIER_PROVIDER','').strip(),
        'verifier_model':os.environ.get('PC_R01_VERIFIER_MODEL','').strip(),
    }
    if not all(declared.values()):
        raise RuntimeError('R01_REAL_PROVIDER_AND_VERIFIER_IDENTITIES_REQUIRED')
    if declared['model_provider']==declared['verifier_provider']:
        raise RuntimeError('R01_INDEPENDENT_VERIFIER_REQUIRES_DIFFERENT_PROVIDER')
    (store.root/'DECLARED_EXTERNAL_IDENTITIES.json').write_bytes(canonical_bytes({
        'identities':declared,'provenance_level':'OPERATOR_DECLARED_NOT_PROVIDER_ATTESTED'}))

    class BridgeModelCallable(object):
        def __call__(self,request):
            payload=model_request_payload(request); seq,stem,_,_=store.request('model',payload)
            obj,raw,_=store.wait_response('model',seq,stem)
            semantic=obj.get('semantic_output')
            if not isinstance(semantic,dict): raise RuntimeError('model response requires semantic_output object')
            if obj.get('provider_identity')!=declared['model_provider'] or obj.get('model_identity')!=declared['model_id']:
                raise RuntimeError('R01_MODEL_IDENTITY_MISMATCH_OR_MISSING')
            if not obj.get('provider_request_id') or not obj.get('observed_at'):
                raise RuntimeError('R01_MODEL_ORIGIN_TRACE_MISSING')
            return ProviderCallResult(text=json.dumps(semantic,ensure_ascii=False),
                provider_identity=obj['provider_identity'],
                model_identity=obj['model_identity'],
                usage=obj.get('usage') or {}, latency=obj.get('latency'), retries=obj.get('retries'), raw=obj)

    class BridgeSearchProvider(SearchProvider):
        def __init__(self):
            SearchProvider.__init__(self,'pc-r01-real-search',availability=PROVIDER_AVAILABLE,signature_key=_host_search_signing_key())
        def search(self,queries,context=None):
            payload={"request_type":"OPEN_WORLD_SEARCH","queries":list(queries or []),"context":jsonable(context or {}),
                     "execution_instruction":"Perform fresh real web/search retrieval for every query/obligation. Return substantive source text, real URLs, and canonical source identities at publisher/organization/study-family/dataset-origin level. URL host alone is not a source identity. Do not use expected-answer hints or historical R01 outputs.",
                     "response_contract":{"receipts":[{"result_urls":["real URL"],"result_contents":{"URL":"retrieved text"},"result_source_identities":{"URL":"publisher/org/study/dataset identity"},"engine":"real search engine/provider"}]}}
            seq,stem,_,_=store.request('search',payload); obj,raw,_=store.wait_response('search',seq,stem)
            out=[]
            for r in obj.get('receipts') or []:
                urls=r.get('result_urls') or []
                origins=r.get('result_source_identities') or {}
                contents=r.get('result_contents') or {}
                if not urls or not (r.get('engine') or obj.get('engine')):
                    raise RuntimeError('R01_SEARCH_SOURCE_OR_PROVIDER_MISSING')
                if any(not origins.get(url) or not contents.get(url) for url in urls):
                    raise RuntimeError('R01_SEARCH_ORIGIN_AND_BYTES_REQUIRED_FOR_EVERY_URL')
                # Source identity is supplied by the operator. It is NOT independently
                # established merely because the host provided a string.
                out.append(_sign_search_receipt(SearchReceipt(queries=list(queries or []),result_urls=urls,result_contents=contents,result_source_identities=origins,engine=r.get('engine') or obj['engine']),self.signature_key))
            return out

    model_callable=BridgeModelCallable()
    adapter=HostModelAdapter(callable_=model_callable,provider_identity=declared['model_provider'],model_identity=declared['model_id'])
    ML.bootstrap_production_runtime(adapter=adapter,description={"purpose":"R01 real-world execution-only evidence bridge"})

    engine=VerificationEngine(); checker_id='pc-r01-real-independent-verifier-v1'
    def checker_fn(payload,inputs=None):
        kind=(payload or {}).get('object_type') if isinstance(payload,dict) else None
        if kind=='CAPABILITY_STRUCTURAL_NA':
            instructions=('Independently challenge the full capability contract and current question. '
                'Try semantically plausible application objects and counterexamples, including paraphrases. '
                'A missing keyword is not evidence of structural non-applicability. '
                'Only return PASS when NO legitimate application object exists within the exact scoped problem. '
                'Provide considered_applications and a specific reason; use UNKNOWN if uncertain.')
            contract={"pass":"boolean","structural_nonapplicability_result":"PASS|FAIL|UNKNOWN",
                      "counterexample_challenge_result":"PASS|FAIL|UNKNOWN",
                      "method_validation_result":"PASS|FAIL|UNKNOWN",
                      "reason":"specific independent reasoning, at least 24 chars",
                      "considered_applications":["concrete alternative or counterexample tested"]}
            required=('structural_nonapplicability_result','counterexample_challenge_result','method_validation_result')
        elif kind=='CAPABILITY_EXHAUSTION':
            instructions=('Independently inspect each actually tested alternative and referenced fresh source. '
                'A search receipt proves an attempt, not epistemic exhaustion. '
                'Confirm that material counterevidence, alternative paths and remaining discoverable sources '
                'were considered. If any important route remains, return UNKNOWN/FAIL; never assert global impossibility.')
            contract={"pass":"boolean","exhaustion_result":"PASS|FAIL|UNKNOWN",
                      "counterevidence_result":"PASS|FAIL|UNKNOWN",
                      "method_validation_result":"PASS|FAIL|UNKNOWN","reason":"bounded exhaustion rationale"}
            required=('exhaustion_result','counterevidence_result','method_validation_result')
        else:
            instructions=('Independently verify the exact claim/method against real grounded source bytes '
                'and the specified capability contract. Do not self-certify or rubber-stamp.')
            contract={"pass":"boolean","detail":"reasoned verification summary",
                      "claim_entailment_result":"PASS|FAIL|UNKNOWN",
                      "counterevidence_result":"PASS|FAIL|UNKNOWN",
                      "method_validation_result":"PASS|FAIL|UNKNOWN"}
            required=('claim_entailment_result','counterevidence_result','method_validation_result')
        req={"request_type":"INDEPENDENT_VERIFICATION","verification_object_type":kind or 'CLAIM_OR_METHOD',
             "claim_payload":jsonable(payload),"input_objects":jsonable(inputs or []),
             "execution_instruction":instructions,"response_contract":contract}
        seq,stem,_,_=store.request('verification',req); obj,raw,_=store.wait_response('verification',seq,stem)
        if (obj.get('provider_identity')!=declared['verifier_provider'] or
                obj.get('model_identity')!=declared['verifier_model'] or
                not obj.get('provider_request_id') or not obj.get('observed_at')):
            raise RuntimeError('R01_VERIFIER_ORIGIN_AND_INDEPENDENCE_TRACE_MISSING')
        if type(obj.get('pass')) is not bool:
            raise RuntimeError('R01_VERIFIER_EXPLICIT_BOOLEAN_VERDICT_REQUIRED')
        if obj.get('pass') and any(obj.get(x)!='PASS' for x in required):
            raise RuntimeError('R01_VERIFIER_PASS_WITH_INCOMPLETE_EPISTEMIC_CHECK')
        if kind=='CAPABILITY_STRUCTURAL_NA' and obj.get('pass'):
            if (not isinstance(obj.get('considered_applications'),list) or
                    not obj['considered_applications'] or
                    len(str(obj.get('reason') or '').strip())<24):
                raise RuntimeError('R01_STRUCTURAL_NA_REQUIRES_ACTUAL_SEMANTIC_CHALLENGE')
        return {k:v for k,v in obj.items() if k not in
                ('request_sha256','provider_identity','model_identity','provider_request_id',
                 'observed_at','usage','latency','retries')}
    engine.registry.register(checker_id,version='1.0',description='Operator-declared external independent verifier (provider provenance not cryptographically attested)',role='production',checker_fn=checker_fn)
    engine.registry.seal()
    return ML,adapter,BridgeSearchProvider(),engine,checker_id,store


def selftest():
    import tempfile
    d=tempfile.mkdtemp(prefix='pc_r01_bridge_selftest_'); st=EvidenceStore(d)
    seq,stem,p,h=st.request('model',{'hello':'world'}); rp=st.root/'model'/'responses'/(stem+'.json'); rp.write_text(json.dumps({'request_sha256':h,'semantic_output':{'narrative':'x','claims':[]}}))
    obj,raw,rh=st.wait_response('model',seq,stem)
    assert obj['semantic_output']['narrative']=='x' and not (st.root/'PENDING_REQUEST.json').exists()
    # Missing key must fail closed; a sufficiently long host-supplied key is accepted.
    previous=os.environ.pop('PC_R01_SEARCH_SIGNING_KEY',None)
    try:
        try: _host_search_signing_key()
        except RuntimeError: pass
        else: raise AssertionError('missing search key accepted')
        os.environ['PC_R01_SEARCH_SIGNING_KEY']='H'*64
        assert _host_search_signing_key() == 'H'*64
    finally:
        if previous is None: os.environ.pop('PC_R01_SEARCH_SIGNING_KEY',None)
        else: os.environ['PC_R01_SEARCH_SIGNING_KEY']=previous
    print(json.dumps({'selftest':'PASS','request_sha256':h,'response_sha256':rh,'root':d},ensure_ascii=False))


def _host_search_signing_key():
    """Host-managed secret; never write it to Product, Handoff or trace files."""
    key = os.environ.get('PC_R01_SEARCH_SIGNING_KEY', '')
    if len(key) < 32:
        raise RuntimeError('R01_HOST_SEARCH_SIGNING_SECRET_REQUIRED_MIN_32_CHARS')
    return key


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--product-root'); ap.add_argument('--product-zip'); ap.add_argument('--expected-product-sha256'); ap.add_argument('--evidence',default='./R01_RAW_EVIDENCE'); ap.add_argument('--question',default='为什么飞机客舱的窗户通常是圆角而不是方角？'); ap.add_argument('--output-profile',default='STANDARD_REPORT'); ap.add_argument('--selftest',action='store_true'); ap.add_argument('--checkpoint'); ap.add_argument('--resume-checkpoint',action='store_true')
    a=ap.parse_args()
    if a.selftest: selftest(); return
    ev=pathlib.Path(a.evidence).resolve(); ev.mkdir(parents=True,exist_ok=True)
    if a.product_zip:
        product_root,_=prepare_fresh_product(a.product_zip,a.expected_product_sha256,str(ev))
    elif a.product_root:
        product_root=pathlib.Path(a.product_root).resolve()
    else:
        raise SystemExit('--product-zip (preferred) or --product-root required')
    try:
        ML,adapter,search,engine,checker_id,store=build(str(product_root),str(ev/'MODEL_BRIDGE'))
        journal = str(pathlib.Path(a.checkpoint).resolve()) if a.checkpoint else str(ev/'SOURCE_REENTRY_CHECKPOINT.json')
        result=ML.execute_problem(a.question,verification_engine=engine,checker_id=checker_id,
            host_binding={'adapter':adapter},search_provider=search,output_profile=a.output_profile,
            checkpoint_path=journal,resume_checkpoint=a.resume_checkpoint)
        (ev/'FINAL_RESULT.json').write_bytes(canonical_bytes(jsonable(result)))
        terminal={"frozen":result.get('frozen'),"snapshot_id":result.get('snapshot_id'),"snapshot_hash":result.get('snapshot_hash'),"publication_state":result.get('publication_state'),"memory_committed":result.get('memory_committed'),"verification_status":result.get('verification_status'),"stages":result.get('stages'),"publication_freeze":jsonable(result.get('publication_freeze')),"freeze_veto":jsonable(result.get('freeze_veto'))}
        (ev/'TERMINAL_STATE.json').write_bytes(canonical_bytes(terminal))
        if a.product_zip: verify_product_post(product_root,str(ev))
        print(json.dumps(terminal,ensure_ascii=False,indent=2))
    except BaseException as exc:
        (ev/'HARNESS_EXCEPTION.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise

if __name__=='__main__': main()
