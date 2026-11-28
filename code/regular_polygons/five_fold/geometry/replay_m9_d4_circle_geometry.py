#!/usr/bin/env python3
"""Complete exact 4D/9-facet geometry overcover for at least 22 shadow corners.

This uses published completeness cardinality 1142. All corresponding
integer realizations and pairwise nonisomorphism are checked afresh. Two
independent half-plane enumerators agree type by type before the connected
polygon cycles are extracted. No metric circle test occurs in this stage.
"""
from pathlib import Path
from collections import Counter
import subprocess,sys,hashlib,json,time

H=Path(__file__).resolve().parent
CODE=H/'CODE';CERT=H/'CERTIFICATES'
sys.path.insert(0,str(CODE))
from r2_geom_catalog4 import supports
from r2_geom_catalog_audit import audit

start=time.monotonic();data=[]
for line in (CERT/'r2_geom_4d_integer_all.txt').read_text().splitlines():
    ident,*v=line.split();a=list(map(int,v));assert len(a)==36
    F=supports([a[4*i:4*i+4] for i in range(9)])
    assert F and all(any(f>>i&1 for f in F) for i in range(9))
    data.append((ident,F))
assert len(data)==1142
hist=audit(data)
print('exact integer realizations and pairwise nonisomorphism',dict(sorted(hist.items())),flush=True)
selected=[(ident,F) for ident,F in data if len(F)>=22];assert len(selected)==855
(H/'m9_d4_f22plus.txt').write_text(''.join(' '.join(map(str,[ident,len(F),*F]))+'\n' for ident,F in selected))
bin_dir=H/'m9_geometry_bin';bin_dir.mkdir(exist_ok=True)
for name in ['r2_geom_shadows','r2_geom_audit']:
    subprocess.run(['g++','-O3','-std=c++17',str(CODE/(name+'.cpp')),'-o',str(bin_dir/name)],check=True)
with (H/'m9_d4_shadow22_counts.txt').open('wb') as out,(H/'m9_d4_shadow22_stderr.txt').open('wb') as err:
    subprocess.run([str(bin_dir/'r2_geom_shadows'),str(H/'m9_d4_f22plus.txt'),str(H/'m9_d4_shadow22_sweeps.txt'),'22'],stdout=out,stderr=err,check=True)
with (H/'m9_d4_shadow22_independent_counts.txt').open('wb') as out,(H/'m9_d4_shadow22_independent_stderr.txt').open('wb') as err:
    subprocess.run([str(bin_dir/'r2_geom_audit'),str(H/'m9_d4_f22plus.txt'),'22'],stdout=out,stderr=err,check=True)
A={s[0]:list(map(int,s[1:])) for row in (H/'m9_d4_shadow22_counts.txt').read_text().splitlines() if (s:=row.split())}
B={s[0]:list(map(int,s[1:])) for row in (H/'m9_d4_shadow22_independent_counts.txt').read_text().splitlines() if (s:=row.split())}
assert len(A)==len(B)==855 and set(A)==set(B)
assert all(A[i][0]==B[i][0] and 2*A[i][2]==B[i][1] for i in A)
assert sum(v[2] for v in A.values())==1042 and sum(v[3] for v in A.values())==1038
assert max(v[4] for v in A.values())==24
subprocess.run([sys.executable,str(H/'extract_m9_d4_shadow22.py')],stdout=subprocess.DEVNULL,check=True)
extracted=json.loads((H/'m9_d4_shadow22_manifest.json').read_text())
assert extracted['sweep_histogram']=={'22':1006,'23':14,'24':18}
assert extracted['template_histogram']=={'22':357,'23':4,'24':3}
inputs=[CERT/'r2_geom_4d_integer_all.txt']+[CODE/f for f in ['r2_geom_catalog4.py','r2_geom_catalog_audit.py','r2_geom_facets.py','r2_geom_shadows.cpp','r2_geom_audit.cpp']]+[H/'extract_m9_d4_shadow22.py',Path(__file__)]
outputs=[H/f for f in ['m9_d4_f22plus.txt','m9_d4_shadow22_counts.txt','m9_d4_shadow22_sweeps.txt','m9_d4_shadow22_independent_counts.txt','m9_d4_shadow22_templates.txt']]
result={'verified':True,'external_complete_census_cardinality':1142,'included_types':855,'signed_orders':2983680,
        'first_valid_sweeps':1042,'second_valid_sweeps':2084,'connected_sweeps':1038,
        'template_histogram':extracted['template_histogram'],'seconds':time.monotonic()-start,
        'input_sha256':{str(p.relative_to(H)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}}
(H/'m9_d4_geometry_verified.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
