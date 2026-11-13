from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class CptRevision(RecordMixin,Base):
 __tablename__="revisions"
 __table_args__=(UniqueConstraint('network_id','version',name='uq_revision_network_version'),)
 name:Mapped[str]=mapped_column(String(180),unique=True)
 network_id:Mapped[str]=mapped_column(ForeignKey("networks.id"))
 version:Mapped[str]=mapped_column(String(40))
 description:Mapped[str]=mapped_column(Text,default="")
