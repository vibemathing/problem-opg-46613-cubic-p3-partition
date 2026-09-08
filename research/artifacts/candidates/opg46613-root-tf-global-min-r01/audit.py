#!/usr/bin/env python3
"""Physical simultaneous exchange traces and new-host activation tests."""
import hashlib,json,random,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from surgery import state,surgery,factor_from_state,minimal_hall,component_rows


def summary(st):return {k:st[k] for k in ('selected','s','D','u','tree_count','excess','nu','kappa')}


def primitive(g,st,e):
    if st['u'] or e in st['selected']:return None
    loc=[]
    for v in g['matching'][e]:
        found=[(j,h) for j,h in enumerate(st['gaps']) if v in h['path'][1:-1]]
        if len(found)!=1:return None
        j,h=found[0];a=h['path'].index(v);loc.append((j,h,((a-1)%3,(h['distance']-a-1)%3)))
    if loc[0][0]==loc[1][0]:return None
    comp={v:c for c in st['components'] for v in c['owners']}
    if st['kappa']==2 and st['tree_count']==st['excess']==1:
        for j in (0,1):
            tr,bc=loc[j],loc[1-j]
            if bc[1]['demand']!=1 or bc[2]!=(0,0) or sum(tr[2])-tr[1]['demand']!=2:continue
            participating={tr[1]['owners'][k] for k in (0,1) if tr[2][k]}
            if tr[1]['demand']:participating.update(tr[1]['owners'])
            tree=comp[next(iter(participating))];bike=comp[bc[1]['owners'][0]]
            if tree['excess']!=-1 or not participating.issubset(tree['owners']) or bike['excess']!=1:continue
            remain=[x['ends'] for i,x in enumerate(st['slots']) if i in bike['slots'] and x['gap']!=bc[0]]
            if len(component_rows(bike['owners'],remain))==1:return 'tree_bicycle_cycle_transfer'
    if st['kappa']==3 and st['tree_count']==0 and st['excess']==3:
        if all(h['demand']==1 and residues==(0,0) for j,h,residues in loc):
            gids={x[0] for x in loc};remain=[x['ends'] for x in st['slots'] if x['gap'] not in gids]
            cc=component_rows(st['selected'],remain)
            if all(c['excess']>=0 for c in cc) and sum(c['excess'] for c in cc)==1:return 'excess_three_to_tree_bicycle'
    if st['kappa']==3 and st['tree_count']==3 and st['excess']==0:
        if all(h['demand']==0 and residues==(1,1) for j,h,residues in loc):
            touched={v for j,h,r in loc for v in h['owners']}
            if all(touched.intersection(c['owners']) for c in st['components'] if c['excess']==-1):return 'three_tree_merge'
    return None


def main():
    raw=Path('../opg46613-root-tf-222-r01/objects.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='9f46cddde95da7e4956f17930f135cbc0870ca70db86345b7fef40df6b8e9bfd'
    controls=json.loads(raw);traces=[]
    for name,before,after in [('control24',[0,3],[0,2,3,4]),('new42',[0,3],[0,1,10,12])]:
        tr=surgery(controls[name],before,after);assert tr['delta_kappa']==-3
        tr['graph_ref']=name;tr['factor']=factor_from_state(controls[name],tr['after']);traces.append(tr)
    neutral=state(controls['control24'],[0,2,3]);assert neutral['kappa']==3
    rows=json.loads(Path('new-hosts.json').read_text())['cases'];sampled=[];activation=[];certificates=[];trees=[]
    for gi,entry in enumerate(rows):
        g=entry['graph'];m=len(g['matching']);rng=random.Random(entry['seed']+17)
        sets=[[],entry['selected'],list(range(m))]
        sets.extend([i for i in range(m) if rng.random()<p] for p in (.04,.08,.15,.25,.4,.65))
        sets.extend(sorted(set(entry['selected'])^{i}) for i in range(min(m,3)));seen=set()
        for selected in sets:
            if tuple(selected) in seen:continue
            seen.add(tuple(selected));st=state(g,selected)
            if st['u']==0:assert (st['excess']-st['tree_count'])%3==0 and st['kappa']!=1
            h=minimal_hall(st)
            if h is not None:certificates.append({'graph':gi,'selected':selected,'hall':h})
            sampled.append({'graph':gi,'state':summary(st)})
            if st['u']:
                bad=next(c for c in st['untouched'] if c['residue']);vertices=set(g['cycles'][bad['cycle']])
                for e,(a,b) in enumerate(g['matching']):
                    if a not in vertices and b not in vertices:continue
                    after=state(g,sorted(set(selected)|{e}));assert after['kappa']<st['kappa']
                    activation.append({'graph':gi,'selected':selected,'insert':e,'bad_cycle':bad['cycle'],'before':st['kappa'],'after':after['kappa']})
        if len(g['cycles'])==3 and all(len(c)%3==2 for c in g['cycles']):
            ci={v:i for i,c in enumerate(g['cycles']) for v in c};cross=[i for i,(a,b) in enumerate(g['matching']) if ci[a]!=ci[b]];selected=None
            for j,e in enumerate(cross):
                for f in cross[j+1:]:
                    if len({ci[v] for z in (e,f) for v in g['matching'][z]})==3:selected=[e,f];break
                if selected is not None:break
            st=state(g,selected);assert st['kappa'] in (0,3) and st['u']==0;trees.append({'graph':gi,'state':summary(st)})
    primitives=[]
    for entry in sampled+trees:
        gi=entry['graph'];g=rows[gi]['graph'];st=state(g,entry['state']['selected'])
        for e in range(len(g['matching'])):
            rule=primitive(g,st,e)
            if rule:
                after=state(g,sorted(set(st['selected'])|{e}));assert after['kappa']<st['kappa']
                primitives.append({'graph':gi,'selected':st['selected'],'insert':e,'rule':rule,'before':st['kappa'],'after':after['kappa']})
    primitives=list({(x['graph'],tuple(x['selected']),x['insert'],x['rule']):x for x in primitives}.values())
    out={'verdict':'candidate_only','source_sha256':hashlib.sha256(raw).hexdigest(),'controls':traces,'neutral_control24':neutral,
         'sampled_states':sampled,'activation_cases':activation,'hall_certificates':certificates,'two_edge_222_states':trees,'primitive_cases':primitives}
    text=json.dumps(out,sort_keys=True,separators=(',',':'))+'\n';Path('audit-data.json').write_text(text)
    print(json.dumps({'status':'PASS','verdict':'candidate_only','new_hosts':len(rows),'sampled_states':len(sampled),'activation_cases':len(activation),
                      'hall_certificates':len(certificates),'two_edge_222_cases':len(trees),'primitive_cases':len(primitives),'old_control_selected_sets':5,
                      'simultaneous_control_deltas':[x['delta_kappa'] for x in traces],'audit_data_sha256':hashlib.sha256(text.encode()).hexdigest(),
                      'global_positive_minimum_found':False,'old_censuses_repeated':False},sort_keys=True))

if __name__=='__main__':main()
