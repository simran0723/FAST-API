from pydantic import BaseModel


# input schema
class BlogCreate(BaseModel):
    title : str
    content : str


# output schema

class BlogResponse(BaseModel):
    id :int
    title : str
    content:str

    class config:
        from_attributes = True