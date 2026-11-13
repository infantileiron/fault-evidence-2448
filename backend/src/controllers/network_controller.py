from sqlalchemy import select
from ..models.network import BayesNetwork
from ..models.common import serialize
from ..services import network_service as service
from .common import require
def list_all(db):return [service.expanded(db,row) for row in db.scalars(select(BayesNetwork).order_by(BayesNetwork.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,BayesNetwork,ident)
 return service.expanded(db,row)
def create(db,body):
 row=service.create(db,body)
 return service.expanded(db,row)
def patch(db,ident,body):
 row=require(db,BayesNetwork,ident);row.description=body.description;db.commit();return service.expanded(db,row)
