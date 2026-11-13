from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class EliminationStep(RecordMixin,Base):
 __tablename__="elimination_steps"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 step:Mapped[int]
 variable:Mapped[str]=mapped_column(String(32))
 input_scopes:Mapped[dict]=mapped_column(JSON)
 product_scope:Mapped[dict]=mapped_column(JSON)
 product_cells:Mapped[int]
 output_scope:Mapped[dict]=mapped_column(JSON)
 output_cells:Mapped[int]
