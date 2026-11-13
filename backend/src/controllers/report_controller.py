from sqlalchemy import select
from ..models.report import Report
from ..models.common import serialize
from ..services import report_service as service
from .common import require
def list_all(db):return [serialize(row) for row in db.scalars(select(Report).order_by(Report.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,Report,ident)
 return serialize(row)
def create(db,body):
 row=service.create(db,body)
 return serialize(row)
