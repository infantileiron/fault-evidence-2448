from enum import StrEnum
class Role(StrEnum):
 ADMIN="admin"
 ANALYST="analyst"
 VIEWER="viewer"
class RunStatus(StrEnum):
 QUEUED="queued"
 RUNNING="running"
 COMPLETED="completed"
 FAILED="failed"
class ReviewState(StrEnum):
 SUBMITTED="submitted"
 APPROVED="approved"
