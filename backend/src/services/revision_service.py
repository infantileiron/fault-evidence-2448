import json
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..models.revision import CptRevision
from ..models.network import BayesNetwork
from ..models.cpt_row import CptRow
from ..models.common import serialize
from .network_service import nodes
from .network_validation import validate_cpt
def rows(db,row):return [{k:getattr(r,k) for k in ['node_id','parent_values','p0','p1','row_sum']} for r in db.scalars(select(CptRow).where(CptRow.revision_id==row.id).order_by(CptRow.node_id,CptRow.id)).all()]
def expanded(db,row):return {**serialize(row),'rows':rows(db,row)}
def create(db,body):
 network=db.get(BayesNetwork,body.network_id)
 if not network:raise HTTPException(422,'网络不存在')
 try:clean=validate_cpt(nodes(db,network),json.loads(body.rows_json))
 except (ValueError,TypeError) as error:raise HTTPException(422,str(error))
 if db.scalar(select(CptRevision).where((CptRevision.name==body.name)|((CptRevision.network_id==body.network_id)&(CptRevision.version==body.version)))):raise HTTPException(409,'版本名称或该网络版本号已存在，不可覆盖')
 row=CptRevision(id=str(uuid4()),name=body.name,network_id=body.network_id,version=body.version,description=body.description)
 try:
  db.add(row);db.flush()
  for item in clean:db.add(CptRow(id=str(uuid4()),revision_id=row.id,**item))
  db.commit()
 except IntegrityError:
  db.rollback();raise HTTPException(409,'版本名称或该网络版本号已存在，不可覆盖')
 return row
