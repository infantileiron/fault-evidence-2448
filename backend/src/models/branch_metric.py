from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class BranchMetric(RecordMixin,Base):
 __tablename__="branch_metrics"
 candidate_id:Mapped[str]=mapped_column(ForeignKey("candidate_metrics.id"))
 state:Mapped[int]
 probability:Mapped[float]=mapped_column(Double)
 log_probability:Mapped[float|None]=mapped_column(Double,nullable=True)
 conditional_entropy:Mapped[float|None]=mapped_column(Double,nullable=True)
 log_evidence:Mapped[float|None]=mapped_column(Double,nullable=True)
 skipped_zero_probability:Mapped[bool]=mapped_column(Boolean)
 probability_underflow:Mapped[bool]=mapped_column(Boolean)
