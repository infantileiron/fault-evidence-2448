from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class CptRow(RecordMixin,Base):
 __tablename__="cpt_rows"
 revision_id:Mapped[str]=mapped_column(ForeignKey("revisions.id"))
 node_id:Mapped[str]=mapped_column(String(32))
 parent_values:Mapped[dict]=mapped_column(JSON)
 p0:Mapped[float]=mapped_column(Double)
 p1:Mapped[float]=mapped_column(Double)
 row_sum:Mapped[float]=mapped_column(Double)
