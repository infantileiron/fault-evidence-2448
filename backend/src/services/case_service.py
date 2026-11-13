import json
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.case import EvidenceCase
from ..models.revision import CptRevision
from ..models.network import BayesNetwork
from .network_service import nodes
from .network_validation import validate_evidence
def create(db,body):
 revision=db.get(CptRevision,body.revision_id)
 if not revision:raise HTTPException(422,'CPT版本不存在')
 try:
  evidence=json.loads(body.evidence_json);candidates=validate_evidence(nodes(db,db.get(BayesNetwork,revision.network_id)),evidence,body.target,json.loads(body.candidates_json))
 except (ValueError,TypeError) as error:raise HTTPException(422,str(error))
 if db.scalar(select(EvidenceCase).where(EvidenceCase.name==body.name)):raise HTTPException(409,'案例名称已存在')
 row=EvidenceCase(id=str(uuid4()),name=body.name,revision_id=revision.id,target=body.target,evidence=evidence,candidates=candidates);db.add(row);db.commit();return row
