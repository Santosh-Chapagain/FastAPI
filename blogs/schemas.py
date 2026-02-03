from pydantic import BaseModel, Field, ConfigDict


class Blog(BaseModel):
    title: str = Field(..., description="Write title of your blog")
    body: str = Field(..., description="Write your blog")


class ShowBlog(BaseModel):
    title: str 
    model_config = ConfigDict(from_attributes=True)
