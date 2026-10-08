#!/usr/bin/env python3
"""Fresh-receiver verifier: outer inventory, frozen Product, and referenced kernel."""
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]

def sha(b):return hashlib.sha256(b).hexdigest()

def bad(msg):raise AssertionError(msg)

manifest=(ROOT/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
expected={}
for row in manifest:
    h,rel=row.split('  ',1)
    if rel in expected:bad('DUPLICATE_MANIFEST_ENTRY')
    expected[rel]=h
actual={str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file() and str(p.relative_to(ROOT)).replace('\\','/')!='MANIFEST.sha256'}
if actual!=set(expected):bad('INVENTORY_MISMATCH '+str((actual-set(expected),set(expected)-actual)))
for rel,h in expected.items():
    if sha((ROOT/rel).read_bytes())!=h:bad('HASH_MISMATCH '+rel)
    if rel.endswith(('.pyc','.pyo')) or '__pycache__' in rel:bad('BYTECODE_POLLUTION')
sys.path.insert(0,str(ROOT/'src'))
import native_host_bridge as bridge
info=bridge.verify_handoff(ROOT/'FROZEN_HANDOFF.zip')
with zipfile.ZipFile(ROOT/'FROZEN_HANDOFF.zip') as outer:
    p=next(m for m in outer.namelist() if m.startswith('PRODUCT/') and m.endswith('.zip'))
    with zipfile.ZipFile(io.BytesIO(outer.read(p))) as product:
        for rel in ['SKILL.md','kernel/constitution.yaml','kernel/node_registry.yaml',
                    'kernel/authority_registry.yaml','kernel/method_registry.yaml']:
            if product.read(rel)!=(ROOT/'PRODUCT_REFERENCE'/rel).read_bytes():
                bad('PRODUCT_REFERENCE_DRIFT '+rel)
print(json.dumps({'receiver_verdict':'PASS','manifest_items':len(expected),
                  'frozen_product_sha256':info['product_sha256'],
                  'host_native_integration_only':True,
                  'native_model_api_required':False,
                  'independent_research_publication_verified':False},ensure_ascii=False))
