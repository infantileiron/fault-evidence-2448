from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class EvidenceCase(RecordMixin,Base):
 __tablename__="cases"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 revision_id:Mapped[str]=mapped_column(ForeignKey("revisions.id"))
 target:Mapped[str]=mapped_column(String(32))
 evidence:Mapped[dict]=mapped_column(JSON)
 candidates:Mapped[dict]=mapped_column(JSON)
