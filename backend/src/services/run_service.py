import json,hashlib
from uuid import uuid4
from fastapi import HTTPException
from ..models.run import InferenceRun
from ..models.case import EvidenceCase
from ..models.revision import CptRevision
from ..models.network import BayesNetwork
from ..models.posterior_state import PosteriorState
from ..models.candidate_metric import CandidateMetric
from ..models.branch_metric import BranchMetric
from ..models.elimination_step import EliminationStep
from ..utils.queue import enqueue
from .network_service import nodes
from .revision_service import rows
from .information_gain import information_gain
def create(db,body):
 if not db.get(EvidenceCase,body.case_id):raise HTTPException(422,'证据案例不存在')
 row=InferenceRun(id=str(uuid4()),case_id=body.case_id,status='queued',result={},error='');db.add(row);db.commit()
 try:enqueue(row.id)
 except Exception:
  row.status='failed';row.error='Redis队列不可用，请重试';db.commit();raise HTTPException(503,row.error)
 return row
def compute(db,ident):
 row=db.get(InferenceRun,ident)
 if not row or row.status not in ['queued','running']:return
 row.status='running';db.commit()
 try:
  case=db.get(EvidenceCase,row.case_id);revision=db.get(CptRevision,case.revision_id);network=db.get(BayesNetwork,revision.network_id);graph=nodes(db,network);cpt=rows(db,revision);snapshot={'nodes':graph,'cpt':cpt,'evidence':case.evidence,'target':case.target,'candidates':case.candidates,'revision_id':revision.id,'version':revision.version};analysis=information_gain(graph,cpt,case.evidence,case.target,case.candidates);base=analysis['baseline']
  fingerprint=hashlib.sha256(json.dumps(snapshot,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();row.result={'network_name':network.name,'revision_name':revision.name,'version':revision.version,'case_name':case.name,'snapshot':snapshot,'analysis':analysis,'input_sha256':fingerprint,'assumptions':'只按给定模拟DAG/CPT进行技术研修；不是从数据发现因果，不生成真实维修指令。'}
  row.log_evidence=base['log_evidence'];row.evidence_probability=base['evidence_probability'];row.evidence_underflow=base['evidence_probability_underflow'];row.target_entropy=analysis['target_entropy']
  for p in base['posterior']:db.add(PosteriorState(id=str(uuid4()),run_id=row.id,**p))
  for candidate in analysis['candidates']:
   metric=CandidateMetric(id=str(uuid4()),run_id=row.id,**{k:candidate[k] for k in ['node_id','prior_entropy','expected_entropy','raw_information_gain','information_gain','micro_negative_clipped']});db.add(metric);db.flush()
   for b in candidate['branches']:db.add(BranchMetric(id=str(uuid4()),candidate_id=metric.id,log_evidence=b['inference']['log_evidence'] if b['inference'] else None,**{k:b[k] for k in ['state','probability','log_probability','probability_underflow','conditional_entropy','skipped_zero_probability']}))
  for i,step in enumerate(base['trace']):db.add(EliminationStep(id=str(uuid4()),run_id=row.id,step=i+1,**step))
  row.status='completed';db.commit()
 except Exception as error:
  db.rollback();row=db.get(InferenceRun,ident);row.status='failed';row.error=str(error)[:1000];db.commit()
