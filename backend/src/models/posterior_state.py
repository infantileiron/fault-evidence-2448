from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class PosteriorState(RecordMixin,Base):
 __tablename__="posterior_states"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 state:Mapped[int]
 probability:Mapped[float]=mapped_column(Double)
 log_probability:Mapped[float|None]=mapped_column(Double,nullable=True)
 probability_underflow:Mapped[bool]=mapped_column(Boolean)
