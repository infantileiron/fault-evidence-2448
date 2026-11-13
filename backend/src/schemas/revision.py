from pydantic import BaseModel,ConfigDict,Field
class RevisionCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 name:str=Field(min_length=2,max_length=180)
 network_id:str
 version:str=Field(min_length=1,max_length=40)
 description:str=Field(default='',max_length=3000)
 rows_json:str=Field(min_length=2,max_length=100000)
