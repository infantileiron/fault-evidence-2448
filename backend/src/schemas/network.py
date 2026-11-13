from pydantic import BaseModel,ConfigDict,Field
class NetworkCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 name:str=Field(min_length=2,max_length=180)
 description:str=Field(default='',max_length=3000)
 nodes_json:str=Field(min_length=2,max_length=30000)
class NetworkPatch(BaseModel):
 model_config=ConfigDict(extra='forbid')
 description:str=Field(max_length=3000)
