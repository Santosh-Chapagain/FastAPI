from pydantic import BaseModel, Field, ConfigDict


class Blog(BaseModel):
    title: str = Field(..., description="Write title of your blog")
    body: str = Field(..., description="Write your blog")
    user_id: int


class ShowBlog(BaseModel):
    title: str
    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)
