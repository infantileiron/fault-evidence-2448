from pydantic import BaseModel,ConfigDict,Field
class RunCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 case_id:str
