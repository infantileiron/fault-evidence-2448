from sqlalchemy import select
from ..models.review import EvidenceReview
from ..models.common import serialize
from ..services import review_service as service
from .common import require
def list_all(db):return [serialize(row) for row in db.scalars(select(EvidenceReview).order_by(EvidenceReview.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,EvidenceReview,ident)
 return serialize(row)
def create(db,body):
 row=service.create(db,body)
 return serialize(row)
def approve(db,ident,user):return serialize(service.approve(db,require(db,EvidenceReview,ident),user))
