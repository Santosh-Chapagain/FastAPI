from fastapi import FastAPI, Depends, status, HTTPException, Response
from blogs import schemas
from blogs import models
from typing import Optional
from blogs import database
from .database import engine
from .database import sessionLocal
from sqlalchemy.orm import Session
from typing import Annotated , List
app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependent = Annotated[Session, Depends(get_db)]


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def createBlog(blog: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog' , response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', response_model=schemas.ShowBlog)
def by_id(id: int, response: Response,  db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(id == models.Blog.id).first()
    if not blog:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available'}

    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlog(db: db_dependent, id: int):
    blog = db.query(models.Blog).filter(id == models.Blog.id).first()
    if not blog:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"BlogId is not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: db_dependent):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No such BlogId {id}")
    update_data = {
        'title': request.blog_title,
        'body': request.blog_text
    }
    blog.update(update_data, synchronize_session=False)

    db.commit()
    return 'updated'


