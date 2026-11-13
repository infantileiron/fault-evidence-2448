from sqlalchemy import select
from ..models.revision import CptRevision
from ..models.common import serialize
from ..services import revision_service as service
from .common import require
def list_all(db):return [service.expanded(db,row) for row in db.scalars(select(CptRevision).order_by(CptRevision.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,CptRevision,ident)
 return service.expanded(db,row)
def create(db,body):
 row=service.create(db,body)
 return service.expanded(db,row)
