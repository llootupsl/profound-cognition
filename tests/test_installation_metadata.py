#!/usr/bin/env python3
"""Local, no-network Agent Skills root-frontmatter conformity check."""
from pathlib import Path
import re
import yaml

root=Path(__file__).resolve().parents[1]
raw=(root/'SKILL.md').read_text(encoding='utf-8')
assert raw.startswith('---\n')
front, sep, body=raw[4:].partition('\n---\n')
assert sep and body.strip(), 'MISSING_FRONTMATTER_OR_BODY'
meta=yaml.safe_load(front)
assert isinstance(meta, dict)
allowed={'name','description','license','compatibility','metadata','allowed-tools'}
assert set(meta).issubset(allowed), f'UNSUPPORTED_FIELDS:{set(meta)-allowed}'
assert {'name','description'}.issubset(meta)
assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['name'])
assert len(meta['name']) <= 64
assert meta['name']=='profound-cognition', 'INSTALL_DIRECTORY_NAME_CONTRACT'
assert isinstance(meta['description'],str) and 1 <= len(meta['description']) <= 1024
assert 'Agent' in meta['description'] and '深度研究' in meta['description']
assert isinstance(meta.get('compatibility'),str) and len(meta['compatibility']) <= 500
assert isinstance(meta.get('metadata'),dict) and all(isinstance(k,str) and isinstance(v,str) for k,v in meta['metadata'].items())
assert (root/'FROZEN_HANDOFF.zip').is_file()
assert (root/'src/native_host_bridge.py').is_file()
print('AGENT_SKILLS_FRONTMATTER_CONTRACT=PASS')
print('REQUIRED=name,description; ALLOWED_FIELDS_ONLY=PASS; NAME_MATCHES_INSTALL_DIR=PASS')
