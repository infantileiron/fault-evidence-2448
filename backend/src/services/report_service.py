import csv,io
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.review import EvidenceReview
from ..models.run import InferenceRun
from ..models.report import Report
def create(db,body):
 review=db.get(EvidenceReview,body.review_id)
 if not review or review.state!='approved':raise HTTPException(409,'须先批准证据复核')
 existing=db.scalar(select(Report).where(Report.review_id==review.id))
 if existing:return existing
 run=db.get(InferenceRun,review.run_id);row=Report(id=str(uuid4()),review_id=review.id,title=body.title,snapshot={'result':run.result,'action':review.action,'reviewer':review.reviewer});db.add(row);db.commit();return row
def export(row):
 r=row.snapshot['result'];a=r['analysis'];base=a['baseline'];out=io.StringIO();w=csv.writer(out);w.writerow(['record_type','node_id','state','probability','log_probability_ln','baseline_log_evidence_ln','baseline_evidence_probability','baseline_exp_underflow','branch_log_evidence_ln','entropy_bits','expected_entropy_bits','raw_ig_bits','ig_bits','micro_negative_clipped','version','input_sha256'])
 def emit(kind,node,state='',p='',lp='',entropy='',expected='',raw='',ig='',clipped='',logz=None):w.writerow([kind,node,state,p,lp,base['log_evidence'],base['evidence_probability'],base['evidence_probability_underflow'],'' if logz is None else logz,entropy,expected,raw,ig,clipped,r['version'],r['input_sha256']])
 for p in base['posterior']:emit('posterior',base['target'],p['state'],p['probability'],p['log_probability'],a['target_entropy'])
 for c in a['candidates']:
  emit('candidate',c['node_id'],entropy=c['prior_entropy'],expected=c['expected_entropy'],raw=c['raw_information_gain'],ig=c['information_gain'],clipped=c['micro_negative_clipped'])
  for b in c['branches']:emit('branch',c['node_id'],b['state'],b['probability'],b['log_probability'],b['conditional_entropy'],logz=b['inference']['log_evidence'] if b['inference'] else '')
 return '\ufeff'+out.getvalue()
