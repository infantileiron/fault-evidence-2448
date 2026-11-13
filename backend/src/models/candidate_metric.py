from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class CandidateMetric(RecordMixin,Base):
 __tablename__="candidate_metrics"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 node_id:Mapped[str]=mapped_column(String(32))
 prior_entropy:Mapped[float]=mapped_column(Double)
 expected_entropy:Mapped[float]=mapped_column(Double)
 raw_information_gain:Mapped[float]=mapped_column(Double)
 information_gain:Mapped[float]=mapped_column(Double)
 micro_negative_clipped:Mapped[bool]=mapped_column(Boolean)
