from fastapi import FastAPI
from pydantic import BaseModel , Field

app = FastAPI()

@app.get('/')
def index():
    return "heyy"

@app.get('/about')
def about():
    return "This is about us page"

# @app.get('/blog/{id}')
# def blog_id(id):
#     return {'data': id}


class Blog(BaseModel):
    blog_id: int = Field(... , description= "Write blog id.")
    title: str = Field(..., description="Give title of blog")

@app.post('/blog')
def create_blog(blog: Blog):
    return f"{blog.blog_id} is created with title {blog.title}"
