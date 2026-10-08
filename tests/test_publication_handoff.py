#!/usr/bin/env python3
"""Synthetic byte/integrity contract tests ONLY; not a research E2E/independent reviewer."""
from pathlib import Path
import copy, hashlib, json, os, sys, tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from publication_handoff import sha,validate_native_delivery,stage_delivery

def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)

def expect(code,func):
    try: func()
    except Exception as e:
        assert code in str(e),(code,str(e))
    else: raise AssertionError('EXPECTED_FAIL:'+code)

with tempfile.TemporaryDirectory(prefix='pc_publication_receiving_') as td:
    root=Path(td)/'run'; raw=root/'NATIVE_RUN_EVIDENCE'
    (root).mkdir(parents=True)
    meta={'run_scope':'USER_RESEARCH','raw_evidence_dir':'NATIVE_RUN_EVIDENCE'}
    write(root/'NATIVE_HOST_PROCESS.json',json.dumps(meta).encode())
    arts=raw/'_runtime_artifacts'/'publication'/'STANDARD_REPORT'
    arts.mkdir(parents=True)
    import fitz
    pdf=fitz.open(); page=pdf.new_page(); page.insert_text((70,70),'Genuine parser-readable PDF document'); pdf.save(str(arts/'publication.pdf'));pdf.close()
    from docx import Document
    doc=Document();doc.add_paragraph('Genuine OOXML document');doc.save(arts/'publication.docx')
    write(arts/'publication.html',b'<html><body><h1>Verified product publication</h1></body></html>')
    files={}
    for fmt in ['pdf','docx','html']:
        p=arts/('publication.'+fmt);files[fmt]={'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'status':'RENDERED'}
    final={'frozen':True,'snapshot_id':'snap-1','snapshot_hash':'a'*64,'publication_state':'PUBLISHED',
           'commit_state':'COMMITTED','memory_committed':True,
           'publication_freeze':{'state':'PUBLICATION_FROZEN'},
           'publication_artifacts':{'artifacts':files,'verify':{'status':'VERIFIED','publication_freeze_pdf':True}}}
    terminal={k:final[k] for k in ('frozen','snapshot_id','snapshot_hash','publication_state')}
    fp=raw/'FINAL_RESULT.json';tp=raw/'TERMINAL_STATE.json'
    def save():
        write(fp,json.dumps(final).encode());write(tp,json.dumps(terminal).encode())
    entries=[]; bridge_events=[]; ids={}
    for kind,context in [('search','ctx-search'),('model','ctx-primary'),('verification','ctx-independent')]:
        request_raw=json.dumps({'kind':kind,'model_visible_fixture':True},sort_keys=True).encode()
        digest=sha(request_raw); ids[kind]=digest
        req_rel=f'{kind}/requests/{kind}.json';resp_rel=f'{kind}/responses/{kind}.json'
        write(raw/'MODEL_BRIDGE'/req_rel,request_raw)
        rb=json.dumps({'real_host_returned':'fixture','kind':kind}).encode()
        tid='observed-fixture-'+kind
        trace={'request_sha256':digest,'result_sha256':sha(rb),'kind':kind,'host_tool_call_id':tid,'host_context_id':context}
        write(raw/'NATIVE_HOST_RAW'/(digest+'.json'),rb)
        write(raw/'NATIVE_HOST_TRACE'/(digest+'.json'),json.dumps(trace).encode())
        wrapped=dict(json.loads(rb));wrapped['request_sha256']=digest
        response_bytes=json.dumps(wrapped,sort_keys=True).encode()
        write(raw/'MODEL_BRIDGE'/resp_rel,response_bytes)
        bridge_events.extend([{'event':'REQUEST','kind':kind,'sha256':digest,'path':req_rel},
                              {'event':'RESPONSE','kind':kind,'request_sha256':digest,
                               'sha256':sha(response_bytes),'path':resp_rel}])
        entries.append({'kind':kind,'request_sha256':digest,'result_sha256':sha(rb),'host_context_id':context,'host_tool_call_id':tid})
    ledger=raw/'NATIVE_TOOL_CONTEXTS.jsonl'
    def put_entries():write(ledger,('\n'.join(json.dumps(x) for x in entries)+'\n').encode())
    put_entries();save()
    write(raw/'MODEL_BRIDGE'/'BRIDGE_INDEX.jsonl', ('\n'.join(json.dumps(x) for x in bridge_events)+'\n').encode())
    dst=Path(td)/'delivered'
    result=stage_delivery(root,dst)
    assert result['NOT_RELEASE'] is True
    assert all((dst/('publication.'+f)).read_bytes()==(arts/('publication.'+f)).read_bytes() for f in ('pdf','docx','html'))
    expect('DELIVERY_PATH_ALREADY_EXISTS',lambda:stage_delivery(root,dst))
    final['frozen']=False;save();expect('CANONICAL_PRODUCT_NOT_PUBLISHED',lambda:validate_native_delivery(root))
    final['frozen']=True;final['publication_freeze']['state']='PUBLICATION_FREEZE_BLOCKED';save();expect('PUBLICATION_FREEZE_MISSING',lambda:validate_native_delivery(root))
    final['publication_freeze']['state']='PUBLICATION_FROZEN';save()
    blob=(arts/'publication.docx').read_bytes(); (arts/'publication.docx').write_bytes(blob+b'TAMPER');expect('PUBLICATION_ARTIFACT_BYTES_MISSING',lambda:validate_native_delivery(root))
    (arts/'publication.docx').write_bytes(blob)
    html=(arts/'publication.html').read_bytes();(arts/'publication.html').write_bytes(b'MUTATION'+html);expect('PUBLICATION_ARTIFACT_BYTES_MISSING',lambda:validate_native_delivery(root))
    (arts/'publication.html').write_bytes(html)
    entries[0]['result_sha256']='0'*64;put_entries();expect('HOST_RAW_BYTES_CHANGED',lambda:validate_native_delivery(root))
    entries[0]['result_sha256']=sha((raw/'NATIVE_HOST_RAW'/(ids['search']+'.json')).read_bytes());put_entries()
    entries[2]['host_context_id']='ctx-primary';put_entries();expect('HOST_PROVENANCE_LEDGER_DISAGREES',lambda:validate_native_delivery(root))
    entries[2]['host_context_id']='ctx-independent';put_entries()
    req=raw/'MODEL_BRIDGE'/'search'/'requests'/'search.json'
    actual_req=req.read_bytes();req.write_bytes(actual_req+b'TAMPER')
    expect('MODEL_VISIBLE_REQUEST_BYTES_MISSING_OR_CHANGED',lambda:validate_native_delivery(root))
    req.write_bytes(actual_req)
    rbpath=raw/'MODEL_BRIDGE'/'model'/'responses'/'model.json'
    response_good=rbpath.read_bytes();rbpath.write_bytes(response_good+b'TAMPER')
    expect('BRIDGE_CONSUMED_RESPONSE_BYTES_MISSING_OR_CHANGED',lambda:validate_native_delivery(root))
    rbpath.write_bytes(response_good)
    d=json.loads(fp.read_text());d['publication_artifacts']['artifacts']['pdf']['path']='/tmp/outside.pdf';write(fp,json.dumps(d).encode())
    expect('PATH_OUTSIDE_RUN_OR_SYMLINK',lambda:validate_native_delivery(root))
    save()
    assert validate_native_delivery(root)['tool_calls']==3
    print('PASS: 12 controlled delivery contract checks; NOT an independent research/publication E2E')
