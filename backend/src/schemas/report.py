from pydantic import BaseModel,ConfigDict,Field
class ReportCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 review_id:str
 title:str=Field(min_length=2,max_length=180)
