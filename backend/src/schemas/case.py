from pydantic import BaseModel,ConfigDict,Field
class CaseCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 name:str=Field(min_length=2,max_length=180)
 revision_id:str
 target:str
 evidence_json:str=Field(default='{}',max_length=5000)
 candidates_json:str=Field(default='null',max_length=5000)
