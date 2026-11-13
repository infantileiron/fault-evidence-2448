from sqlalchemy import String,Text,JSON,ForeignKey,Double,Boolean
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class NetworkNode(RecordMixin,Base):
 __tablename__="network_nodes"
 network_id:Mapped[str]=mapped_column(ForeignKey("networks.id"))
 node_id:Mapped[str]=mapped_column(String(32))
 label:Mapped[str]=mapped_column(String(120))
 parents:Mapped[dict]=mapped_column(JSON)
