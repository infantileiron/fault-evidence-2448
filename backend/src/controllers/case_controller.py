from sqlalchemy import select
from ..models.case import EvidenceCase
from ..models.common import serialize
from ..services import case_service as service
from .common import require
def list_all(db):return [serialize(row) for row in db.scalars(select(EvidenceCase).order_by(EvidenceCase.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,EvidenceCase,ident)
 return serialize(row)
def create(db,body):
 row=service.create(db,body)
 return serialize(row)
