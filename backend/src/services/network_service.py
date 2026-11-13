import json
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.network import BayesNetwork
from ..models.network_node import NetworkNode
from ..models.common import serialize
from .network_validation import validate_network
def nodes(db,row):return [{k:getattr(n,k) for k in ['node_id','label','parents']} for n in db.scalars(select(NetworkNode).where(NetworkNode.network_id==row.id).order_by(NetworkNode.node_id)).all()]
def expanded(db,row):return {**serialize(row),'nodes':nodes(db,row),'topological_order':validate_network(nodes(db,row))['topological_order']}
def create(db,body):
 try:clean=validate_network(json.loads(body.nodes_json))['nodes']
 except (ValueError,TypeError) as error:raise HTTPException(422,str(error))
 if db.scalar(select(BayesNetwork).where(BayesNetwork.name==body.name)):raise HTTPException(409,'网络名称已存在')
 row=BayesNetwork(id=str(uuid4()),name=body.name,description=body.description);db.add(row);db.flush()
 for node in clean:db.add(NetworkNode(id=str(uuid4()),network_id=row.id,**node))
 db.commit();return row
