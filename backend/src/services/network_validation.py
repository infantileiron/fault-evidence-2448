import math,re,itertools

def validate_network(nodes):
 if not isinstance(nodes,list) or not 1<=len(nodes)<=10 or any(not isinstance(n,dict) for n in nodes):raise ValueError('网络须含1–10个二元节点对象')
 clean=[];ids=[]
 for node in nodes:
  ident=node.get('node_id','');parents=node.get('parents',[])
  if not isinstance(ident,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,31}',ident) or ident in ids:raise ValueError('节点ID非法或重复')
  if not isinstance(parents,list) or any(not isinstance(p,str) for p in parents) or len(parents)>4 or len(set(parents))!=len(parents) or ident in parents:raise ValueError('父节点重复、自环、非法或超过4个')
  ids.append(ident);clean.append({'node_id':ident,'label':str(node.get('label') or ident),'parents':list(parents)})
 for node in clean:
  if any(parent not in ids for parent in node['parents']):raise ValueError('存在未知父节点')
 remaining={node['node_id']:set(node['parents']) for node in clean};order=[]
 while remaining:
  ready=sorted(ident for ident,parents in remaining.items() if not parents)
  if not ready:raise ValueError('网络必须无环')
  for ident in ready:order.append(ident);remaining.pop(ident)
  for parents in remaining.values():parents.difference_update(ready)
 return {'nodes':clean,'topological_order':order}

def validate_cpt(nodes,rows):
 nodes=validate_network(nodes)['nodes'];lookup={n['node_id']:n for n in nodes};clean=[];seen=set()
 if not isinstance(rows,list) or any(not isinstance(r,dict) for r in rows):raise ValueError('CPT须为配置行对象列表')
 for row in rows:
  ident=row.get('node_id');values=row.get('parent_values',[])
  if ident not in lookup:raise ValueError('CPT含未知节点')
  if not isinstance(values,list) or len(values)!=len(lookup[ident]['parents']) or any(type(v) is not int or v not in (0,1) for v in values):raise ValueError('父配置须按父节点顺序使用0/1')
  key=(ident,tuple(values))
  if key in seen:raise ValueError('CPT父配置重复')
  seen.add(key);probabilities=[]
  for field in ['p0','p1']:
   value=row.get(field)
   if isinstance(value,bool):raise ValueError('CPT概率须为有限数')
   try:value=float(value)
   except (ValueError,TypeError):raise ValueError('CPT概率须为有限数')
   if not math.isfinite(value) or not 0<=value<=1:raise ValueError('CPT概率须在[0,1]且有限')
   probabilities.append(value)
  total=math.fsum(probabilities)
  if abs(total-1)>1e-12:raise ValueError('每个父配置p0+p1须等于1（容差1e-12）')
  clean.append({'node_id':ident,'parent_values':values,'p0':probabilities[0],'p1':probabilities[1],'row_sum':total})
 expected={(n['node_id'],tuple(values)) for n in nodes for values in itertools.product([0,1],repeat=len(n['parents']))}
 if seen!=expected:raise ValueError('CPT须完整覆盖每个节点的所有父配置')
 return sorted(clean,key=lambda r:(r['node_id'],r['parent_values']))

def validate_evidence(nodes,evidence,target,candidates=None):
 ids={n['node_id'] for n in validate_network(nodes)['nodes']}
 if target not in ids:raise ValueError('查询目标未知')
 if not isinstance(evidence,dict) or any(k not in ids or type(v) is not int or v not in (0,1) for k,v in evidence.items()):raise ValueError('证据须为已知节点的二元0/1映射')
 eligible=sorted(ids-set(evidence)-{target})
 if candidates is not None:
  if not isinstance(candidates,list) or any(not isinstance(c,str) for c in candidates) or len(set(candidates))!=len(candidates) or any(c not in eligible for c in candidates):raise ValueError('候选须为未观测的非目标节点且不重复')
  eligible=sorted(candidates)
 return eligible
