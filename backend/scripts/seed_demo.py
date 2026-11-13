import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select,func
from src.config.database import Session,initialize
from src.models.user import User
from src.models.network import BayesNetwork
from src.models.network_node import NetworkNode
from src.models.revision import CptRevision
from src.models.cpt_row import CptRow
from src.models.case import EvidenceCase
from src.models.run import InferenceRun
from src.models.review import EvidenceReview
from src.models.report import Report
from src.utils.security import hash_password
from src.services.network_validation import validate_cpt,validate_evidence
from src.services.run_service import compute
from scripts.demo_data import DEMO_NODES,DEMO_CPT,HAND_NODES,HAND_CPT,TINY_NODES,TINY_CPT

def seed():
 initialize()
 with Session() as db:
  for role in ['admin','analyst','viewer']:
   if not db.get(User,'seed-'+role):db.add(User(id='seed-'+role,email=role+'@evidence.demo',password_hash=hash_password('EvidenceDemo2026!'),role=role))
  for ident,name,nodes,cpt in [('demo-network','CY-07 研修证据图',DEMO_NODES,DEMO_CPT),('hand-network','F与S手算图',HAND_NODES,HAND_CPT),('tiny-network','极小正证据对数图',TINY_NODES,TINY_CPT)]:
   if not db.get(BayesNetwork,ident):
    db.add(BayesNetwork(id=ident,name=name,description='澄翼技术研修组15人；CY-07_evidence_202611.json，模拟DAG/CPT，仅给定模型推理，不发现因果、不输出真实维修指令。'));db.flush()
    for node in nodes:db.add(NetworkNode(id=ident+'-'+node['node_id'],network_id=ident,**node))
   rid='demo-revision' if ident=='demo-network' else ident.replace('network','revision')
   if not db.get(CptRevision,rid):
    db.add(CptRevision(id=rid,name=name+' / CPT r1',network_id=ident,version='r1',description='按parents顺序列出完整父配置；固定版本不可覆盖。'));db.flush()
    for i,row in enumerate(validate_cpt(nodes,cpt)):db.add(CptRow(id=rid+'-'+str(i),revision_id=rid,**row))
  cases=[('demo-case','温升与告警联合证据','demo-revision','Fault',{'Heat':1,'Alarm':1},DEMO_NODES),('hand-case','S1后的F手算后验','hand-revision','F',{'S':1},HAND_NODES),('tiny-case','两项1e-200证据仍可行','tiny-revision','Q',{'A':1,'B':1},TINY_NODES),('zero-case','零概率反例：Fault0与Lock1','demo-revision','Fault',{'Fault':0,'Lock':1},DEMO_NODES),('observed-case','已观测目标先检查证据','demo-revision','Fault',{'Fault':1,'Alarm':1},DEMO_NODES)]
  for ident,name,rid,target,evidence,nodes in cases:
   if not db.get(EvidenceCase,ident):db.add(EvidenceCase(id=ident,name=name,revision_id=rid,target=target,evidence=evidence,candidates=validate_evidence(nodes,evidence,target)))
  db.flush()
  if not db.get(InferenceRun,'demo-run'):db.add(InferenceRun(id='demo-run',case_id='demo-case',status='queued',result={},error=''))
  db.commit();run=db.get(InferenceRun,'demo-run')
  if run.status=='queued':compute(db,'demo-run')
  run=db.get(InferenceRun,'demo-run')
  if run.status=='completed':
   if not db.get(EvidenceReview,'demo-review'):db.add(EvidenceReview(id='demo-review',run_id='demo-run',action='已核对CPT r1、证据logZ及候选分支；仅模拟研修，信息增益不等于故障修复收益。',state='approved',reviewer='admin@evidence.demo'));db.flush()
   if not db.get(Report,'demo-report'):db.add(Report(id='demo-report',review_id='demo-review',title='CY-07 联合证据研修底稿',snapshot={'result':run.result,'action':'已核对CPT、logZ、分支与研修限制','reviewer':'admin@evidence.demo'}))
  db.commit();counts={t.__tablename__:db.scalar(select(func.count()).select_from(t)) for t in [User,BayesNetwork,NetworkNode,CptRevision,CptRow,EvidenceCase,InferenceRun,EvidenceReview,Report]};print(json.dumps(counts));return counts
if __name__=='__main__':seed()
