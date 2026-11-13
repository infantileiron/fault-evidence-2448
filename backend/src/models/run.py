from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class InferenceRun(RecordMixin,Base):
 __tablename__="runs"
 case_id:Mapped[str]=mapped_column(ForeignKey("cases.id"))
 status:Mapped[str]=mapped_column(String(20),default="queued")
 result:Mapped[dict]=mapped_column(JSON,default=dict)
 error:Mapped[str]=mapped_column(Text,default="")
 log_evidence:Mapped[float|None]=mapped_column(Double,nullable=True)
 evidence_probability:Mapped[float|None]=mapped_column(Double,nullable=True)
 target_entropy:Mapped[float|None]=mapped_column(Double,nullable=True)
 evidence_underflow:Mapped[bool]=mapped_column(Boolean,default=False)
